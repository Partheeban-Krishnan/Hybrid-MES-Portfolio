
# =============================
# PowerShell Automation Script
# =============================
# Prerequisites:
# - FFmpeg installed and added to PATH
# - Python installed

# Step 1: Define paths
$DownloadsFolder = "$env:USERPROFILE\Downloads"
$VideoFile = Get-ChildItem -Path $DownloadsFolder -Filter *.mp4 | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $VideoFile) {
    Write-Host "No MP4 file found in Downloads folder." -ForegroundColor Red
    exit
}

Write-Host "Using video file: $($VideoFile.FullName)" -ForegroundColor Green

# Step 2: Create HLS output folder
$HLSFolder = "$DownloadsFolder\hls_output"
if (-not (Test-Path $HLSFolder)) {
    New-Item -ItemType Directory -Path $HLSFolder | Out-Null
}

# Step 3: Generate HLS using FFmpeg
Write-Host "Generating HLS segments..." -ForegroundColor Yellow
$FFmpegCommand = "ffmpeg -stream_loop -1 -re -i `"$($VideoFile.FullName)`" -c:v libx264 -f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments `"$HLSFolder\stream.m3u8`""
Invoke-Expression $FFmpegCommand

# Step 4: Start Python HTTP server
Write-Host "Starting HTTP server on port 8080..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$HLSFolder`"; python cors_server.py"

# Step 5: Output Grafana URL
$LocalIP = (Invoke-RestMethod -Uri "http://ipinfo.io/ip")
Write-Host "\nAdd this URL to Grafana Video Panel:" -ForegroundColor Cyan
Write-Host "http://$LocalIP:8080/stream.m3u8" -ForegroundColor Green
