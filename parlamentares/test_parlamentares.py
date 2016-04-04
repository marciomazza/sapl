import pytest
from django.core.urlresolvers import reverse
from model_mommy import mommy

from .models import (Dependente, Filiacao, Legislatura, Mandato, Parlamentar,
                     Partido, TipoDependente)


# vamos refazer a funcionalidade adicionando os campos ogrigatórios de mandato
@pytest.mark.django_db(transaction=False)
def TODO_DESLIGADO_RELIGAR_test_cadastro_parlamentar(client):
    mommy.make(Legislatura, pk=5)

    response = client.get(reverse('parlamentares_cadastro', kwargs={'pk': 5}))
    assert response.status_code == 200
    response = client.post(reverse('parlamentares_cadastro', kwargs={'pk': 5}),
                           {'nome_completo': 'Teresa Barbosa',
                            'nome_parlamentar': 'Terezinha',
                            'sexo': 'F',
                            'ativo': 'True'}, follow=True)

    parlamentar = Parlamentar.objects.first()
    assert "Terezinha" == parlamentar.nome_parlamentar
    if not parlamentar.ativo:
        pytest.fail("Parlamentar deve estar ativo")


@pytest.mark.django_db(transaction=False)
def test_filiacao_submit(client):
    mommy.make(Parlamentar, pk=14)
    mommy.make(Partido, pk=32)

    client.post(reverse('parlamentares_filiacao',
                        kwargs={'pk': 14}),
                {'partido': 32,
                 'data': '2016-03-22',
                 'salvar': 'salvar'},
                follow=True)

    filiacao = Filiacao.objects.first()
    assert 32 == filiacao.partido.pk


@pytest.mark.django_db(transaction=False)
def test_dependente_submit(client):
    mommy.make(Parlamentar, pk=14)
    mommy.make(Partido, pk=32)
    mommy.make(TipoDependente, pk=3)

    client.post(reverse('parlamentares_dependentes',
                        kwargs={'pk': 14}),
                {'nome': 'Eduardo',
                 'tipo': 3,
                 'sexo': 'M',
                 'salvar': 'salvar'},
                follow=True)

    dependente = Dependente.objects.first()
    assert 3 == dependente.tipo.pk
    assert 'Eduardo' == dependente.nome


@pytest.mark.django_db(transaction=False)
def test_form_errors_dependente(client):
    mommy.make(Parlamentar, pk=14)
    response = client.post(reverse('parlamentares_dependentes',
                                   kwargs={'pk': 14}),
                           {'salvar': 'salvar'},
                           follow=True)

    assert (response.context_data['form'].errors['nome'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['tipo'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['sexo'] ==
            ['Este campo é obrigatório.'])


@pytest.mark.django_db(transaction=False)
def test_form_errors_filiacao(client):
    mommy.make(Parlamentar, pk=14)

    response = client.post(reverse('parlamentares_filiacao',
                                   kwargs={'pk': 14}),
                           {'partido': '',
                            'salvar': 'salvar'},
                           follow=True)

    assert (response.context_data['form'].errors['partido'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['data'] ==
            ['Este campo é obrigatório.'])


@pytest.mark.django_db(transaction=False)
def test_mandato_submit(client):
    mommy.make(Parlamentar, pk=14)
    mommy.make(Legislatura, pk=5)

    client.post(reverse('parlamentares_mandato',
                        kwargs={'pk': 14}),
                {'legislatura': 5,
                 'data_fim_mandato': '2016-01-01',
                 'data_expedicao_diploma': '2016-03-22',
                 'observacao': 'Observação do mandato',
                 'salvar': 'salvar'},
                follow=True)

    mandato = Mandato.objects.first()
    assert 'Observação do mandato' == mandato.observacao


@pytest.mark.django_db(transaction=False)
def test_form_errors_mandato(client):
    mommy.make(Parlamentar, pk=14)
    response = client.post(reverse('parlamentares_mandato',
                                   kwargs={'pk': 14}),
                           {'legislatura': '',
                            'salvar': 'salvar'},
                           follow=True)

    assert (response.context_data['form'].errors['legislatura'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['data_fim_mandato'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['data_expedicao_diploma'] ==
            ['Este campo é obrigatório.'])


@pytest.mark.django_db(transaction=False)
def test_incluir_parlamentar_errors(client):
    mommy.make(Legislatura, pk=5)

    response = client.post(reverse('parlamentares_cadastro',
                                   kwargs={'pk': 5}),
                           {'salvar': 'salvar'},
                           follow=True)

    assert (response.context_data['form'].errors['nome_parlamentar'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['nome_completo'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['sexo'] ==
            ['Este campo é obrigatório.'])
    assert (response.context_data['form'].errors['ativo'] ==
            ['Este campo é obrigatório.'])
