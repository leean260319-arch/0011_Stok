"""T095 빌드 헬퍼 테스트
버전: v1.0
"""
import pytest

from src.utils.build_helper import BuildConfig, generate_spec_content, get_default_config


class TestBuildConfig:
    """BuildConfig 데이터 클래스 테스트."""

    def test_default_app_name(self):
        """기본 앱 이름은 StokAI."""
        config = BuildConfig()
        assert config.app_name == "StokAI"

    def test_default_one_file(self):
        """기본 one_file은 True."""
        config = BuildConfig()
        assert config.one_file is True

    def test_default_windowed(self):
        """기본 windowed는 True (콘솔 숨김)."""
        config = BuildConfig()
        assert config.windowed is True

    def test_default_icon_path(self):
        """기본 icon_path는 빈 문자열."""
        config = BuildConfig()
        assert config.icon_path == ""

    def test_default_hidden_imports(self):
        """기본 hidden_imports는 리스트."""
        config = BuildConfig()
        assert isinstance(config.hidden_imports, list)
        assert len(config.hidden_imports) > 0

    def test_default_extra_data(self):
        """기본 extra_data는 리스트."""
        config = BuildConfig()
        assert isinstance(config.extra_data, list)

    def test_custom_app_name(self):
        """커스텀 앱 이름 설정."""
        config = BuildConfig(app_name="MyApp")
        assert config.app_name == "MyApp"

    def test_custom_icon_path(self):
        """커스텀 아이콘 경로 설정."""
        config = BuildConfig(icon_path="icon.ico")
        assert config.icon_path == "icon.ico"

    def test_custom_hidden_imports(self):
        """커스텀 hidden_imports 설정."""
        config = BuildConfig(hidden_imports=["module_a", "module_b"])
        assert config.hidden_imports == ["module_a", "module_b"]

    def test_custom_extra_data(self):
        """커스텀 extra_data 설정."""
        data = [("data/config.json", "data")]
        config = BuildConfig(extra_data=data)
        assert config.extra_data == data


class TestGenerateSpecContent:
    """generate_spec_content 함수 테스트."""

    def test_returns_string(self):
        """spec 내용은 문자열."""
        config = BuildConfig()
        result = generate_spec_content(config)
        assert isinstance(result, str)

    def test_contains_app_name(self):
        """spec 내용에 앱 이름이 포함된다."""
        config = BuildConfig(app_name="TestApp")
        result = generate_spec_content(config)
        assert "TestApp" in result

    def test_contains_analysis(self):
        """spec 내용에 Analysis 블록이 포함된다."""
        config = BuildConfig()
        result = generate_spec_content(config)
        assert "Analysis" in result

    def test_contains_exe(self):
        """spec 내용에 EXE 블록이 포함된다."""
        config = BuildConfig()
        result = generate_spec_content(config)
        assert "EXE" in result

    def test_onefile_true(self):
        """one_file=True이면 onefile=True가 spec에 포함된다."""
        config = BuildConfig(one_file=True)
        result = generate_spec_content(config)
        assert "onefile=True" in result

    def test_onefile_false(self):
        """one_file=False이면 onefile=False가 spec에 포함된다."""
        config = BuildConfig(one_file=False)
        result = generate_spec_content(config)
        assert "onefile=False" in result

    def test_windowed_true(self):
        """windowed=True이면 console=False가 spec에 포함된다."""
        config = BuildConfig(windowed=True)
        result = generate_spec_content(config)
        assert "console=False" in result

    def test_windowed_false(self):
        """windowed=False이면 console=True가 spec에 포함된다."""
        config = BuildConfig(windowed=False)
        result = generate_spec_content(config)
        assert "console=True" in result

    def test_hidden_imports_in_spec(self):
        """hidden_imports가 spec에 포함된다."""
        config = BuildConfig(hidden_imports=["PyQt6", "sqlcipher3"])
        result = generate_spec_content(config)
        assert "PyQt6" in result
        assert "sqlcipher3" in result

    def test_icon_path_in_spec(self):
        """icon_path가 설정되면 spec에 포함된다."""
        config = BuildConfig(icon_path="assets/icon.ico")
        result = generate_spec_content(config)
        assert "assets/icon.ico" in result

    def test_extra_data_in_spec(self):
        """extra_data가 spec에 포함된다."""
        config = BuildConfig(extra_data=[("data/cfg.json", "data")])
        result = generate_spec_content(config)
        assert "data/cfg.json" in result


class TestGetDefaultConfig:
    """get_default_config 함수 테스트."""

    def test_returns_build_config(self):
        """BuildConfig 인스턴스를 반환한다."""
        config = get_default_config()
        assert isinstance(config, BuildConfig)

    def test_default_app_name_stokai(self):
        """기본 설정의 앱 이름은 StokAI."""
        config = get_default_config()
        assert config.app_name == "StokAI"

    def test_default_has_pyqt6_hidden_import(self):
        """기본 설정에 PyQt6 hidden import 포함."""
        config = get_default_config()
        assert "PyQt6" in config.hidden_imports

    def test_default_has_sqlcipher3_hidden_import(self):
        """기본 설정에 sqlcipher3 hidden import 포함."""
        config = get_default_config()
        assert "sqlcipher3" in config.hidden_imports
