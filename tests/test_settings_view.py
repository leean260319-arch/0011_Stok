"""T027~T036 SettingsView 테스트"""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from PyQt6.QtWidgets import QGroupBox, QLineEdit, QDialog
from PyQt6.QtCore import Qt

from src.ui.settings_view import SettingsView


# ---------------------------------------------------------------------------
# T027 레이아웃 테스트
# ---------------------------------------------------------------------------
class TestSettingsViewLayout:
    """T027: 계정 설정 페이지 레이아웃"""

    def test_is_qwidget(self, qapp):
        from PyQt6.QtWidgets import QWidget
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        assert isinstance(view, QWidget)

    def test_has_five_groupboxes(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        boxes = view.findChildren(QGroupBox)
        assert len(boxes) == 5

    def test_groupbox_titles(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        titles = {b.title() for b in view.findChildren(QGroupBox)}
        assert "투자 모드" in titles
        assert "계좌 정보" in titles
        assert "API 발급 안내" in titles
        assert "연결 상태" in titles
        assert "보안 저장소" in titles


# ---------------------------------------------------------------------------
# T029 AccountForm 테스트
# ---------------------------------------------------------------------------
class TestAccountForm:
    """T029: 계좌 입력 폼"""

    def _make_view(self):
        with patch("src.ui.settings_view.CredentialManager"):
            return SettingsView()

    def test_account_number_lineedit_exists(self, qapp):
        view = self._make_view()
        assert hasattr(view, "account_number")
        assert isinstance(view.account_number, QLineEdit)

    def test_account_password_lineedit_exists(self, qapp):
        view = self._make_view()
        assert hasattr(view, "account_password")
        assert isinstance(view.account_password, QLineEdit)

    def test_api_key_lineedit_exists(self, qapp):
        view = self._make_view()
        assert hasattr(view, "api_key")
        assert isinstance(view.api_key, QLineEdit)

    def test_account_password_echo_mode(self, qapp):
        view = self._make_view()
        assert view.account_password.echoMode() == QLineEdit.EchoMode.Password

    def test_api_key_echo_mode(self, qapp):
        view = self._make_view()
        assert view.api_key.echoMode() == QLineEdit.EchoMode.Password

    def test_account_number_validator_accepts_10_digits(self, qapp):
        view = self._make_view()
        validator = view.account_number.validator()
        assert validator is not None
        from PyQt6.QtGui import QValidator
        state, _, _ = validator.validate("1234567890", 0)
        assert state == QValidator.State.Acceptable

    def test_account_number_validator_rejects_letters(self, qapp):
        view = self._make_view()
        validator = view.account_number.validator()
        from PyQt6.QtGui import QValidator
        state, _, _ = validator.validate("abcdefghij", 0)
        assert state != QValidator.State.Acceptable

    def test_account_number_validator_rejects_short(self, qapp):
        view = self._make_view()
        validator = view.account_number.validator()
        from PyQt6.QtGui import QValidator
        state, _, _ = validator.validate("12345", 0)
        assert state != QValidator.State.Acceptable


# ---------------------------------------------------------------------------
# T030 PasswordToggle 테스트
# ---------------------------------------------------------------------------
class TestPasswordToggle:
    """T030: 비밀번호 보기 토글"""

    def _make_view(self):
        with patch("src.ui.settings_view.CredentialManager"):
            return SettingsView()

    def test_toggle_password_visibility(self, qapp):
        view = self._make_view()
        assert view.account_password.echoMode() == QLineEdit.EchoMode.Password
        view.toggle_password_visibility(view.account_password)
        assert view.account_password.echoMode() == QLineEdit.EchoMode.Normal

    def test_toggle_password_back_to_hidden(self, qapp):
        view = self._make_view()
        view.toggle_password_visibility(view.account_password)
        view.toggle_password_visibility(view.account_password)
        assert view.account_password.echoMode() == QLineEdit.EchoMode.Password

    def test_toggle_api_key_visibility(self, qapp):
        view = self._make_view()
        view.toggle_password_visibility(view.api_key)
        assert view.api_key.echoMode() == QLineEdit.EchoMode.Normal


# ---------------------------------------------------------------------------
# T031 StatusPanel 테스트
# ---------------------------------------------------------------------------
class TestStatusPanel:
    """T031: 연결 상태 표시 패널"""

    def _make_view(self):
        with patch("src.ui.settings_view.CredentialManager"):
            return SettingsView()

    def test_has_status_label(self, qapp):
        view = self._make_view()
        assert hasattr(view, "status_label")

    def test_update_status_changes_text(self, qapp):
        view = self._make_view()
        view.update_status("연결 중...")
        assert "연결 중" in view.status_label.text()

    def test_update_status_with_step(self, qapp):
        view = self._make_view()
        view.update_status("로그인 중...", step=2)
        assert view.status_label.text() != ""


# ---------------------------------------------------------------------------
# T032 SecurityPanel 테스트
# ---------------------------------------------------------------------------
class TestSecurityPanel:
    """T032: 보안 저장소 상태 표시"""

    def _make_view(self):
        with patch("src.ui.settings_view.CredentialManager"):
            return SettingsView()

    def test_has_security_label(self, qapp):
        view = self._make_view()
        assert hasattr(view, "security_label")

    def test_security_label_has_text(self, qapp):
        view = self._make_view()
        assert view.security_label.text() != ""


# ---------------------------------------------------------------------------
# T033 test_connection 테스트
# ---------------------------------------------------------------------------
class TestConnectionTest:
    """T033: 연결 테스트 로직 (6단계)"""

    def _make_view(self, mock_cred=None):
        with patch("src.ui.settings_view.CredentialManager") as MockCred:
            if mock_cred:
                MockCred.return_value = mock_cred
            view = SettingsView()
        return view

    def test_test_connection_exists(self, qapp):
        view = self._make_view()
        assert callable(getattr(view, "test_connection", None))

    def test_test_connection_validates_empty_account(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_test_connection_validates_empty_api_key(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("1234567890")
        view.account_password.setText("pass")
        view.api_key.setText("")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_test_connection_calls_kiwoom_steps(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.return_value = None
        mock_kiwoom.login.return_value = True
        mock_kiwoom.get_account_list.return_value = ["1234567890"]

        view.account_number.setText("1234567890")
        view.account_password.setText("testpass")
        view.api_key.setText("testapikey")
        view.mock_app_key.setText("testappkey")

        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is True
        mock_kiwoom.connect.assert_called_once()

    def test_test_connection_emits_status_updates(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.return_value = None
        mock_kiwoom.login.return_value = True
        mock_kiwoom.get_account_list.return_value = ["1234567890"]

        statuses = []
        view.connection_status_changed.connect(lambda msg, step: statuses.append((msg, step)))

        view.account_number.setText("1234567890")
        view.account_password.setText("testpass")
        view.api_key.setText("testapikey")
        view.mock_app_key.setText("testappkey")
        view.test_connection(kiwoom=mock_kiwoom)

        assert len(statuses) >= 3

    def test_test_connection_login_failure(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.return_value = None
        mock_kiwoom.login.return_value = False

        view.account_number.setText("1234567890")
        view.account_password.setText("testpass")
        view.api_key.setText("testapikey")
        view.mock_app_key.setText("testappkey")

        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False


# ---------------------------------------------------------------------------
# T034 자격증명 저장/불러오기/삭제 테스트
# ---------------------------------------------------------------------------
class TestCredentials:
    """T034: keyring 저장/불러오기/삭제"""

    def test_save_credentials(self, qapp):
        mock_cred = MagicMock()
        with patch("src.ui.settings_view.CredentialManager", return_value=mock_cred):
            view = SettingsView()
            view.account_number.setText("1234567890")
            view.account_password.setText("pass123")
            view.api_key.setText("apikey123")
            view.save_credentials()

        mock_cred.save.assert_any_call("account_number", "1234567890")
        mock_cred.save.assert_any_call("account_password", "pass123")
        # api_key alias는 mock_api_key와 동일한 QLineEdit이므로 mock_api_key로 저장됨
        mock_cred.save.assert_any_call("mock_api_key", "apikey123")

    def test_save_credentials_all_four_keys(self, qapp):
        """4개 API 키 모두 저장 확인."""
        mock_cred = MagicMock()
        with patch("src.ui.settings_view.CredentialManager", return_value=mock_cred):
            view = SettingsView()
            view.live_api_key.setText("live_api")
            view.live_app_key.setText("live_app")
            view.mock_api_key.setText("mock_api")
            view.mock_app_key.setText("mock_app")
            view.save_credentials()

        mock_cred.save.assert_any_call("live_api_key", "live_api")
        mock_cred.save.assert_any_call("live_app_key", "live_app")
        mock_cred.save.assert_any_call("mock_api_key", "mock_api")
        mock_cred.save.assert_any_call("mock_app_key", "mock_app")

    def test_load_credentials(self, qapp):
        mock_cred = MagicMock()
        mock_cred.get.side_effect = lambda k: {
            "account_number": "9876543210",
            "account_password": "mypass",
            "live_api_key": "live_api",
            "live_app_key": "live_app",
            "mock_api_key": "mock_api",
            "mock_app_key": "mock_app",
        }.get(k)

        with patch("src.ui.settings_view.CredentialManager", return_value=mock_cred):
            view = SettingsView()
            view.load_credentials()

        assert view.account_number.text() == "9876543210"
        assert view.account_password.text() == "mypass"
        assert view.live_api_key.text() == "live_api"
        assert view.live_app_key.text() == "live_app"
        assert view.mock_api_key.text() == "mock_api"
        assert view.mock_app_key.text() == "mock_app"
        # alias 확인
        assert view.api_key.text() == "mock_api"

    def test_load_credentials_missing_key(self, qapp):
        mock_cred = MagicMock()
        mock_cred.get.return_value = None

        with patch("src.ui.settings_view.CredentialManager", return_value=mock_cred):
            view = SettingsView()
            view.load_credentials()

        assert view.account_number.text() == ""

    def test_clear_credentials(self, qapp):
        mock_cred = MagicMock()
        with patch("src.ui.settings_view.CredentialManager", return_value=mock_cred):
            view = SettingsView()
            view.clear_credentials()

        assert mock_cred.delete.call_count >= 6


# ---------------------------------------------------------------------------
# T035 실전투자 전환 재인증 테스트
# ---------------------------------------------------------------------------
class TestConfirmLiveMode:
    """T035: 실전투자 전환 재인증"""

    def test_confirm_live_mode_exists(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        assert callable(getattr(view, "confirm_live_mode", None))

    def test_confirm_live_mode_accepted(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        with patch("src.ui.settings_view.LiveModeDialog") as MockDialog:
            instance = MockDialog.return_value
            instance.exec.return_value = QDialog.DialogCode.Accepted
            instance.get_password.return_value = "correctpass"
            view.account_password.setText("correctpass")
            result = view.confirm_live_mode()
        assert result is True

    def test_confirm_live_mode_rejected(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        with patch("src.ui.settings_view.LiveModeDialog") as MockDialog:
            instance = MockDialog.return_value
            instance.exec.return_value = QDialog.DialogCode.Rejected
            result = view.confirm_live_mode()
        assert result is False

    def test_confirm_live_mode_wrong_password(self, qapp):
        with patch("src.ui.settings_view.CredentialManager"):
            view = SettingsView()
        with patch("src.ui.settings_view.LiveModeDialog") as MockDialog:
            instance = MockDialog.return_value
            instance.exec.return_value = QDialog.DialogCode.Accepted
            instance.get_password.return_value = "wrongpass"
            view.account_password.setText("correctpass")
            result = view.confirm_live_mode()
        assert result is False


# ---------------------------------------------------------------------------
# T036 에러 처리 테스트
# ---------------------------------------------------------------------------
class TestErrorHandling:
    """T036: 7가지 에러 시나리오"""

    def _make_view(self):
        with patch("src.ui.settings_view.CredentialManager"):
            return SettingsView()

    def test_error_empty_account_number(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("")
        view.account_password.setText("pass")
        view.api_key.setText("key")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_error_empty_password(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("1234567890")
        view.account_password.setText("")
        view.api_key.setText("key")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_error_empty_api_key(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("1234567890")
        view.account_password.setText("pass")
        view.api_key.setText("")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_error_invalid_account_format(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        view.account_number.setText("abc")
        view.account_password.setText("pass")
        view.api_key.setText("key")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_error_connection_failure(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.side_effect = ConnectionError("연결 실패")
        view.account_number.setText("1234567890")
        view.account_password.setText("pass")
        view.api_key.setText("key")
        view.mock_app_key.setText("appkey")
        with pytest.raises(ConnectionError):
            view.test_connection(kiwoom=mock_kiwoom)

    def test_error_login_failure(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.return_value = None
        mock_kiwoom.login.return_value = False
        view.account_number.setText("1234567890")
        view.account_password.setText("pass")
        view.api_key.setText("key")
        view.mock_app_key.setText("appkey")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False

    def test_error_account_not_found(self, qapp):
        view = self._make_view()
        mock_kiwoom = MagicMock()
        mock_kiwoom.connect.return_value = None
        mock_kiwoom.login.return_value = True
        mock_kiwoom.get_account_list.return_value = ["9999999999"]
        view.account_number.setText("1234567890")
        view.account_password.setText("pass")
        view.api_key.setText("key")
        view.mock_app_key.setText("appkey")
        result = view.test_connection(kiwoom=mock_kiwoom)
        assert result is False
