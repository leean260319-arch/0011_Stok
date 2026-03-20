"""T083 토스트 알림 테스트
버전: v1.0
"""
import pytest

from src.ui.widgets.toast_notification import ToastNotification


class TestToastNotification:
    """ToastNotification 위젯 테스트."""

    def test_creation(self, qapp):
        """ToastNotification 인스턴스 생성."""
        toast = ToastNotification()
        assert toast is not None

    def test_show_toast_info(self, qapp):
        """info 타입 토스트."""
        toast = ToastNotification()
        toast.show_toast("정보 메시지", toast_type="info")
        assert toast._message_label.text() == "정보 메시지"
        assert toast._toast_type == "info"

    def test_show_toast_warning(self, qapp):
        """warning 타입 토스트."""
        toast = ToastNotification()
        toast.show_toast("경고 메시지", toast_type="warning")
        assert toast._toast_type == "warning"

    def test_show_toast_error(self, qapp):
        """error 타입 토스트."""
        toast = ToastNotification()
        toast.show_toast("에러 메시지", toast_type="error")
        assert toast._toast_type == "error"

    def test_default_duration(self, qapp):
        """기본 지속 시간은 3000ms."""
        toast = ToastNotification()
        toast.show_toast("테스트")
        assert toast._duration_ms == 3000

    def test_custom_duration(self, qapp):
        """커스텀 지속 시간."""
        toast = ToastNotification()
        toast.show_toast("테스트", duration_ms=5000)
        assert toast._duration_ms == 5000

    def test_default_type_info(self, qapp):
        """기본 타입은 info."""
        toast = ToastNotification()
        toast.show_toast("테스트")
        assert toast._toast_type == "info"
