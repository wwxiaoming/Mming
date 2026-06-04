@echo off
cd /d "%~dp0"
echo Stopping JZhu Trading...
:: compose down stops containers and releases their host-port bindings.
:: (Deliberately no taskkill on 18080/8180: on Docker Desktop those ports are
:: held by com.docker.backend.exe / vpnkit.exe, and killing that pid crashes
:: Docker Desktop itself.)
docker compose down 2>nul
echo Stopped.
pause
