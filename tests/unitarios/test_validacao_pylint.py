# -*- coding: utf-8 -*-

import unittest
import mock
from py_inspector import verificadores


class WritableObject(unittest.TestCase):
    def test_deve_adicionar_valores_na_lista_interna(self):
        writable = verificadores.WritableObject()
        writable.content.should.be.empty
        writable.write('valor')
        writable.content.should.be.equal(['valor'])

    def test_deve_adicionar_manter_valores_na_lista_interna(self):
        writable = verificadores.WritableObject()
        writable.content.should.be.empty
        writable.write('valor1')
        writable.write('valor2')
        writable.content.should.be.equal(['valor1', 'valor2'])

    def test_nao_deve_adicionar_valores_na_lista_se_for_quebra(self):
        writable = verificadores.WritableObject()
        writable.write('\n')
        writable.content.should.be.empty

    def test_nao_deve_adicionar_valores_na_lista_se_for_asteriscos(self):
        writable = verificadores.WritableObject()
        writable.write('**********')
        writable.content.should.be.empty

    def test_deve_retornar_a_lista_interna_no_read(self):
        writable = verificadores.WritableObject()
        writable.write('valor1')
        writable.write('valor2')
        writable.read().should.be.equal(['valor1', 'valor2'])


class ValidandoPyLint(unittest.TestCase):
    @mock.patch('py_inspector.verificadores.assert_true')
    @mock.patch('py_inspector.verificadores.lint')
    @mock.patch('py_inspector.verificadores.TextReporter')
    @mock.patch('py_inspector.verificadores.WritableObject')
    def test_nao_deve_dar_erro_se_resultado_for_vazio(self, writable_mock, reporter_mock, lint_mock, assert_mock):
        writable = mock.MagicMock()
        writable.read.return_value = []
        writable_mock.return_value = writable
        reporter = mock.MagicMock()
        reporter_mock.return_value = reporter
        validador = verificadores.TestValidacaoPython()
        validador.validacao_pylint(['arquivo'])
        reporter_mock.assert_called_with(writable)
        lint_mock.Run.assert_called_with(
            [
                'arquivo',
                '-r',
                'n',
                "--msg-template='Pylint em {path}:{line}:{column} [{msg_id}: {msg} em {obj}]'",
                '--disable=C0301,R0201,R0903',
                '--class-attribute-rgx=([A-Za-z_][A-Za-z0-9_]{2,60}|(__.*__))$',
                '--max-args=8'
            ],
            exit=False,
            reporter=reporter
        )
        assert_mock.called.should.be.falsy

    @mock.patch('py_inspector.verificadores.assert_true')
    @mock.patch('py_inspector.verificadores.lint')
    @mock.patch('py_inspector.verificadores.TextReporter')
    @mock.patch('py_inspector.verificadores.WritableObject')
    def test_deve_dar_erro_se_resultado_nao_for_vazio(self, writable_mock, reporter_mock, lint_mock, assert_mock):
        writable = mock.MagicMock()
        writable.read.return_value = ['erro na parada']
        writable_mock.return_value = writable
        validador = verificadores.TestValidacaoPython()
        validador.validacao_pylint(['arquivo'])
        assert_mock.assert_called_with(False, 'erro na parada')
