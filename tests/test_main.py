"""T013: main.py 진입점 테스트"""
import pytest
from PyQt6.QtWidgets import QApplication


class TestCreateApp:
    """create_app() 함수 테스트"""

    def test_create_app_returns_qapplication(self, qapp):
        """create_app()이 QApplication 인스턴스를 반환해야 한다"""
        from src.main import create_app
        app = create_app()
        assert isinstance(app, QApplication)

    def test_create_app_reuses_existing_instance(self, qapp):
        """이미 QApplication이 있을 때 기존 인스턴스를 반환해야 한다"""
        from src.main import create_app
        app1 = create_app()
        app2 = create_app()
        assert app1 is app2

    def test_main_function_exists(self):
        """main() 함수가 존재해야 한다"""
        from src.main import main
        assert callable(main)
