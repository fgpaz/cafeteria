@echo off
REM Windows installation script for claude-code-prompt-improver
REM This script sets up the plugin for Windows users

echo Installing Claude Code Prompt Improver for Windows...
echo.

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found successfully.
echo.

REM Check if Claude Code is installed
where claude >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Claude Code not found in PATH.
    echo Please make sure Claude Code is installed and in your PATH.
    pause
    exit /b 1
)

echo Claude Code found successfully.
echo.

REM Get current directory
set PLUGIN_DIR=%CD%

echo Installing plugin from: %PLUGIN_DIR%
echo.

REM Add current directory as local marketplace
echo Adding local marketplace...
claude plugin marketplace add ./
if %errorlevel% neq 0 (
    echo ERROR: Failed to add local marketplace.
    pause
    exit /b 1
)

echo Installing prompt-improver plugin...
claude plugin install prompt-improver@local-dev
if %errorlevel% neq 0 (
    echo ERROR: Failed to install plugin.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo Please restart Claude Code to activate the plugin.
echo.
echo To verify installation, run: claude "help me with this"
echo You should see "PROMPT EVALUATION" appear.
echo.
pause