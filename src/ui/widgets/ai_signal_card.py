"""T103 AI 시그널 카드 위젯
버전: v1.0
설명: AI 매매 시그널(buy/sell/hold)과 신뢰도, 근거를 표시하는 카드
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QVBoxLayout

from src.utils.constants import Colors

# 시그널 타입별 색상 매핑
_SIGNAL_COLORS = {
    "buy": Colors.BULLISH,
    "sell": Colors.BEARISH,
    "hold": Colors.TEXT_SECONDARY,
}

_SIGNAL_LABELS = {
    "buy": "BUY (매수)",
    "sell": "SELL (매도)",
    "hold": "HOLD (관망)",
}


class AISignalCard(QFrame):
    """AI 매매 시그널 표시 카드 위젯."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._signal_type: str = ""
        self._confidence: float = 0.0
        self._reasoning: str = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        """UI 초기화."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"AISignalCard {{"
            f"  background-color: {Colors.SURFACE};"
            f"  border-radius: 8px;"
            f"  border: 1px solid {Colors.BORDER};"
            f"}}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # 시그널 타입 라벨
        self._signal_label = QLabel("--")
        self._signal_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; background: transparent; border: none;"
        )
        self._signal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._signal_label)

        # 신뢰도 게이지
        self._gauge = QProgressBar()
        self._gauge.setRange(0, 100)
        self._gauge.setValue(0)
        self._gauge.setTextVisible(True)
        self._gauge.setFormat("%v%")
        self._gauge.setFixedHeight(20)
        layout.addWidget(self._gauge)

        # 근거 텍스트
        self._reasoning_label = QLabel("")
        self._reasoning_label.setWordWrap(True)
        self._reasoning_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;"
            "background: transparent; border: none;"
        )
        layout.addWidget(self._reasoning_label)

    def set_signal(self, signal_type: str, confidence: float, reasoning: str) -> None:
        """시그널 정보를 설정한다.

        Args:
            signal_type: "buy", "sell", "hold"
            confidence: 0.0 ~ 1.0
            reasoning: 근거 텍스트
        """
        self._signal_type = signal_type
        self._confidence = confidence
        self._reasoning = reasoning

        color = _SIGNAL_COLORS.get(signal_type, Colors.TEXT_SECONDARY)
        label = _SIGNAL_LABELS.get(signal_type, signal_type.upper())

        self._signal_label.setText(label)
        self._signal_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {color};"
            "background: transparent; border: none;"
        )

        pct = int(confidence * 100)
        self._gauge.setValue(pct)
        self._gauge.setStyleSheet(
            f"QProgressBar {{ background-color: {Colors.SURFACE_VARIANT};"
            f"  border-radius: 4px; border: none; text-align: center;"
            f"  color: {Colors.TEXT_PRIMARY}; }}"
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 4px; }}"
        )

        self._reasoning_label.setText(reasoning)
