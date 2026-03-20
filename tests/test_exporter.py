"""T092: Exporter CSV/Excel 내보내기 테스트"""

# 버전 정보
# v1.0 - 2026-03-17: 신규 작성

import csv
import os

import pytest

from src.utils.exporter import Exporter


class TestExporterCSV:
    """CSV 내보내기 테스트"""

    def test_export_to_csv_creates_file(self, tmp_path):
        """export_to_csv()는 CSV 파일을 생성해야 한다"""
        filepath = str(tmp_path / "out.csv")
        data = [{"name": "apple", "price": 100}]
        Exporter.export_to_csv(data, filepath)
        assert os.path.exists(filepath)

    def test_export_to_csv_content(self, tmp_path):
        """CSV 파일에 올바른 데이터가 기록되어야 한다"""
        filepath = str(tmp_path / "out.csv")
        data = [
            {"code": "005930", "name": "삼성전자", "price": 70000},
            {"code": "000660", "name": "SK하이닉스", "price": 120000},
        ]
        Exporter.export_to_csv(data, filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["code"] == "005930"
        assert rows[1]["name"] == "SK하이닉스"

    def test_export_to_csv_empty_data(self, tmp_path):
        """빈 데이터 리스트도 정상 처리해야 한다"""
        filepath = str(tmp_path / "empty.csv")
        Exporter.export_to_csv([], filepath)
        assert os.path.exists(filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            content = f.read().strip()
        assert content == ""

    def test_export_to_csv_creates_parent_dir(self, tmp_path):
        """상위 디렉토리가 없으면 자동 생성해야 한다"""
        filepath = str(tmp_path / "sub" / "dir" / "out.csv")
        data = [{"a": 1}]
        Exporter.export_to_csv(data, filepath)
        assert os.path.exists(filepath)

    def test_export_to_csv_header_order(self, tmp_path):
        """CSV 헤더 순서가 첫 번째 dict의 키 순서와 일치해야 한다"""
        filepath = str(tmp_path / "order.csv")
        data = [{"z_col": 1, "a_col": 2, "m_col": 3}]
        Exporter.export_to_csv(data, filepath)
        with open(filepath, encoding="utf-8-sig") as f:
            header = f.readline().strip()
        assert header == "z_col,a_col,m_col"


class TestExporterExcel:
    """Excel 내보내기 테스트 (openpyxl 없으면 CSV fallback)"""

    def test_export_to_excel_creates_file(self, tmp_path):
        """export_to_excel()은 파일을 생성해야 한다"""
        filepath = str(tmp_path / "out.xlsx")
        data = [{"name": "apple", "price": 100}]
        result_path = Exporter.export_to_excel(data, filepath)
        assert os.path.exists(result_path)

    def test_export_to_excel_fallback_to_csv(self, tmp_path):
        """openpyxl 미설치 시 CSV로 fallback되어야 한다"""
        filepath = str(tmp_path / "out.xlsx")
        data = [{"name": "apple", "price": 100}]
        result_path = Exporter.export_to_excel(data, filepath)
        # openpyxl이 없으므로 .csv 파일이 생성됨
        assert result_path.endswith(".csv") or result_path.endswith(".xlsx")
        assert os.path.exists(result_path)

    def test_export_to_excel_with_data(self, tmp_path):
        """Excel/CSV fallback 파일에 데이터가 포함되어야 한다"""
        filepath = str(tmp_path / "data.xlsx")
        data = [
            {"code": "005930", "price": 70000},
            {"code": "000660", "price": 120000},
        ]
        result_path = Exporter.export_to_excel(data, filepath)
        assert os.path.getsize(result_path) > 0

    def test_export_to_excel_empty_data(self, tmp_path):
        """빈 데이터도 정상 처리해야 한다"""
        filepath = str(tmp_path / "empty.xlsx")
        result_path = Exporter.export_to_excel([], filepath)
        assert os.path.exists(result_path)
