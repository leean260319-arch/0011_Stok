"""T085 매매 설정 뷰 테스트
버전: v1.0
"""
import pytest

from src.ui.trade_settings_view import TradeSettingsView
from src.utils.constants import RiskDefaults


class TestTradeSettingsView:
    """TradeSettingsView 위젯 테스트."""

    def test_creation(self, qapp):
        """TradeSettingsView 인스턴스 생성."""
        view = TradeSettingsView()
        assert view is not None

    def test_default_daily_loss_limit(self, qapp):
        """기본 일일 손실 한도 = 3.0%."""
        view = TradeSettingsView()
        assert view._daily_loss_spin.value() == RiskDefaults.DAILY_LOSS_LIMIT_PCT

    def test_default_max_position(self, qapp):
        """기본 최대 포지션 = 20.0%."""
        view = TradeSettingsView()
        assert view._max_position_spin.value() == RiskDefaults.MAX_POSITION_PCT

    def test_default_stop_loss(self, qapp):
        """기본 손절 = 2.0%."""
        view = TradeSettingsView()
        assert view._stop_loss_spin.value() == RiskDefaults.STOP_LOSS_PCT

    def test_default_take_profit(self, qapp):
        """기본 이익 실현 = 5.0%."""
        view = TradeSettingsView()
        assert view._take_profit_spin.value() == RiskDefaults.TAKE_PROFIT_PCT

    def test_spin_boxes_are_double(self, qapp):
        """스핀박스는 QDoubleSpinBox."""
        from PyQt6.QtWidgets import QDoubleSpinBox
        view = TradeSettingsView()
        assert isinstance(view._daily_loss_spin, QDoubleSpinBox)
        assert isinstance(view._max_position_spin, QDoubleSpinBox)
        assert isinstance(view._stop_loss_spin, QDoubleSpinBox)
        assert isinstance(view._take_profit_spin, QDoubleSpinBox)

    def test_has_save_button(self, qapp):
        """저장 버튼이 존재한다."""
        view = TradeSettingsView()
        assert view._save_button is not None

    def test_has_load_button(self, qapp):
        """불러오기 버튼이 존재한다."""
        view = TradeSettingsView()
        assert view._load_button is not None
