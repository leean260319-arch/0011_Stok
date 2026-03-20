"""T084 AI 설정 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.ai_settings_view import AISettingsView
from src.utils.constants import LLMConfig


class TestAISettingsView:
    """AISettingsView 위젯 테스트."""

    def test_creation(self, qapp):
        """AISettingsView 인스턴스 생성."""
        view = AISettingsView()
        assert view is not None

    def test_primary_model_combo(self, qapp):
        """Primary 모델 선택 콤보박스."""
        view = AISettingsView()
        assert view._primary_model_combo.count() > 0

    def test_fallback_model_combo(self, qapp):
        """Fallback 모델 선택 콤보박스."""
        view = AISettingsView()
        assert view._fallback_model_combo.count() > 0

    def test_primary_api_key_password_mode(self, qapp):
        """Primary API Key 입력은 Password 모드."""
        from PyQt6.QtWidgets import QLineEdit
        view = AISettingsView()
        assert view._primary_api_key_edit.echoMode() == QLineEdit.EchoMode.Password

    def test_fallback_api_key_password_mode(self, qapp):
        """Fallback API Key 입력은 Password 모드."""
        from PyQt6.QtWidgets import QLineEdit
        view = AISettingsView()
        assert view._fallback_api_key_edit.echoMode() == QLineEdit.EchoMode.Password

    def test_has_test_button(self, qapp):
        """연결 테스트 버튼이 존재한다."""
        view = AISettingsView()
        assert view._test_button is not None
        assert "테스트" in view._test_button.text()

    def test_default_primary_model(self, qapp):
        """기본 Primary 모델은 GPT-4o-mini."""
        view = AISettingsView()
        assert "gpt-4o-mini" in view._primary_model_combo.currentText().lower()

    def test_default_fallback_model(self, qapp):
        """기본 Fallback 모델은 DeepSeek."""
        view = AISettingsView()
        text = view._fallback_model_combo.currentText().lower()
        assert "deepseek" in text
