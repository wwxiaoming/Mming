@echo off
cd /d "%~dp0"
echo Restarting JZhu Trading...
echo.

:: Locate PowerShell. Some users have PATH stripped of the WindowsPowerShell\v1.0
:: entry (Anaconda installer / PATH-editor tools do this). Try pwsh, powershell,
:: then absolute path. Empty PS_EXE = PowerShell-dependent steps are skipped,
:: NOT a startup blocker.
set "PS_EXE="
where pwsh >nul 2>nul && set "PS_EXE=pwsh"
if not defined PS_EXE (
    where powershell >nul 2>nul && set "PS_EXE=powershell"
)
if not defined PS_EXE (
    if exist "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
)

:: Pre-flight: path must only contain safe characters.
:: Uses PowerShell because batch pipes break on Chinese GBK encoding.
:: PCHK: 0=ok, 2=space, 3=non-ascii, anything else=check skipped (PS unavailable).
:: An unavailable PowerShell must NOT be misreported as a bad path - this was a real bug.
set "PCHK=255"
if defined PS_EXE %PS_EXE% -NoProfile -Command "$p=(Get-Location).Path; if($p -match ' '){exit 2}; if($p -match '[^a-zA-Z0-9:\\._ -]'){exit 3}; exit 0" >nul 2>nul
if defined PS_EXE set "PCHK=%errorlevel%"
if "%PCHK%"=="2" goto :BAD_PATH_SPACE
if "%PCHK%"=="3" goto :BAD_PATH_NONASCII
if not "%PCHK%"=="0" echo [Warn] Path safety check skipped, PowerShell unavailable ^(code=%PCHK%^).

:: ---------------------------------------------------------------
:: WinNAT port reservation check.
:: Windows Hyper-V / WSL2 randomly grabs dynamic port ranges at boot.
:: A "worked yesterday, fails today" install usually means 8180 fell
:: into a freshly-grabbed range. Symptom in docker compose up:
::   bind: An attempt was made to access a socket in a way forbidden
:: Fix: permanently exclude our ports so WinNAT skips them next boot.
:: Needs admin; we self-elevate via UAC if necessary. Idempotent.
:: ---------------------------------------------------------------
set "NEED_PORT_FIX="
for /f "tokens=1,2" %%a in ('netsh interface ipv4 show excludedportrange protocol^=tcp 2^>nul ^| findstr /r "^ *[0-9]"') do (
    call :_CHECK_PORT_RANGE %%a %%b
)
if not defined NEED_PORT_FIX goto :PORTS_OK

net session >nul 2>&1
if not errorlevel 1 goto :_FIX_PORTS_ADMIN

echo.
echo ============================================
echo   Detected Windows port reservation conflict.
echo   Windows has reserved one of our ports
echo   (18080 / 8180-8189) for Hyper-V/WSL2 use.
echo.
echo   Requesting admin rights to permanently
echo   reserve them for jzhu-trading.
echo   Please click "Yes" when Windows asks.
echo ============================================
echo.
if defined PS_EXE (
    %PS_EXE% -NoProfile -Command "try { Start-Process -FilePath '%~f0' -WorkingDirectory '%~dp0' -Verb RunAs -ErrorAction Stop; exit 0 } catch { exit 1 }"
    if errorlevel 1 (
        echo.
        echo [Info] Admin prompt was declined or failed.
        echo        jzhu-trading cannot start without this one-time fix.
        echo        Please run restart.bat again and click "Yes" on the UAC prompt.
        echo.
        pause
        exit /b 1
    )
    exit /b 0
)
echo [Warn] PowerShell not available. Please right-click restart.bat and
echo        choose "Run as administrator", then try again.
pause
exit /b 1

:_FIX_PORTS_ADMIN
echo Reserving ports for jzhu-trading ^(one-time, persistent^)...
net stop winnat >nul 2>&1
netsh int ipv4 add excludedportrange protocol=tcp startport=8180 numberofports=10 store=persistent >nul 2>&1
netsh int ipv4 add excludedportrange protocol=tcp startport=18080 numberofports=1 store=persistent >nul 2>&1
net start winnat >nul 2>&1
echo Done. Ports are now permanently reserved.
echo.

:PORTS_OK

:: Create desktop shortcut on first run. Name encoded via codepoints so script stays ASCII.
:: Silently skipped if PowerShell is unavailable.
if defined PS_EXE %PS_EXE% -NoProfile -Command "$n=-join @(0x5C0F,0x5B87,0x91CF,0x5316 | ForEach-Object {[char]$_}); $d=[Environment]::GetFolderPath('Desktop'); $lnk=Join-Path $d ($n+'.lnk'); if(-not (Test-Path $lnk)){$s=(New-Object -ComObject WScript.Shell).CreateShortcut($lnk); $s.TargetPath=Join-Path '%~dp0' 'restart.bat'; $s.WorkingDirectory='%~dp0'; $ico=Join-Path '%~dp0' 'icon.ico'; if(Test-Path $ico){$s.IconLocation=$ico}; $s.Description=$n; $s.Save()}" >nul 2>nul

set "HOST_INSTALL_PATH=%CD%"

:: LAN IP detection. Skips 127.* / 169.254.*.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    if not defined HOST_LAN_IP (
        for /f "tokens=*" %%b in ("%%a") do (
            echo %%b| findstr /r "^127\. ^169\.254\." >nul
            if errorlevel 1 set "HOST_LAN_IP=%%b"
        )
    )
)

docker info >nul 2>&1
if not errorlevel 1 goto :DOCKER_READY

:: Docker not running. Locate Docker Desktop and launch it.
set "DOCKER_EXE="
if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" set "DOCKER_EXE=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
if not defined DOCKER_EXE if exist "%LOCALAPPDATA%\Docker\Docker Desktop.exe" set "DOCKER_EXE=%LOCALAPPDATA%\Docker\Docker Desktop.exe"
if not defined DOCKER_EXE goto :NO_DOCKER

