"""T097 자동 업데이트 확인 테스트
버전: v1.0
"""
import pytest
from unittest.mock import patch, MagicMock

from src.utils.updater import Updater
from src.utils.constants import APP_VERSION


class TestUpdaterCreation:
    """Updater 생성 테스트."""

    def test_creation(self):
        """Updater 인스턴스 생성."""
        updater = Updater()
        assert updater is not None

    def test_current_version(self):
        """current_version은 APP_VERSION과 동일."""
        updater = Updater()
        assert updater.current_version == APP_VERSION

    def test_custom_version(self):
        """커스텀 버전 설정."""
        updater = Updater(current_version="1.2.3")
        assert updater.current_version == "1.2.3"


class TestParseVersion:
    """parse_version 메서드 테스트."""

    def test_parse_simple(self):
        """단순 버전 파싱."""
        updater = Updater()
        assert updater.parse_version("1.0.0") == (1, 0, 0)

    def test_parse_with_v_prefix(self):
        """v 접두사 버전 파싱."""
        updater = Updater()
        assert updater.parse_version("v1.2.3") == (1, 2, 3)

    def test_parse_two_parts(self):
        """2자리 버전 파싱."""
        updater = Updater()
        assert updater.parse_version("1.0") == (1, 0)

    def test_parse_four_parts(self):
        """4자리 버전 파싱."""
        updater = Updater()
        assert updater.parse_version("1.2.3.4") == (1, 2, 3, 4)

    def test_parse_app_version(self):
        """APP_VERSION 파싱."""
        updater = Updater()
        result = updater.parse_version(APP_VERSION)
        assert isinstance(result, tuple)
        assert all(isinstance(v, int) for v in result)


class TestIsNewer:
    """is_newer 메서드 테스트."""

    def test_newer_major(self):
        """major 버전이 높으면 newer."""
        updater = Updater()
        assert updater.is_newer("2.0.0", "1.0.0") is True

    def test_newer_minor(self):
        """minor 버전이 높으면 newer."""
        updater = Updater()
        assert updater.is_newer("1.1.0", "1.0.0") is True

    def test_newer_patch(self):
        """patch 버전이 높으면 newer."""
        updater = Updater()
        assert updater.is_newer("1.0.1", "1.0.0") is True

    def test_same_version(self):
        """동일 버전은 newer가 아님."""
        updater = Updater()
        assert updater.is_newer("1.0.0", "1.0.0") is False

    def test_older_version(self):
        """낮은 버전은 newer가 아님."""
        updater = Updater()
        assert updater.is_newer("0.9.0", "1.0.0") is False

    def test_with_v_prefix(self):
        """v 접두사가 있어도 정상 비교."""
        updater = Updater()
        assert updater.is_newer("v1.1.0", "v1.0.0") is True

    def test_different_length(self):
        """길이가 다른 버전 비교."""
        updater = Updater()
        assert updater.is_newer("1.0.1", "1.0") is True


class TestGetUpdateUrl:
    """get_update_url 메서드 테스트."""

    def test_returns_github_url(self):
        """GitHub releases URL 반환."""
        updater = Updater()
        url = updater.get_update_url("v0.2.0")
        assert "github.com" in url
        assert "v0.2.0" in url

    def test_url_contains_releases(self):
        """URL에 releases 경로 포함."""
        updater = Updater()
        url = updater.get_update_url("v1.0.0")
        assert "releases" in url


class TestCheckUpdate:
    """check_update 메서드 테스트 (mock)."""

    def test_returns_none_when_no_update(self):
        """업데이트 없으면 None 반환."""
        updater = Updater(current_version="99.99.99")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v0.1.0",
            "html_url": "https://github.com/owner/repo/releases/tag/v0.1.0",
            "body": "Initial release",
        }
        with patch("src.utils.updater.requests.get", return_value=mock_response):
            result = updater.check_update("owner", "repo")
        assert result is None

    def test_returns_dict_when_update_available(self):
        """업데이트 있으면 dict 반환."""
        updater = Updater(current_version="0.1.0")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v0.2.0",
            "html_url": "https://github.com/owner/repo/releases/tag/v0.2.0",
            "body": "New features",
        }
        with patch("src.utils.updater.requests.get", return_value=mock_response):
            result = updater.check_update("owner", "repo")
        assert result is not None
        assert result["tag"] == "v0.2.0"
        assert "url" in result
        assert "description" in result

    def test_returns_none_on_api_error(self):
        """API 오류 시 None 반환."""
        updater = Updater()
        mock_response = MagicMock()
        mock_response.status_code = 404
        with patch("src.utils.updater.requests.get", return_value=mock_response):
            result = updater.check_update("owner", "repo")
        assert result is None
