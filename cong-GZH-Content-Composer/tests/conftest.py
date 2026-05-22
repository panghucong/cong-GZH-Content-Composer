# -*- coding: utf-8 -*-
"""
pytest 配置和公共 Fixtures
公众号内容智能生成器 v8.4.1
"""
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def skill_root():
    """技能根目录"""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def sections_dir(skill_root):
    """sections/ 目录"""
    return skill_root / "sections"


@pytest.fixture(scope="session")
def compliance_dir(skill_root):
    """compliance/ 目录"""
    return skill_root / "compliance"


@pytest.fixture(scope="session")
def profiles_dir(skill_root):
    """profiles/ 目录"""
    return skill_root / "profiles"


@pytest.fixture(scope="session")
def templates_dir(skill_root):
    """templates/ 目录"""
    return skill_root / "templates"


@pytest.fixture(scope="session")
def shared_definitions(skill_root):
    """shared-definitions.md 内容"""
    path = skill_root / "shared-definitions.md"
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def skill_md(skill_root):
    """SKILL.md 内容"""
    path = skill_root / "SKILL.md"
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def changelog_md(skill_root):
    """CHANGELOG.md 内容"""
    path = skill_root / "CHANGELOG.md"
    return path.read_text(encoding="utf-8")


def pytest_configure(config):
    """pytest 启动时的全局配置"""
    config.addinivalue_line("markers", "section: section文件相关测试")
    config.addinivalue_line("markers", "compliance: 合规词库相关测试")
    config.addinivalue_line("markers", "scoring: 评分体系相关测试")
    config.addinivalue_line("markers", "version: 版本一致性测试")
