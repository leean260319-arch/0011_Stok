"""T104 AI 상태 표시 테스트
버전: v1.0
"""
import pytest

from src.ui.widgets.ai_status_indicator import AIStatusIndicator


class TestAIStatusIndicator:
    """AIStatusIndicator 위젯 테스트."""

    def test_creation(self, qapp):
        """AIStatusIndicator 인스턴스 생성."""
        indicator = AIStatusIndicator()
        assert indicator is not None

    def test_default_status_idle(self, qapp):
        """기본 상태는 idle."""
        indicator = AIStatusIndicator()
        assert indicator._status == "idle"

    def test_set_status_processing(self, qapp):
        """processing 상태 설정."""
        indicator = AIStatusIndicator()
        indicator.set_status("processing")
        assert indicator._status == "processing"

    def test_set_status_complete(self, qapp):
        """complete 상태 설정."""
        indicator = AIStatusIndicator()
        indicator.set_status("complete")
        assert indicator._status == "complete"

    def test_set_status_error(self, qapp):
        """error 상태 설정."""
        indicator = AIStatusIndicator()
        indicator.set_status("error")
        assert indicator._status == "error"

    def test_status_text_changes(self, qapp):
        """상태 변경 시 텍스트도 변경된다."""
        indicator = AIStatusIndicator()
        indicator.set_status("processing")
        text = indicator._status_label.text()
        assert len(text) > 0

    def test_idle_text(self, qapp):
        """idle 상태의 텍스트."""
        indicator = AIStatusIndicator()
        indicator.set_status("idle")
        assert "대기" in indicator._status_label.text()

    def test_processing_shows_progress(self, qapp):
        """processing 상태에서 프로그레스바가 보인다."""
        indicator = AIStatusIndicator()
        indicator.set_status("processing")
        assert not indicator._progress_bar.isHidden()

    def test_idle_hides_progress(self, qapp):
        """idle 상태에서 프로그레스바가 숨겨진다."""
        indicator = AIStatusIndicator()
        indicator.set_status("idle")
        assert indicator._progress_bar.isHidden()
