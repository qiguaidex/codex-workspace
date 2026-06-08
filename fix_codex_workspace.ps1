# Codex 工作区修复脚本
# 用法：完全退出 Codex → 右键此文件 → "使用 PowerShell 运行"
# 或在终端执行：powershell -ExecutionPolicy Bypass -File fix_codex_workspace.ps1

$jsonPath = "$env:USERPROFILE\.codex\.codex-global-state.json"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Codex 工作区修复脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 备份
$bakPath = $jsonPath + ".manual-bak"
Copy-Item $jsonPath $bakPath -Force
Write-Host "[1/3] 已备份" -ForegroundColor Green

# 2. 更新 JSON
Write-Host "[2/3] 更新工作区配置..." -ForegroundColor Yellow
$json = Get-Content $jsonPath -Raw -Encoding UTF8 | ConvertFrom-Json

$newRoots = @(
    "D:\workspace",
    "D:\workspace\Projects-01-个人助理",
    "D:\workspace\Projects-02-抖音运营",
    "D:\workspace\Projects-03-微信发卷",
    "D:\workspace\Projects-04-早期探索"
)

$json.'electron-saved-workspace-roots' = $newRoots
$json.'project-order' = $newRoots
$json.'active-workspace-roots' = @("D:\workspace")

# 线程归属映射
# 格式: 线程ID = 工作区路径
$threadMap = @{
    # === Projects-00 工作区管理 ===
    "019ea5ae-9af2-77a3-9337-ab409dab9322" = "D:\workspace"  # 当前对话（工作区整理）
    "019e8be7-a220-7ae2-a953-fd68b7f006c3" = "D:\workspace"  # 上下文窗口扩展到105万
    "019e9162-d499-7960-baf1-e3c42d5dd469" = "D:\workspace"  # 上下文调整+自查
    "019e91d7-79ac-7982-b9e8-bf47dc5ffbd3" = "D:\workspace"  # 插件灰色不可用
    "019e95a6-659e-70d1-bd2e-425e2151dfb8" = "D:\workspace"  # 最大化显示不全
    "019e95be-9a55-7e71-9bae-163b527b8e09" = "D:\workspace"  # 边框透明化
    "019e9f57-f397-7cd2-be58-99987e793e7c" = "D:\workspace"  # 管理员方式运行
    "019ea491-5a50-78b1-8e4f-7b3716ba13a9" = "D:\workspace"  # coze api问题

    # === Projects-01 个人助理 ===
    "019e91d2-5839-71c1-b72b-978506b13ed6" = "D:\workspace\Projects-01-个人助理"  # 能力梳理
    "019e965b-32ed-72d3-895a-1005ffd0f9f4" = "D:\workspace\Projects-01-个人助理"  # 元域AI技能
    "019e95d9-3385-7512-9606-64fd8127a81e" = "D:\workspace\Projects-01-个人助理"  # 剧本分镜
    "019e9622-95b2-7682-ad06-9853f7277719" = "D:\workspace\Projects-01-个人助理"  # coze脚本
    "019e9632-28f1-7251-9976-8d95312fe27f" = "D:\workspace\Projects-01-个人助理"  # 飞书机器人
    "019e91fc-92b0-7583-831f-98caedcf9fee" = "D:\workspace\Projects-01-个人助理"  # 技能中文备注

    # === Projects-02 抖音运营 ===
    "019ea0a1-9509-7193-891e-830d74902b33" = "D:\workspace\Projects-02-抖音运营"  # 抖音运营网页

    # === Projects-03 微信发卷 ===
    "019e929f-72df-7d91-8e30-801cff28a19a" = "D:\workspace\Projects-03-微信发卷"  # 定时发卷

    # === Projects-04 早期探索 ===
    "019e914d-5387-7891-aaca-fc6dfaa62392" = "D:\workspace\Projects-04-早期探索"  # 网页制作
}

$json.'thread-workspace-root-hints' = $threadMap

# 从 projectless 中移除所有已归类的线程
$pl = [System.Collections.ArrayList]($json.'projectless-thread-ids')
foreach ($tid in $threadMap.Keys) {
    $pl.Remove($tid)
}
# 仅保留 3 个问候测试对话为 projectless
$json.'projectless-thread-ids' = $pl

$json | ConvertTo-Json -Depth 10 -Compress | Set-Content $jsonPath -Encoding UTF8 -NoNewline
Write-Host "       5 个工作区, $($threadMap.Count) 个线程已归类" -ForegroundColor Green

# 3. 清理旧目录
Write-Host "[3/3] 清理旧目录..." -ForegroundColor Yellow
@("D:\Documents\Aghet","D:\Documents\kehu","D:\Documents\WORK","D:\Documents\juanzi","D:\Documents\New project") | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item $_ -Recurse -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path $_)) { Write-Host "       已删除: $_" -ForegroundColor Gray }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  修复完成！请重新启动 Codex" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "启动后左侧应出现 5 个工作区：" -ForegroundColor White
Write-Host "  workspace           ← 8个对话（配置维护类）" -ForegroundColor White
Write-Host "  Projects-01-个人助理  ← 6个对话" -ForegroundColor White
Write-Host "  Projects-02-抖音运营   ← 1个对话" -ForegroundColor White
Write-Host "  Projects-03-微信发卷   ← 1个对话" -ForegroundColor White
Write-Host "  Projects-04-早期探索   ← 1个对话" -ForegroundColor White
Write-Host ""
Write-Host "另有 3 个问候测试对话保留为「无项目」" -ForegroundColor DarkGray

Read-Host "`n按回车键退出"
