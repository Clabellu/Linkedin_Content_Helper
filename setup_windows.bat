@echo off
title AI Content Helper - Setup Windows
color 0A

echo ==========================================
echo   AI CONTENT HELPER - SETUP WINDOWS
echo ==========================================
echo.
echo Questo script configurera' l'ambiente per l'applicazione
echo.
pause

REM Vai nella cartella dello script
cd /d "%~dp0"

echo.
echo [1/5] Verifica Python...
echo ==========================================
echo.

REM Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo.
    echo Per favore installa Python da: https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante l'installazione seleziona:
    echo  - "Add Python to PATH"
    echo  - "Install pip"
    echo.
    pause
    exit /b 1
)

echo Python trovato!
python --version
echo.

echo [2/5] Verifica pip...
echo ==========================================
echo.

python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: pip non trovato!
    echo.
    echo Installa pip eseguendo:
    echo python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

echo pip trovato!
python -m pip --version
echo.

echo [3/5] Creazione ambiente virtuale...
echo ==========================================
echo.

REM Rimuovi venv esistente se presente
if exist "venv" (
    echo Rimozione ambiente virtuale esistente...
    rmdir /s /q venv
)

echo Creazione nuovo ambiente virtuale...
python -m venv venv

if not exist "venv\Scripts\python.exe" (
    echo ERRORE: Impossibile creare ambiente virtuale!
    echo.
    pause
    exit /b 1
)

echo Ambiente virtuale creato con successo!
echo.

echo [4/5] Installazione dipendenze...
echo ==========================================
echo.

REM Attiva ambiente virtuale e installa dipendenze
call venv\Scripts\activate.bat

echo Aggiornamento pip...
python -m pip install --upgrade pip

echo.
echo Installazione dipendenze da requirements.txt...
echo Questo potrebbe richiedere alcuni minuti...
echo.

if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ATTENZIONE: Alcune dipendenze potrebbero non essere installate
        echo Continuo comunque...
        echo.
    )
) else (
    echo ATTENZIONE: requirements.txt non trovato
    echo Installo solo le dipendenze essenziali...
    echo.
    pip install feedparser requests python-dotenv anthropic
)

echo.

echo [5/5] Verifica installazione...
echo ==========================================
echo.

REM Verifica dipendenze critiche
echo Verifica feedparser...
python -c "import feedparser; print('✓ feedparser OK')" 2>nul || echo "✗ feedparser MANCANTE"

echo Verifica requests...
python -c "import requests; print('✓ requests OK')" 2>nul || echo "✗ requests MANCANTE"

echo Verifica tkinter...
python -c "import tkinter; print('✓ tkinter OK')" 2>nul || echo "✗ tkinter MANCANTE (incluso in Python)"

echo Verifica python-dotenv...
python -c "import dotenv; print('✓ python-dotenv OK')" 2>nul || echo "✗ python-dotenv MANCANTE"

echo.
echo ==========================================
echo   SETUP COMPLETATO!
echo ==========================================
echo.
echo ✓ Python installato
echo ✓ Ambiente virtuale creato: venv\
echo ✓ Dipendenze installate
echo.
echo PROSSIMI PASSI:
echo.
echo 1. Crea un file .env nella cartella del progetto
echo 2. Aggiungi la tua API key:
echo    ANTHROPIC_API_KEY=la_tua_chiave_api
echo.
echo 3. Avvia l'applicazione con: start_app.bat
echo.
echo Per maggiori informazioni consulta il README.md
echo.
pause
