import subprocess
from getpass import getpass

import requests
from django.core import management
from sapl.legacy.migracao_dados import REPO, TAG_MARCO, gravar_marco, info, migrar_dados
from sapl.legacy.migracao_documentos import migrar_documentos
from sapl.legacy.migracao_usuarios import migrar_usuarios
from sapl.legacy.scripts.exporta_zope.variaveis_comuns import TAG_ZOPE
from sapl.legacy.scripts.verifica_diff import verifica_diff
from sapl.legacy_migration_settings import DIR_REPO, NOME_BANCO_LEGADO
from sapl.materia.models import Proposicao
from unipath import Path


def adornar_msg(msg):
    return "\n{1}\n{0}\n{1}".format(msg, "#" * len(msg))


def migrar(primeira_migracao=True, apagar_do_legado=False):
    if TAG_MARCO in REPO.tags:
        info("A migração já está feita.")
        return
    assert TAG_ZOPE in REPO.tags, adornar_msg(
        "Antes de migrar " "é necessário fazer a exportação de documentos do zope"
    )
    management.call_command("migrate")
    migracao_corretiva = not primeira_migracao
    if migracao_corretiva:
        gravar_marco("producao")
    fks_orfas = migrar_dados(primeira_migracao, apagar_do_legado)
    assert not fks_orfas, "Ainda existem FKs órfãs"
    migrar_usuarios(REPO.working_dir, primeira_migracao)
    migrar_documentos(REPO, primeira_migracao)
    if migracao_corretiva:
        dir_dados = gravar_marco("dados")
        REPO.git.add([dir_dados.name])

    gerar_backup_postgres()

    # versiona mudanças, se de fato existem
    if "master" not in REPO.heads or REPO.index.diff("HEAD"):
        REPO.index.commit("Migração concluída")
    REPO.git.execute("git tag -f".split() + [TAG_MARCO])

    if migracao_corretiva:
        sigla = NOME_BANCO_LEGADO[-3:]
        verifica_diff(sigla)


def gerar_backup_postgres(nome_banco=NOME_BANCO_LEGADO):
    print("Gerando backup do banco... ", end="", flush=True)
    arq_backup = DIR_REPO.child("{}.backup".format(nome_banco))
    arq_backup.remove()
    backup_cmds = [
        f"""
        docker exec postgres pg_dump -U sapl --format custom --blobs --verbose
        --file {arq_backup.name} {nome_banco}""",
        f"docker cp postgres:{arq_backup.name} {arq_backup}",
        f"docker exec postgres rm {arq_backup.name}",
    ]
    for cmd in backup_cmds:
        subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
    REPO.git.add([arq_backup.name])  # type: ignore
    print("SUCESSO")


def compactar_pasta(sufixo, pasta):
    print(f"Criando tar da pasta {pasta}... ", end="", flush=True)
    arq_tar = DIR_REPO.child(f"{NOME_BANCO_LEGADO}.{sufixo}")
    arq_tar.remove()
    subprocess.check_output(["tar", "czvfh", arq_tar, "-C", DIR_REPO, pasta])
    print("SUCESSO")


def compactar_media():
    # tar de media/sapl
    compactar_pasta("media.tar.gz", "sapl")
    # tar do sapl_documentos com documentos que não correspondem a nenhum registro
    compactar_pasta("sapl_documentos_remanescentes.tar.gz", "sapl_documentos")


PROPOSICAO_UPLOAD_TO = Proposicao._meta.get_field("texto_original").upload_to  # type: ignore


def salva_conteudo_do_sde(proposicao, conteudo):
    caminho_relativo = PROPOSICAO_UPLOAD_TO(
        proposicao, "proposicao_sde_{}.xml".format(proposicao.pk)
    )
    caminho_absoluto = Path(REPO.working_dir, caminho_relativo)
    caminho_absoluto.parent.mkdir(parents=True)
    # ajusta caminhos para folhas de estilo
    conteudo = conteudo.replace(b'"XSLT/HTML', b'"/XSLT/HTML')
    conteudo = conteudo.replace(b"'XSLT/HTML", b"'/XSLT/HTML")
    with open(caminho_absoluto, "wb") as arq:
        arq.write(conteudo)
    proposicao.texto_original = caminho_relativo
    proposicao.save()


def scrap_sde(url, usuario, senha=None):
    if not senha:
        senha = getpass()

    # login
    session = requests.session()
    res = session.post(
        "{}?retry=1".format(url),
        {"__ac_name": usuario, "__ac_password": senha},
    )
    assert res.status_code == 200

    url_proposicao_tmpl = "{}/sapl_documentos/proposicao/{}/renderXML?xsl=__default__"
    total = Proposicao.objects.count()
    for num, proposicao in enumerate(Proposicao.objects.all()):
        pk = proposicao.pk
        url_proposicao = url_proposicao_tmpl.format(url, pk)
        res = session.get(url_proposicao)
        print(
            "pk: {} status: {} {} (progresso: {:.2%})".format(
                pk, res.status_code, url_proposicao, num / total
            )
        )
        if res.status_code == 200:
            salva_conteudo_do_sde(proposicao, res.content)


def tenta_correcao():
    from sapl.legacy.migracao_dados import ocorrencias

    gravar_marco("producao")
    migrar_dados()
    assert "fk" not in ocorrencias, "AINDA EXISTEM FKS ORFAS"
    gravar_marco("dados")
    sigla = NOME_BANCO_LEGADO[-3:]
    verifica_diff(sigla)


def commit_ajustes():
    import git

    sigla = NOME_BANCO_LEGADO[-3:]

    ajustes = Path(
        f"/home/mazza/work/consulta_sapls/ajustes_pre_migracao/{sigla}.sql"
    ).read_file()
    assert ajustes.count("RESSUSCITADOS") <= 1

    consulta_sapl = git.Repo("/home/mazza/work/consulta_sapls")  # type: ignore
    consulta_sapl.git.add(
        f"/home/mazza/work/consulta_sapls/ajustes_pre_migracao/{sigla}*"
    )
    if consulta_sapl.git.diff("--cached"):
        consulta_sapl.index.commit(f"Ajusta {sigla}")
