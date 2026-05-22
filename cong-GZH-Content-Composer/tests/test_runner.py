# -*- coding: utf-8 -*-
"""
测试套件主入口 - 运行所有测试用例
公众号内容智能生成器 v8.4.1

用法:
  pytest tests/test_runner.py -v
  python -m pytest tests/ -v
  python tests/test_runner.py          # 直接运行
"""
import subprocess
import sys
from pathlib import Path

# 技能根目录
SKILL_ROOT = Path(__file__).parent.parent.resolve()


def print_header():
    print("=" * 60)
    print("  公众号内容智能生成器 v8.4.1 - 测试套件")
    print("=" * 60)
    print(f"  技能根目录: {SKILL_ROOT}")
    print()


def run_tests():
    """运行所有测试模块"""
    test_files = [
        "tests/test_section_loading.py",
        "tests/test_compliance_scanner.py",
        "tests/test_scoring_consistency.py",
    ]

    all_passed = True
    results = {}

    for test_file in test_files:
        test_path = SKILL_ROOT / test_file
        if not test_path.exists():
            print(f"  ⚠️  跳过缺失文件: {test_file}")
            continue

        print(f"\n▶ 运行: {test_file}")
        print("-" * 40)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
            cwd=str(SKILL_ROOT),
            capture_output=False,
        )
        passed = result.returncode == 0
        results[test_file] = passed
        if not passed:
            all_passed = False

    return all_passed, results


def run_version_check():
    """运行版本一致性检查"""
    print("\n▶ 运行: scripts/version_checker.py")
    print("-" * 40)
    script_path = SKILL_ROOT / "scripts" / "version_checker.py"
    if not script_path.exists():
        print("  ⚠️  版本检查脚本不存在，跳过")
        return True

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(SKILL_ROOT),
        capture_output=False,
    )
    return result.returncode == 0


def print_summary(all_passed, results):
    """打印测试汇总"""
    print("\n" + "=" * 60)
    print("  测试汇总")
    print("=" * 60)

    for test_file, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {test_file}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n  通过率: {passed}/{total}")

    if all_passed:
        print("\n  🎉 所有测试通过！")
    else:
        print("\n  ❌ 有测试失败，请修复后重试。")

    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    print_header()

    # 尝试使用 pytest 运行（更规范的测试报告）
    try:
        import pytest
    except ImportError:
        print("⚠️  pytest 未安装，将使用内置测试逻辑")
        pytest = None

    if pytest is not None:
        all_passed, results = run_tests()
    else:
        # 降级：直接导入各测试模块
        sys.path.insert(0, str(SKILL_ROOT))
        all_passed, results = run_tests()

    # 版本一致性检查（不算入测试通过率，但必须通过）
    version_ok = run_version_check()

    final_passed = print_summary(all_passed, results)
    if not final_passed or not version_ok:
        sys.exit(1)
    else:
        sys.exit(0)
