@echo off
title AI Content Automation

echo ========================================
echo    AUTOMAZIONE GIORNALIERA AI CONTENT
echo ========================================
echo Start Time: %date% %time%
echo.

REM Vai nella cartella progetto (usa path dinamico)
cd /d "%~dp0"

REM Controlla che tutti i file esistano
if not exist "daily_ai_automation.py" (
    echo ERRORE: File daily_ai_automation.py non trovato
    echo End Time: %date% %time%
    exit /b 1
)

if not exist "venv\Scripts\activate.bat" (
    echo ERRORE: Ambiente virtuale non trovato
    echo End Time: %date% %time%
    exit /b 1
)

REM Attiva ambiente virtuale
echo Attivazione ambiente virtuale...
call venv\Scripts\activate

REM Verifica che Python sia corretto
python --version
if errorlevel 1 (
    echo ERRORE: Python non funziona correttamente
    echo End Time: %date% %time%
    exit /b 1
)

REM Esegui automazione
echo.
echo Avvio automazione AI content...
echo.
python daily_ai_automation.py

REM Registra risultato
set EXIT_CODE=%errorlevel%
echo.
echo ========================================
if %EXIT_CODE% equ 0 (
    echo ✅ AUTOMAZIONE COMPLETATA CON SUCCESSO
) else (
    echo ❌ AUTOMAZIONE FALLITA (Codice: %EXIT_CODE%)
)
echo End Time: %date% %time%
echo ========================================

REM Deattiva ambiente virtuale
call deactivate >nul 2>&1

REM Mantieni la finestra aperta solo se c'è errore (per debug)
if not %EXIT_CODE% equ 0 (
    echo.
    echo Premere un tasto per chiudere...
    pause >nul
)