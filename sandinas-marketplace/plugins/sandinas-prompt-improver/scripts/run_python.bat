@echo off
REM Python wrapper for Windows - with stderr suppression for hooks
REM Redirects stderr to prevent non-JSON output from breaking hook parsing

setlocal EnableDelayedExpansion

REM Try python3 first
where python3 >nul 2>&1
if !errorlevel! equ 0 (
    python3 %* 2>nul
    exit /b !errorlevel!
)

REM Try python
where python >nul 2>&1
if !errorlevel! equ 0 (
    python %* 2>nul
    exit /b !errorlevel!
)

REM Try py launcher
where py >nul 2>&1
if !errorlevel! equ 0 (
    py %* 2>nul
    exit /b !errorlevel!
)

REM If Python not found, still output JSON to prevent hook errors
REM This ensures the Stop hook never prevents session closure
echo {"continue": false}
exit /b 0
