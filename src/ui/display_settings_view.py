"""화면 설정 - UI 크기 및 폰트 크기 조절"""

# 버전 정보
# v1.0 - 2026-03-17: 신규 작성

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QSpinBox, QComboBox, QPushButton, QFormLayout
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from src.utils.constants import Colors
from src.utils.logger import get_logger

logger = get_logger("display_settings")


class DisplaySettingsView(QWidget):
    """화면 설정 위젯 - 폰트 크기, UI 스케일 조절"""
    settings_changed = pyqtSignal()  # 설정 변경 시그널

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # --- 폰트 크기 ---
        font_group = QGroupBox("폰트 크기")
        font_layout = QFormLayout(font_group)

        self.font_spin = QSpinBox()
        self.font_spin.setRange(8, 24)
        self.font_spin.setValue(12)
        self.font_spin.setSuffix(" px")
        self.font_spin.valueChanged.connect(self._update_preview)
        font_layout.addRow("글꼴 크기:", self.font_spin)

        # 프리셋 버튼
        preset_layout = QHBoxLayout()
        for name, size in [("작게", 10), ("보통", 12), ("크게", 14), ("매우 크게", 16)]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, s=size: self.font_spin.setValue(s))
            preset_layout.addWidget(btn)
        font_layout.addRow("프리셋:", preset_layout)

        layout.addWidget(font_group)

        # --- UI 스케일 ---
        scale_group = QGroupBox("UI 스케일")
        scale_layout = QFormLayout(scale_group)

        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["75%", "100%", "125%", "150%", "200%"])
        self.scale_combo.setCurrentText("100%")
        self.scale_combo.currentTextChanged.connect(self._update_preview)
        scale_layout.addRow("화면 배율:", self.scale_combo)

        layout.addWidget(scale_group)

        # --- 미리보기 ---
        preview_group = QGroupBox("미리보기")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_label = QLabel("가나다라마바사 ABCDEFG 0123456789\n주식 자동매매 StokAI - 미리보기 텍스트")
        self.preview_label.setWordWrap(True)
        preview_layout.addWidget(self.preview_label)

        layout.addWidget(preview_group)

        # --- 단축키 안내 ---
        shortcut_group = QGroupBox("단축키")
        shortcut_layout = QFormLayout(shortcut_group)
        shortcut_layout.addRow("확대:", QLabel("Ctrl + ="))
        shortcut_layout.addRow("축소:", QLabel("Ctrl + -"))
        shortcut_layout.addRow("기본 크기:", QLabel("Ctrl + 0"))
        layout.addWidget(shortcut_group)

        # --- 적용 버튼 ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.apply_btn = QPushButton("적용")
        self.apply_btn.clicked.connect(self._on_apply)
        btn_layout.addWidget(self.apply_btn)
        layout.addLayout(btn_layout)

        layout.addStretch()

    def _update_preview(self):
        """미리보기 라벨의 폰트를 갱신한다."""
        size = self.font_spin.value()
        font = QFont("Malgun Gothic", size)
        self.preview_label.setFont(font)

    def get_font_size(self) -> int:
        return self.font_spin.value()

    def get_ui_scale(self) -> int:
        text = self.scale_combo.currentText().replace("%", "")
        return int(text)

    def set_font_size(self, size: int):
        self.font_spin.setValue(size)

    def set_ui_scale(self, scale: int):
        self.scale_combo.setCurrentText(f"{scale}%")

    def _on_apply(self):
        self.settings_changed.emit()
