# -*- coding: utf-8 -*-

import unittest
from mock import MagicMock, patch
from py_inspector import verificadores


class CustomReport(unittest.TestCase):
    def test_deve_retornar_quantidade_erros(self):
        options = MagicMock()
        report = verificadores.CustomReport(options)
        report._deferred_print = []
        report.file_errors = 3
        report.get_file_results().should.be.equal(3)

    def test_deve_montar_erros(self):
        options = MagicMock()
        report = verificadores.CustomReport(options)
        report.filename = 'filename'
        report.line_offset = 2
        report.file_errors = 3
        report._deferred_print = [(23, 2, 'code', 'text', '_'), (22, 3, 'code zas', 'text zas', '_ zas')]
        report.get_file_results()
        report.results.should.be.equal([{'path': 'filename', 'code': 'code zas', 'text': 'text zas', 'col': 4, 'row': 24}, {'path': 'filename', 'code': 'code', 'text': 'text', 'col': 3, 'row': 25}])


class ValidandoPep8(unittest.TestCase):
    @patch('py_inspector.verificadores.assert_true')
    def test_deve_passar_se_nao_tiver_erro_de_pep8(self, assert_mock):
        verificadores.CustomReport.results = []
        validador = verificadores.TestValidacaoPython()
        from tests.unitarios import arquivo_sem_erro_pep8
        validador.validacao_pep8([arquivo_sem_erro_pep8.__file__.replace('pyc', 'py')])
        assert_mock.called.should.be.falsy

    @patch('py_inspector.verificadores.assert_true')
    def test_deve_dar_erro_se_tiver_erro_de_pep8(self, assert_mock):
        verificadores.CustomReport.results = []
        validador = verificadores.TestValidacaoPython()
        from tests.unitarios import arquivo_com_erro_pep8
        arquivo = arquivo_com_erro_pep8.__file__.replace('pyc', 'py')
        validador.validacao_pep8([arquivo])
        assert_mock.assert_called_with(False, 'PEP8 em {}:16:5 - E303: too many blank lines (2)'.format(arquivo))
