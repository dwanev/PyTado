import json
import unittest
from unittest import mock

from . import common

from PyTado.http import Http
from PyTado.interface import Tado
import PyTado.interface.api as API


class TestTadoInterface(unittest.TestCase):
    """Test cases for main tado interface class"""

    def test_interface_with_tado_api(self):
        login_patch = mock.patch(
            "PyTado.http.Http._login", return_value=(False, "foo")
        )
        login_mock = login_patch.start()
        self.addCleanup(login_patch.stop)

        with mock.patch("PyTado.interface.api.my_tado.Tado.get_me") as mock_it:
            tado_interface = Tado("my@username.com", "mypassword")
            tado_interface.get_me()

            assert not tado_interface._http.is_x_line
            mock_it.assert_called_once()

        with mock.patch(
            "PyTado.interface.api.hops_tado.TadoX.get_me"
        ) as mock_it:
            tado_interface = Tado("my@username.com", "mypassword")
            tado_interface.get_me()

            mock_it.assert_not_called()

        assert login_mock.call_count == 2

    def test_interface_with_tadox_api(self):
        login_patch = mock.patch(
            "PyTado.http.Http._login", return_value=(True, "foo")
        )
        login_mock = login_patch.start()
        self.addCleanup(login_patch.stop)

        with mock.patch(
            "PyTado.interface.api.hops_tado.TadoX.get_me"
        ) as mock_it:
            tado_interface = Tado("my@username.com", "mypassword")
            tado_interface.get_me()

            mock_it.assert_called_once()
            assert tado_interface._http.is_x_line

        login_mock.assert_called_once()

    def test_error_handling_on_api_calls(self):
        login_patch = mock.patch(
            "PyTado.http.Http._login", return_value=(False, "foo")
        )
        login_patch.start()
        self.addCleanup(login_patch.stop)

        with mock.patch("PyTado.interface.api.my_tado.Tado.get_me") as mock_it:
            mock_it.side_effect = Exception("API Error")

            tado_interface = Tado("my@username.com", "mypassword")

            with self.assertRaises(Exception) as context:
                tado_interface.get_me()

                self.assertIn("API Error", str(context.exception))
