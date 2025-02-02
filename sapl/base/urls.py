import os

from django.conf.urls import include, url
from django.contrib.auth import views
from django.contrib.auth.decorators import permission_required

from django.views.generic.base import RedirectView, TemplateView

from sapl.base.views import (AutorCrud, ConfirmarEmailView, TipoAutorCrud, get_estatistica,
                             RecuperarSenhaEmailView, RecuperarSenhaFinalizadoView,
                             RecuperarSenhaConfirmaView, RecuperarSenhaCompletoView, RelatorioMateriaAnoAssuntoView,
                             IndexView, UserCrud)
from sapl.settings import MEDIA_URL, LOGOUT_REDIRECT_URL

from .apps import AppConfig
from .forms import LoginForm
from .views import (LoginSapl, AlterarSenha, AppConfigCrud, CasaLegislativaCrud,
                    HelpTopicView, LogotipoView, RelatorioAtasView,
                    RelatorioAudienciaView, RelatorioDataFimPrazoTramitacaoView, RelatorioHistoricoTramitacaoView,
                    RelatorioMateriasPorAnoAutorTipoView, RelatorioMateriasPorAutorView,
                    RelatorioMateriasTramitacaoView, RelatorioPresencaSessaoView, RelatorioReuniaoView, SaplSearchView,
                    RelatorioNormasPublicadasMesView, RelatorioNormasVigenciaView,
                    EstatisticasAcessoNormas, RelatoriosListView, ListarInconsistenciasView,
                    ListarProtocolosDuplicadosView, ListarProtocolosComMateriasView, ListarMatProtocoloInexistenteView,
                    ListarParlamentaresDuplicadosView, ListarFiliacoesSemDataFiliacaoView,
                    ListarMandatoSemDataInicioView, ListarParlMandatosIntersecaoView, ListarParlFiliacoesIntersecaoView,
                    ListarAutoresDuplicadosView, ListarBancadaComissaoAutorExternoView, ListarLegislaturaInfindavelView,
                    ListarAnexadasCiclicasView, ListarAnexadosCiclicosView, pesquisa_textual,
                    RelatorioHistoricoTramitacaoAdmView, RelatorioDocumentosAcessoriosView, RelatorioNormasPorAutorView)


app_name = AppConfig.name

admin_user = [
    url(r'^sistema/usuario/', include(UserCrud.get_urls())),

]

alterar_senha = [
    url(r'^sistema/alterar-senha/$',
        AlterarSenha.as_view(),
        name='alterar_senha'),

]

recuperar_senha = [
    url(r'^recuperar-senha/email/$', RecuperarSenhaEmailView.as_view(),
        name='recuperar_senha_email'),
    url(r'^recuperar-senha/finalizado/$',
        RecuperarSenhaFinalizadoView.as_view(), name='recuperar_senha_finalizado'),
    url(r'^recuperar-senha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', RecuperarSenhaConfirmaView.as_view(),
        name='recuperar_senha_confirma'),
    url(r'^recuperar-senha/completo/$',
        RecuperarSenhaCompletoView.as_view(), name='recuperar_senha_completo'),
]