echo Docker Desktop is not running. Launching it...
start "" "%DOCKER_EXE%"
echo Waiting for Docker engine (up to 3 minutes)
<nul set /p "=  "

set /a WAIT_ELAPSED=0
:WAIT_DOCKER
timeout /t 3 /nobreak >nul
set /a WAIT_ELAPSED+=3
docker info >nul 2>&1
if not errorlevel 1 (
    echo.
    echo Docker ready after %WAIT_ELAPSED%s.
    echo.
    goto :DOCKER_READY
)
<nul set /p "=."
if %WAIT_ELAPSED% geq 180 goto :DOCKER_TIMEOUT
goto :WAIT_DOCKER

:DOCKER_READY
docker compose down 2>nul

:: If another Docker container (not ours) still holds our ports, stop it.
setlocal enabledelayedexpansion
set "OUR_PROJECT=deploy"
for %%i in ("%CD%") do set "OUR_PROJECT=%%~ni"

for %%p in (18080 8180) do (
    for /f %%c in ('docker ps --filter publish=%%p -q 2^>nul') do (
        for /f "tokens=*" %%x in ('docker inspect --format "{{index .Config.Labels \"com.docker.compose.project\"}}" %%c 2^>nul') do (
            if /i not "%%x"=="!OUR_PROJECT!" (
                for /f "tokens=*" %%n in ('docker inspect --format "{{.Name}}" %%c 2^>nul') do (
                    echo Port %%p is in use by Docker container %%n ^(project: %%x^)
                    echo Stopping it...
                )
                docker stop %%c >nul 2>&1
            )
        )
    )
)
endlocal

echo Pulling latest and starting...
docker compose pull --quiet
docker compose up -d
if errorlevel 1 goto :START_FAILED
echo.
echo ============================================
echo   Ready! Opening browser...
echo   http://localhost:18080
echo ============================================
timeout /t 3 >nul
start http://localhost:18080
goto :EOF

:START_FAILED
echo.
echo ============================================
echo.
echo   [ERROR] Failed to start containers.
echo.
echo   Try the following:
echo     1. Quit Docker Desktop completely, then reopen it
echo     2. Wait until Docker Desktop is fully started
echo     3. Run restart.bat again
echo.
echo   If it still fails, check Docker Desktop:
echo     Settings -^> Resources -^> File Sharing
echo     Make sure the install path is listed: %CD%
echo.
echo ============================================
pause
exit /b 1

:NO_DOCKER
echo ============================================
echo.
echo   Docker Desktop is not installed.
echo.
echo   Please install Docker Desktop:
echo   https://docker.com/products/docker-desktop
echo.
echo   Choose the right version:
echo     Mac M1/M2/M3/M4  = Apple Silicon
echo     Mac Intel         = Intel Chip
echo     Windows           = AMD64
echo.
echo   Free to use. Skip login when prompted.
echo   Then run restart.bat again.
echo.
echo ============================================
pause
goto :EOF

:DOCKER_TIMEOUT
echo.
echo ============================================
echo.
echo   [ERROR] Docker engine did not start within 3 minutes.
echo.
echo   Open Docker Desktop manually and check:
echo     - Tray icon says "Docker Desktop is running"?
echo     - Any first-run setup dialog waiting for input?
echo     - WSL2 installed? (Windows Features -^> Linux subsystem)
echo     - Virtualization enabled in BIOS?
echo.
echo   Once it shows running, run restart.bat again.
echo.
echo ============================================
pause
exit /b 1

:BAD_PATH_SPACE
echo ============================================
echo.
echo   [ERROR] Install path contains a SPACE.
echo.
echo   Current path:
echo   %CD%
echo.
echo   Docker cannot reliably handle spaces in
echo   bind-mount paths. The database container
echo   will fail to load.
echo.
echo   FIX: Move the jzhu-trading folder to a
echo   path with NO SPACES and re-run.
echo.
echo   Recommended: C:\jzhu-trading\
echo.
echo ============================================
pause
exit /b 1

:BAD_PATH_NONASCII
echo ============================================
echo.
echo   [ERROR] Path contains non-English characters.
echo.
echo   Detected path:
echo   %CD%
echo.
echo   Character codepoints ^(any value above 007F is the offender^):
if defined PS_EXE %PS_EXE% -NoProfile -Command "(((Get-Location).Path).ToCharArray() | ForEach-Object { '{0:X4}' -f [int]$_ }) -join ' '" 2>nul
echo.
echo   Common culprits:
echo     - Full-width Latin from Chinese IME ^(FF54='t', FF4F='o'^)
echo     - Cyrillic look-alikes ^(043E='o', 0440='r'^)
echo     - Chinese / Japanese characters ^(4E00 and above^)
echo.
echo   Folder names must only contain:
echo   a-z, A-Z, 0-9, dash, underscore.
echo.
echo   FIX: Re-type the folder name in pure ASCII,
echo   or move jzhu-trading to C:\jzhu-trading\
echo.
echo ============================================
pause
exit /b 1

:: ---------------------------------------------------------------
:: Subroutine called per excludedportrange row.
:: %1 = start port, %2 = end port.
:: Sets NEED_PORT_FIX=1 if the range overlaps any port we use.
:: ---------------------------------------------------------------
:_CHECK_PORT_RANGE
if "%~1"=="" goto :EOF
if "%~2"=="" goto :EOF
if %~1 LEQ 8189 if %~2 GEQ 8180 set "NEED_PORT_FIX=1"
if %~1 LEQ 18080 if %~2 GEQ 18080 set "NEED_PORT_FIX=1"
goto :EOF
