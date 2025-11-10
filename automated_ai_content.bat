@echo off
REM automated_ai_content.bat - Script ottimizzato per Task Scheduler
REM Questo script viene eseguito automaticamente dal Task Scheduler

REM Imposta variabili (usa path dinamico)
set PROJECT_DIR=%~dp0
REM Rimuovi il trailing backslash se presente
if "%PROJECT_DIR:~-1%"=="\" set PROJECT_DIR=%PROJECT_DIR:~0,-1%

set VENV_PYTHON=%PROJECT_DIR%\venv\Scripts\python.exe
set LOG_FILE=%PROJECT_DIR%\logs\scheduler_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%.log

REM Vai nella directory del progetto
cd /d "%PROJECT_DIR%"

REM Crea log di avvio
echo [%date% %time%] === AVVIO AUTOMAZIONE SCHEDULATA === >> "%LOG_FILE%"
echo [%date% %time%] Percorso progetto: %PROJECT_DIR% >> "%LOG_FILE%"
echo [%date% %time%] Python venv: %VENV_PYTHON% >> "%LOG_FILE%"

REM Verifica che l'ambiente virtuale esista
if not exist "%VENV_PYTHON%" (
    echo [%date% %time%] ERRORE: Python ambiente virtuale non trovato >> "%LOG_FILE%"
    echo [%date% %time%] Percorso cercato: %VENV_PYTHON% >> "%LOG_FILE%"
    exit /b 1
)

REM Verifica che il file di automazione esista
if not exist "daily_ai_automation.py" (
    echo [%date% %time%] ERRORE: File daily_ai_automation.py non trovato >> "%LOG_FILE%"
    exit /b 1
)

REM Verifica configurazione
if not exist "automation_config.json" (
    echo [%date% %time%] ERRORE: File automation_config.json non trovato >> "%LOG_FILE%"
    exit /b 1
)

REM Controlla se l'automazione è abilitata nel config
findstr /C:"\"enabled\": true" automation_config.json >nul
if errorlevel 1 (
    echo [%date% %time%] AUTOMAZIONE DISABILITATA nel file di configurazione >> "%LOG_FILE%"
    echo [%date% %time%] Esecuzione interrotta >> "%LOG_FILE%"
    exit /b 0
)

echo [%date% %time%] Tutti i controlli preliminari superati >> "%LOG_FILE%"
echo [%date% %time%] Avvio generazione contenuti AI... >> "%LOG_FILE%"

REM Esegui l'automazione e cattura il risultato
"%VENV_PYTHON%" daily_ai_automation.py
set AUTOMATION_EXIT_CODE=%errorlevel%

REM Log del risultato
if %AUTOMATION_EXIT_CODE% equ 0 (
    echo [%date% %time%] ✓ AUTOMAZIONE COMPLETATA CON SUCCESSO >> "%LOG_FILE%"
) else (
    echo [%date% %time%] ✗ AUTOMAZIONE FALLITA - Codice errore: %AUTOMATION_EXIT_CODE% >> "%LOG_FILE%"
)

echo [%date% %time%] === FINE AUTOMAZIONE SCHEDULATA === >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Pulizia file temporanei (opzionale)
if exist "temp_*.png" del "temp_*.png" >nul 2>&1
if exist "temp_*.jpg" del "temp_*.jpg" >nul 2>&1

exit /b %AUTOMATION_EXIT_CODE%