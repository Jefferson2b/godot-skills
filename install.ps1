[CmdletBinding()]
param(
    [string[]]$Skill = @(),
    [string]$Destination = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex\skills'),
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$sourceRoot = Join-Path $PSScriptRoot 'skills'
if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Skills directory not found: $sourceRoot"
}

$available = @(Get-ChildItem -LiteralPath $sourceRoot -Directory | Sort-Object Name)
if ($Skill.Count -gt 0) {
    $unknown = @($Skill | Where-Object { $_ -notin $available.Name })
    if ($unknown.Count -gt 0) {
        throw "Unknown skill(s): $($unknown -join ', '). Available: $($available.Name -join ', ')"
    }
    $selected = @($available | Where-Object { $_.Name -in $Skill })
}
else {
    $selected = $available
}

if ($selected.Count -eq 0) {
    throw 'No skills selected.'
}

$invalid = @($selected | Where-Object { -not (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf) })
if ($invalid.Count -gt 0) {
    throw "Invalid skill folder(s), missing SKILL.md: $($invalid.Name -join ', ')"
}

$conflicts = @($selected | Where-Object { Test-Path -LiteralPath (Join-Path $Destination $_.Name) })
if ($conflicts.Count -gt 0 -and -not $Force) {
    throw "Already installed: $($conflicts.Name -join ', '). Re-run with -Force to replace them."
}

New-Item -ItemType Directory -Path $Destination -Force | Out-Null
foreach ($item in $selected) {
    $target = Join-Path $Destination $item.Name
    if (Test-Path -LiteralPath $target) {
        $resolvedDestination = (Resolve-Path -LiteralPath $Destination).Path
        $resolvedTarget = (Resolve-Path -LiteralPath $target).Path
        if (-not $resolvedTarget.StartsWith($resolvedDestination + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to replace path outside destination: $resolvedTarget"
        }
        Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
    }
    Copy-Item -LiteralPath $item.FullName -Destination $target -Recurse
    Write-Host "Installed $($item.Name) -> $target"
}

Write-Host "Installed $($selected.Count) skill(s). Restart Codex to reload skills."
