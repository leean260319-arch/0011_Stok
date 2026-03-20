"""T097 자동 업데이트 확인 모듈
버전: v1.0
설명: GitHub releases API를 통한 버전 확인 및 업데이트 URL 생성
"""

import requests

from src.utils.constants import APP_VERSION
from src.utils.logger import get_logger

logger = get_logger("utils.updater")


class Updater:
    """자동 업데이트 확인 클래스."""

    def __init__(self, current_version: str = APP_VERSION):
        self.current_version = current_version

    def parse_version(self, version_str: str) -> tuple[int, ...]:
        """버전 문자열을 정수 튜플로 파싱한다. 'v' 접두사를 허용한다."""
        cleaned = version_str.lstrip("v")
        return tuple(int(part) for part in cleaned.split("."))

    def is_newer(self, remote: str, local: str) -> bool:
        """remote 버전이 local보다 높은지 비교한다."""
        remote_parts = self.parse_version(remote)
        local_parts = self.parse_version(local)
        return remote_parts > local_parts

    def get_update_url(self, tag: str) -> str:
        """GitHub releases URL을 생성한다."""
        return f"https://github.com/StokAI/StokAI/releases/tag/{tag}"

    def check_update(self, owner: str, repo: str) -> dict | None:
        """GitHub API를 호출하여 최신 릴리즈를 확인한다.

        반환: {"tag": "v0.2.0", "url": "...", "description": "..."} 또는 None
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logger.warning("업데이트 확인 실패: HTTP %d", response.status_code)
            return None

        data = response.json()
        tag = data.get("tag_name", "")
        html_url = data.get("html_url", "")
        body = data.get("body", "")

        if not self.is_newer(tag, self.current_version):
            return None

        return {
            "tag": tag,
            "url": html_url,
            "description": body,
        }
