"""T092: 데이터 내보내기 - CSV/Excel 내보내기 유틸리티"""

# 버전 정보
# v1.0 - 2026-03-17: 신규 작성
#   - CSV 내보내기 (csv 모듈)
#   - Excel 내보내기 (openpyxl 사용, 미설치 시 CSV fallback)

import csv
import os

from src.utils.logger import get_logger

logger = get_logger("utils.exporter")


class Exporter:
    """매매 이력, 분석 결과 등을 CSV/Excel로 내보내는 유틸리티 클래스."""

    @staticmethod
    def export_to_csv(data: list[dict], filepath: str) -> None:
        """dict 리스트를 CSV 파일로 내보낸다.

        Args:
            data: 내보낼 데이터 (dict 리스트)
            filepath: 저장할 CSV 파일 경로
        """
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            if not data:
                return
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        logger.info("CSV 내보내기 완료: %s (%d건)", filepath, len(data))

    @staticmethod
    def export_to_excel(data: list[dict], filepath: str) -> str:
        """dict 리스트를 Excel 파일로 내보낸다. openpyxl 미설치 시 CSV로 fallback한다.

        Args:
            data: 내보낼 데이터 (dict 리스트)
            filepath: 저장할 Excel 파일 경로

        Returns:
            실제 저장된 파일 경로 (fallback 시 .csv 확장자)
        """
        # openpyxl 사용 시도
        _has_openpyxl = False
        try:
            import openpyxl
            _has_openpyxl = True
        except ImportError:
            pass

        if _has_openpyxl:
            import openpyxl

            dir_path = os.path.dirname(filepath)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            wb = openpyxl.Workbook()
            ws = wb.active
            if data:
                headers = list(data[0].keys())
                ws.append(headers)
                for row in data:
                    ws.append([row.get(h) for h in headers])
            wb.save(filepath)
            logger.info("Excel 내보내기 완료: %s (%d건)", filepath, len(data))
            return filepath

        # CSV fallback
        csv_path = os.path.splitext(filepath)[0] + ".csv"
        logger.info("openpyxl 미설치 - CSV로 fallback: %s", csv_path)
        Exporter.export_to_csv(data, csv_path)
        return csv_path
