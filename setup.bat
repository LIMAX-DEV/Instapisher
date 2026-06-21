@echo off
title Cloudflare Installer

echo BAIXANDO CLOUDFLARE...
echo.

if %PROCESSOR_ARCHITECTURE%==AMD64 (
    powershell -command "Invoke-WebRequest 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -Outfile 'cloudflare.exe'"
)
if %PROCESSOR_ARCHITECTURE%==x86 (
    powershell -command "Invoke-WebRequest 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe' -Outfile 'cloudflare.exe'"
)

if exist cloudflare.exe (
    echo.
    echo CLOUDFLARE BAIXADO COM SUCESSO!
) else (
    echo.
    echo ERRO AO BAIXAR!
)

pause