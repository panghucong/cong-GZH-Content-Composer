# ============================================================================
# Pre-commit Hook (PowerShell): Auto-run version checker + test suite
# 公众号内容智能生成器 v8.5.0
#
# 安装方式（Windows Git Bash）:
#   cp scripts/pre-commit .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
# ============================================================================

Write-Host ""
Write-Host "🔍 公众号内容智能生成器 — Pre-commit 检查" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$SKILL_ROOT = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$PYTHON = (Get-Command python -ErrorAction SilentlyContinue).Source

if (-not $PYTHON) {
    Write-Host "⚠️  Python 不可用，跳过检查" -ForegroundColor Yellow
    exit 0
}

$PASS = $true

# 1. Version check
Write-Host ""
Write-Host "📋 [1/2] 版本一致性检查..." -ForegroundColor White
Write-Host "----------------------------------------"
$VERSION_CHECK = Join-Path $SKILL_ROOT "scripts/version_checker.py"
if (Test-Path $VERSION_CHECK) {
    & $PYTHON $VERSION_CHECK
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ 版本不一致！请修复后再提交。" -ForegroundColor Red
        $PASS = $false
    }
} else {
    Write-Host "⚠️  版本检查脚本不存在" -ForegroundColor Yellow
}

# 2. Test suite
Write-Host ""
Write-Host "🧪 [2/2] 测试套件..." -ForegroundColor White
Write-Host "----------------------------------------"
$TEST_RUNNER = Join-Path $SKILL_ROOT "tests/test_runner.py"
if (Test-Path $TEST_RUNNER) {
    & $PYTHON $TEST_RUNNER 2>&1 | Select-Object -Last 20
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ 测试失败！请修复后再提交。" -ForegroundColor Red
        $PASS = $false
    }
} else {
    Write-Host "⚠️  测试入口不存在" -ForegroundColor Yellow
}

# Final
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
if ($PASS) {
    Write-Host "✅ 所有检查通过！允许提交。" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ 检查未通过！提交被阻止。" -ForegroundColor Red
    Write-Host ""
    Write-Host "提示：" -ForegroundColor Yellow
    Write-Host "  - 只更新了内容但版本未同步？运行 python scripts/version_checker.py"
    Write-Host "  - 紧急跳过检查：git commit --no-verify"
    exit 1
}
