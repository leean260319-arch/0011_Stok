"""T096 최초 실행 설정 마법사 테스트
버전: v1.0
"""
import pytest

from src.ui.setup_wizard import SetupWizard


class TestSetupWizardCreation:
    """SetupWizard 생성 테스트."""

    def test_creation(self, qapp):
        """SetupWizard 인스턴스 생성."""
        wizard = SetupWizard()
        assert wizard is not None

    def test_initial_step_is_zero(self, qapp):
        """초기 단계는 0."""
        wizard = SetupWizard()
        assert wizard.current_step() == 0

    def test_is_qwidget(self, qapp):
        """QWidget 상속."""
        from PyQt6.QtWidgets import QWidget
        wizard = SetupWizard()
        assert isinstance(wizard, QWidget)


class TestSetupWizardNavigation:
    """SetupWizard 네비게이션 테스트."""

    def test_next_step(self, qapp):
        """다음 단계로 이동."""
        wizard = SetupWizard()
        wizard.next_step()
        assert wizard.current_step() == 1

    def test_prev_step(self, qapp):
        """이전 단계로 이동."""
        wizard = SetupWizard()
        wizard.next_step()
        wizard.prev_step()
        assert wizard.current_step() == 0

    def test_cannot_go_below_zero(self, qapp):
        """0단계 이하로 이동 불가."""
        wizard = SetupWizard()
        wizard.prev_step()
        assert wizard.current_step() == 0

    def test_cannot_exceed_max_step(self, qapp):
        """최대 단계 초과 불가."""
        wizard = SetupWizard()
        for _ in range(10):
            wizard.next_step()
        assert wizard.current_step() == 3

    def test_navigate_all_steps(self, qapp):
        """모든 단계 순회."""
        wizard = SetupWizard()
        for i in range(4):
            assert wizard.current_step() == i
            if i < 3:
                wizard.next_step()


class TestSetupWizardStep1:
    """1단계: 앱 비밀번호 설정 테스트."""

    def test_step1_has_password_fields(self, qapp):
        """1단계에 비밀번호 입력 필드 존재."""
        wizard = SetupWizard()
        data = wizard.get_step_data(0)
        assert "password" in data
        assert "password_confirm" in data

    def test_step1_password_default_empty(self, qapp):
        """1단계 비밀번호 기본값은 빈 문자열."""
        wizard = SetupWizard()
        data = wizard.get_step_data(0)
        assert data["password"] == ""
        assert data["password_confirm"] == ""


class TestSetupWizardStep2:
    """2단계: 키움 API 설정 테스트."""

    def test_step2_has_kiwoom_fields(self, qapp):
        """2단계에 키움 API 필드 존재."""
        wizard = SetupWizard()
        data = wizard.get_step_data(1)
        assert "account_number" in data
        assert "account_password" in data
        assert "api_key" in data

    def test_step2_defaults_empty(self, qapp):
        """2단계 기본값은 빈 문자열."""
        wizard = SetupWizard()
        data = wizard.get_step_data(1)
        assert data["account_number"] == ""
        assert data["account_password"] == ""
        assert data["api_key"] == ""


class TestSetupWizardStep3:
    """3단계: AI 설정 테스트."""

    def test_step3_has_ai_fields(self, qapp):
        """3단계에 AI API Key 필드 존재."""
        wizard = SetupWizard()
        data = wizard.get_step_data(2)
        assert "openai_api_key" in data
        assert "deepseek_api_key" in data

    def test_step3_defaults_empty(self, qapp):
        """3단계 기본값은 빈 문자열."""
        wizard = SetupWizard()
        data = wizard.get_step_data(2)
        assert data["openai_api_key"] == ""
        assert data["deepseek_api_key"] == ""


class TestSetupWizardStep4:
    """4단계: 매매 설정 테스트."""

    def test_step4_has_trade_fields(self, qapp):
        """4단계에 매매 설정 필드 존재."""
        wizard = SetupWizard()
        data = wizard.get_step_data(3)
        assert "daily_loss_limit" in data
        assert "max_position" in data
        assert "stop_loss" in data
        assert "take_profit" in data

    def test_step4_has_default_values(self, qapp):
        """4단계 기본값이 RiskDefaults와 일치."""
        from src.utils.constants import RiskDefaults
        wizard = SetupWizard()
        data = wizard.get_step_data(3)
        assert data["daily_loss_limit"] == RiskDefaults.DAILY_LOSS_LIMIT_PCT
        assert data["max_position"] == RiskDefaults.MAX_POSITION_PCT
        assert data["stop_loss"] == RiskDefaults.STOP_LOSS_PCT
        assert data["take_profit"] == RiskDefaults.TAKE_PROFIT_PCT


class TestSetupWizardCompletion:
    """SetupWizard 완료 테스트."""

    def test_not_complete_initially(self, qapp):
        """초기 상태에서 완료가 아님."""
        wizard = SetupWizard()
        assert wizard.is_complete() is False

    def test_complete_after_all_steps(self, qapp):
        """모든 단계를 거친 후 완료."""
        wizard = SetupWizard()
        for _ in range(3):
            wizard.next_step()
        assert wizard.current_step() == 3
        # 마지막 단계에 도달해도 is_complete는 완료 버튼 클릭 후
        assert wizard.is_complete() is False

    def test_has_wizard_completed_signal(self, qapp):
        """wizard_completed 시그널 존재."""
        wizard = SetupWizard()
        assert hasattr(wizard, "wizard_completed")

    def test_has_next_button(self, qapp):
        """다음 버튼 존재."""
        wizard = SetupWizard()
        assert wizard._next_button is not None

    def test_has_prev_button(self, qapp):
        """이전 버튼 존재."""
        wizard = SetupWizard()
        assert wizard._prev_button is not None

    def test_has_complete_button(self, qapp):
        """완료 버튼 존재."""
        wizard = SetupWizard()
        assert wizard._complete_button is not None
