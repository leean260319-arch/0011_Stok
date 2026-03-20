"""WebSettingsView 테스트 - 웹 대시보드 설정 페이지
버전: v1.0
"""
from unittest.mock import patch, MagicMock

import pytest

from src.ui.web_settings_view import WebSettingsView


@pytest.fixture
def widget(qtbot):
    w = WebSettingsView()
    qtbot.addWidget(w)
    return w


class TestWebSettingsViewUI:
    def test_widget_creation(self, widget):
        """위젯이 정상적으로 생성된다."""
        assert widget is not None

    def test_default_enabled(self, widget):
        """기본값으로 활성화 체크박스가 체크되어 있다."""
        assert widget.enabled_check.isChecked() is True

    def test_default_port(self, widget):
        """기본 포트가 8080이다."""
        assert widget.port_spin.value() == 8080

    def test_port_range(self, widget):
        """포트 범위가 1024~65535이다."""
        assert widget.port_spin.minimum() == 1024
        assert widget.port_spin.maximum() == 65535

    def test_default_username(self, widget):
        """기본 아이디가 admin이다."""
        assert widget.username_edit.text() == "admin"

    def test_password_echo_mode(self, widget):
        """비밀번호 필드가 Password 모드이다."""
        from PyQt6.QtWidgets import QLineEdit
        assert widget.password_edit.echoMode() == QLineEdit.EchoMode.Password

    def test_url_label_exists(self, widget):
        """접속 URL 라벨이 존재한다."""
        assert "http://" in widget.url_label.text()

    def test_connection_count_label(self, widget):
        """접속자 수 라벨이 0으로 초기화된다."""
        assert widget.connection_count_label.text() == "0"

    def test_update_connection_count(self, widget):
        """접속자 수 업데이트가 동작한다."""
        widget.update_connection_count(5)
        assert widget.connection_count_label.text() == "5"


class TestGetLocalIp:
    def test_get_local_ip_returns_string(self, widget):
        """get_local_ip가 문자열을 반환한다."""
        ip = widget.get_local_ip()
        assert isinstance(ip, str)
        parts = ip.split(".")
        assert len(parts) == 4


class TestSaveSettings:
    def test_save_settings(self, widget):
        """save_settings가 ConfigManager를 통해 저장한다."""
        widget.username_edit.setText("testuser")
        widget.port_spin.setValue(9090)
        widget.password_edit.setText("newpass")

        mock_config = MagicMock()
        with patch("src.config.ConfigManager", return_value=mock_config):
            widget.save_settings()
            mock_config.load.assert_called_once()
            # set 호출 확인
            calls = [c[0] for c in mock_config.set.call_args_list]
            keys = [c[0] for c in calls]
            assert "web_dashboard.enabled" in keys
            assert "web_dashboard.port" in keys
            assert "web_dashboard.username" in keys
            assert "web_dashboard.password" in keys
            mock_config.save.assert_called_once()

    def test_save_settings_no_password_change(self, widget):
        """비밀번호가 비어있으면 password는 저장하지 않는다."""
        widget.password_edit.setText("")

        mock_config = MagicMock()
        with patch("src.config.ConfigManager", return_value=mock_config):
            widget.save_settings()
            keys = [c[0][0] for c in mock_config.set.call_args_list]
            assert "web_dashboard.password" not in keys
