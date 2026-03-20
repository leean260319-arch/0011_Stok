"""pytest 공통 픽스처 설정"""
import os
import sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"

# kiwoom_pb2_grpc.py가 'import kiwoom_pb2'(절대 임포트)를 사용하므로
# src.bridge.kiwoom_pb2를 kiwoom_pb2 이름으로 먼저 등록한 뒤 grpc 스텁 임포트
import src.bridge.kiwoom_pb2 as _kiwoom_pb2
sys.modules.setdefault("kiwoom_pb2", _kiwoom_pb2)

import src.bridge.kiwoom_pb2_grpc as _kiwoom_pb2_grpc
sys.modules.setdefault("kiwoom_pb2_grpc", _kiwoom_pb2_grpc)

import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app
