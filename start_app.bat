@echo off
title AI Content Helper - Launcher

echo ==========================================
echo      AI CONTENT HELPER - LAUNCHER  
echo ==========================================
echo.

REM Vai nella cartella progetto
cd /d "C:\Users\bellu\OneDrive\Desktop\Programmazione\Linkedin_Content_Helper_Clean"

REM Verifica che i file esistano
if not exist "main_launcher.py" (
    echo ERRORE: File main_launcher.py non trovato
    pause
    exit /b 1
)

if not exist "venv\Scripts\pythonw.exe" (
    echo ERRORE: Ambiente virtuale non trovato
    pause
    exit /b 1
)

if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

REM Usa pythonw (senza finestra console)
set VENV_PYTHON=%CD%\venv\Scripts\python.exe
set VENV_PYTHONW=%CD%\venv\Scripts\pythonw.exe

echo Verificando dipendenze...
echo.

REM Verifica/installa dipendenze
"%VENV_PYTHON%" -c "import feedparser; print('✓ feedparser installato')" 2>nul || (
    echo Installando feedparser...
    "%VENV_PYTHON%" -m pip install feedparser
    echo.
)

"%VENV_PYTHON%" -c "import requests; print('✓ requests installato')" 2>nul || (
    echo Installando requests...
    "%VENV_PYTHON%" -m pip install requests
    echo.
)

"%VENV_PYTHON%" -c "import tkinter; print('✓ tkinter disponibile')" 2>nul || (
    echo ✗ tkinter non disponibile
)

echo.
echo Tutte le dipendenze verificate!
echo.
echo Avviando AI Content Helper...
echo L'app si aprirà senza finestra command prompt.
echo.

REM Lancia l'app senza finestra console usando pythonw
start /min "AI Content Helper" "%VENV_PYTHONW%" main_launcher.py

REM Attende 2 secondi per permettere all'app di avviarsi
timeout /t 2 /nobreak >nul

echo.
echo ✓ AI Content Helper avviato con successo!
echo.
echo L'app è ora in esecuzione in background.
echo Cerca l'icona nella barra delle applicazioni.
echo.
echo Puoi chiudere questa finestra.
echo.
pause