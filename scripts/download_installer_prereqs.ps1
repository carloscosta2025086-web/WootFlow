param(
    [switch]$Force,
    [string]$WebView2StandaloneUrl = "",
    [switch]$IncludeBootstrapper = $true
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$prereqDir = Join-Path $repoRoot "installer\prereqs"
New-Item -ItemType Directory -Path $prereqDir -Force | Out-Null

function Download-IfNeeded {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if ((-not $Force) -and (Test-Path $Destination)) {
        Write-Host "Ja existe: $Destination" -ForegroundColor Yellow
        return
    }

    Write-Host "A transferir: $Url" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $Url -OutFile $Destination
    Write-Host "Guardado em: $Destination" -ForegroundColor Green
}

$vcRedistPath = Join-Path $prereqDir "vc_redist.x64.exe"
Download-IfNeeded -Url "https://aka.ms/vc14/vc_redist.x64.exe" -Destination $vcRedistPath

if ($WebView2StandaloneUrl) {
    $standalonePath = Join-Path $prereqDir "MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
    Download-IfNeeded -Url $WebView2StandaloneUrl -Destination $standalonePath
} elseif ($IncludeBootstrapper) {
    $bootstrapperPath = Join-Path $prereqDir "MicrosoftEdgeWebView2Setup.exe"
    Download-IfNeeded -Url "https://go.microsoft.com/fwlink/p/?LinkId=2124703" -Destination $bootstrapperPath
    Write-Host "WebView2 bootstrapper incluído. Para setup 100% offline, substitui por MicrosoftEdgeWebView2RuntimeInstallerX64.exe em installer/prereqs/." -ForegroundColor Yellow
} else {
    Write-Host "WebView2 não foi transferido. Coloca manualmente o instalador offline em installer/prereqs/ se precisares de media 100% offline." -ForegroundColor Yellow
}