urlpatterns = [
    url(r'^$', IndexView.as_view(template_name='index.html'), name='sapl_index'),

    url(r'^sistema/autor/tipo/', include(TipoAutorCrud.get_urls())),
    url(r'^sistema/autor/', include(AutorCrud.get_urls())),

    url(r'^sistema/ajuda/(?P<topic>\w+)$',
        HelpTopicView.as_view(), name='help_topic'),
    url(r'^sistema/ajuda/$', TemplateView.as_view(template_name='ajuda.html'),
        name='help'),
    url(r'^sistema/casa-legislativa/', include(CasaLegislativaCrud.get_urls()),
        name="casa_legislativa"),
    url(r'^sistema/app-config/', include(AppConfigCrud.get_urls())),

    # TODO mover estas telas para a app 'relatorios'
    url(r'^sistema/relatorios/$',
        RelatoriosListView.as_view(), name='relatorios_list'),
    url(r'^sistema/relatorios/materia-por-autor$',
        RelatorioMateriasPorAutorView.as_view(), name='materia_por_autor'),
    url(r'^sistema/relatorios/relatorio-por-mes$',
        RelatorioNormasPublicadasMesView.as_view(), name='normas_por_mes'),
    url(r'^sistema/relatorios/relatorio-por-vigencia$',
        RelatorioNormasVigenciaView.as_view(), name='normas_por_vigencia'),
    url(r'^sistema/relatorios/estatisticas-acesso$',
        EstatisticasAcessoNormas.as_view(), name='estatisticas_acesso'),
    url(r'^sistema/relatorios/materia-por-ano-autor-tipo$',
        RelatorioMateriasPorAnoAutorTipoView.as_view(),
        name='materia_por_ano_autor_tipo'),
    url(r'^sistema/relatorios/materia-por-tramitacao$',
        RelatorioMateriasTramitacaoView.as_view(),
        name='materia_por_tramitacao'),
    url(r'^sistema/relatorios/materia-por-assunto$',
        RelatorioMateriaAnoAssuntoView.as_view(),
        name='materia_por_ano_assunto'),
    url(r'^sistema/relatorios/historico-tramitacoes$',
        RelatorioHistoricoTramitacaoView.as_view(),
        name='historico_tramitacoes'),
    url(r'^sistema/relatorios/data-fim-prazo-tramitacoes$',
        RelatorioDataFimPrazoTramitacaoView.as_view(),
        name='data_fim_prazo_tramitacoes'),
    url(r'^sistema/relatorios/presenca$',
        RelatorioPresencaSessaoView.as_view(),
        name='presenca_sessao'),
    url(r'^sistema/relatorios/atas$',
        RelatorioAtasView.as_view(),
        name='atas'),
    url(r'^sistema/relatorios/reuniao$',
        RelatorioReuniaoView.as_view(),
        name='reuniao'),
    url(r'^sistema/relatorios/audiencia$',
        RelatorioAudienciaView.as_view(),
        name='audiencia'),
    url(r'^sistema/relatorios/historico-tramitacoesadm$',
        RelatorioHistoricoTramitacaoAdmView.as_view(),
        name='historico_tramitacoes_adm'),
    url(r'^sistema/relatorios/documentos_acessorios$',
        RelatorioDocumentosAcessoriosView.as_view(),
        name='relatorio_documentos_acessorios'),
    url(r'^sistema/relatorios/normas-por-autor$',
        RelatorioNormasPorAutorView.as_view(), name='normas_por_autor'),

    url(r'^email/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        ConfirmarEmailView.as_view(), name='confirmar_email'),

    url(r'^sistema/inconsistencias/$',
        ListarInconsistenciasView.as_view(),
        name='lista_inconsistencias'),
    url(r'^sistema/inconsistencias/protocolos_duplicados$',
        ListarProtocolosDuplicadosView.as_view(),
        name='lista_protocolos_duplicados'),
    url(r'^sistema/inconsistencias/protocolos_com_materias$',
        ListarProtocolosComMateriasView.as_view(),
        name='lista_protocolos_com_materias'),
    url(r'^sistema/inconsistencias/materias_protocolo_inexistente$',
        ListarMatProtocoloInexistenteView.as_view(),
        name='lista_materias_protocolo_inexistente'),
    url(r'^sistema/inconsistencias/filiacoes_sem_data_filiacao$',
        ListarFiliacoesSemDataFiliacaoView.as_view(),
        name='lista_filiacoes_sem_data_filiacao'),
    url(r'^sistema/inconsistencias/mandato_sem_data_inicio',
        ListarMandatoSemDataInicioView.as_view(),
        name='lista_mandato_sem_data_inicio'),
    url(r'^sistema/inconsistencias/parlamentares_duplicados$',
        ListarParlamentaresDuplicadosView.as_view(),
        name='lista_parlamentares_duplicados'),
    url(r'^sistema/inconsistencias/parlamentares_mandatos_intersecao$',
        ListarParlMandatosIntersecaoView.as_view(),
        name='lista_parlamentares_mandatos_intersecao'),
    url(r'^sistema/inconsistencias/parlamentares_filiacoes_intersecao$',
        ListarParlFiliacoesIntersecaoView.as_view(),
        name='lista_parlamentares_filiacoes_intersecao'),
    url(r'^sistema/inconsistencias/autores_duplicados$',
        ListarAutoresDuplicadosView.as_view(),
        name='lista_autores_duplicados'),
    url(r'^sistema/inconsistencias/bancada_comissao_autor_externo$',
        ListarBancadaComissaoAutorExternoView.as_view(),
        name='lista_bancada_comissao_autor_externo'),
    url(r'^sistema/inconsistencias/legislatura_infindavel$',
        ListarLegislaturaInfindavelView.as_view(),
        name='lista_legislatura_infindavel'),
    url(r'sistema/inconsistencias/anexadas_ciclicas$',
        ListarAnexadasCiclicasView.as_view(),
        name='lista_anexadas_ciclicas'),
    url(r'sistema/inconsistencias/anexados_ciclicos$',
        ListarAnexadosCiclicosView.as_view(),
        name='lista_anexados_ciclicos'),

    url(r'^sistema/pesquisa-textual',
        pesquisa_textual,
        name='pesquisa_textual'),

    url(r'^sistema/estatisticas', get_estatistica),

    # todos os sublinks de sistema devem vir acima deste
    url(r'^sistema/$', permission_required('base.view_tabelas_auxiliares')
        (TemplateView.as_view(template_name='sistema.html')),
        name='sistema'),

    url(r'^login/$', LoginSapl.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(),
        {'next_page': LOGOUT_REDIRECT_URL}, name='logout'),

    url(r'^sistema/search/', SaplSearchView(), name='haystack_search'),

    # Folhas XSLT e extras referenciadas por documentos migrados do sapl 2.5
    url(r'^(sapl/)?XSLT/HTML/(?P<path>.*)$', RedirectView.as_view(
        url=os.path.join(MEDIA_URL, 'sapl/public/XSLT/HTML/%(path)s'),
        permanent=False)),
    # url do logotipo usada em documentos migrados do sapl 2.5
    url(r'^(sapl/)?sapl_documentos/props_sapl/logo_casa',
        LogotipoView.as_view(), name='logotipo'),


] + recuperar_senha + alterar_senha + admin_user
