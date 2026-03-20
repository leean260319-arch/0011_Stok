"""T095 PyInstaller 빌드 설정 헬퍼 모듈
버전: v1.0
설명: PyInstaller .spec 파일 생성을 위한 설정 관리 (실제 빌드 실행은 하지 않음)
"""

from dataclasses import dataclass, field

from src.utils.constants import APP_NAME


@dataclass
class BuildConfig:
    """PyInstaller 빌드 설정 데이터 클래스."""

    app_name: str = APP_NAME
    one_file: bool = True
    windowed: bool = True
    icon_path: str = ""
    hidden_imports: list[str] = field(default_factory=lambda: [
        "PyQt6",
        "sqlcipher3",
        "keyring",
        "grpcio",
        "google.protobuf",
    ])
    extra_data: list[tuple[str, str]] = field(default_factory=list)


def generate_spec_content(config: BuildConfig) -> str:
    """BuildConfig를 기반으로 .spec 파일 내용 문자열을 생성한다."""
    hidden_imports_str = ", ".join(f"'{h}'" for h in config.hidden_imports)

    datas_str = ""
    if config.extra_data:
        datas_items = ", ".join(
            f"('{src}', '{dst}')" for src, dst in config.extra_data
        )
        datas_str = f"    datas=[{datas_items}],\n"
    else:
        datas_str = "    datas=[],\n"

    icon_str = f"'{config.icon_path}'" if config.icon_path else "None"
    console_str = "False" if config.windowed else "True"
    onefile_str = "True" if config.one_file else "False"

    spec = f"""# -*- mode: python ; coding: utf-8 -*-
# {config.app_name} PyInstaller spec 파일 (자동 생성)

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
{datas_str}    hiddenimports=[{hidden_imports_str}],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries if {onefile_str} else [],
    a.datas if {onefile_str} else [],
    [],
    name='{config.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console_str},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={icon_str},
    onefile={onefile_str},
)
"""
    return spec


def get_default_config() -> BuildConfig:
    """기본 빌드 설정을 반환한다."""
    return BuildConfig()
