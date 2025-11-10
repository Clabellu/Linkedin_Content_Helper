@echo off
title LinkedIn Content Helper
color 0B

REM ============================================================================
REM   LINKEDIN CONTENT HELPER - LAUNCHER UNIFICATO
REM ============================================================================
REM   Questo è il modo consigliato per avviare l'applicazione.
REM   Lo script verifica l'installazione e avvia l'app automaticamente.
REM ============================================================================

REM Vai nella cartella del progetto
cd /d "%~dp0"

echo.
echo ========================================================================
echo           LINKEDIN CONTENT HELPER - AVVIO APPLICAZIONE
echo ========================================================================
echo.

REM ============================================================================
REM STEP 1: Verifica installazione
REM ============================================================================

echo [Verifica 1/4] Controllo installazione...

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [X] Python non trovato!
    echo.
    echo L'applicazione richiede Python 3.8 o superiore.
    echo Vuoi procedere con l'installazione automatica? (S/N)
    set /p INSTALL=^>
    if /i "%INSTALL%"=="S" (
        echo.
        echo Avvio installazione...
        call setup_windows.bat
        exit /b
    ) else (
        echo.
        echo Installa Python da: https://www.python.org/downloads/
        echo Poi esegui: setup_windows.bat
        echo.
        pause
        exit /b 1
    )
)

REM Verifica ambiente virtuale
if not exist "venv\Scripts\python.exe" (
    echo.
    echo [X] Ambiente virtuale non trovato!
    echo.
    echo Prima esecuzione rilevata.
    echo Vuoi procedere con l'installazione automatica? (S/N)
    set /p INSTALL=^>
    if /i "%INSTALL%"=="S" (
        echo.
        echo Avvio installazione...
        call setup_windows.bat
        exit /b
    ) else (
        echo.
        echo Esegui manualmente: setup_windows.bat
        echo.
        pause
        exit /b 1
    )
)

echo [OK] Python e ambiente virtuale trovati

REM ============================================================================
REM STEP 2: Verifica file essenziali
REM ============================================================================

echo [Verifica 2/4] Controllo file essenziali...

set MISSING_FILES=0

if not exist "main_launcher.py" (
    echo [X] File main_launcher.py mancante!
    set MISSING_FILES=1
)

if not exist "control_panel.py" (
    echo [X] File control_panel.py mancante!
    set MISSING_FILES=1
)

if not exist "daily_ai_automation.py" (
    echo [X] File daily_ai_automation.py mancante!
    set MISSING_FILES=1
)

if not exist "automation_config.json" (
    echo [X] File automation_config.json mancante!
    set MISSING_FILES=1
)

if %MISSING_FILES%==1 (
    echo.
    echo [X] Alcuni file essenziali sono mancanti!
    echo Reinstalla l'applicazione o scarica i file dal repository.
    echo.
    pause
    exit /b 1
)

echo [OK] Tutti i file essenziali presenti

REM ============================================================================
REM STEP 3: Verifica configurazione API keys
REM ============================================================================

echo [Verifica 3/4] Controllo configurazione API keys...

if not exist ".env" (
    echo.
    echo [!] File .env non trovato!
    echo.
    echo Prima configurazione richiesta.
    echo Vuoi configurare le API keys ora? (S/N)
    set /p CONFIG=^>
    if /i "%CONFIG%"=="S" (
        echo.
        echo Avvio configurazione guidata...
        call venv\Scripts\python.exe first_run_config.py
        if errorlevel 1 (
            echo.
            echo [!] Configurazione annullata o fallita
            echo Configura manualmente il file .env e riprova
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo [!] ATTENZIONE: L'app non funzionerà senza API keys configurate!
        echo.
        echo Crea un file .env partendo da .env.example
        echo Oppure esegui: python first_run_config.py
        echo.
        pause
        exit /b 1
    )
)

REM Verifica che .env contenga chiavi reali (non placeholder)
findstr /C:"your_anthropic" .env >nul
if not errorlevel 1 (
    echo.
    echo [!] ATTENZIONE: API keys non configurate correttamente!
    echo.
    echo Il file .env contiene ancora i placeholder.
    echo Vuoi riconfigurare le API keys? (S/N)
    set /p RECONFIG=^>
    if /i "%RECONFIG%"=="S" (
        call venv\Scripts\python.exe first_run_config.py
    ) else (
        echo.
        echo [!] L'app potrebbe non funzionare senza API keys valide
        echo.
    )
)

echo [OK] File .env presente

REM ============================================================================
REM STEP 4: Verifica cartelle necessarie
REM ============================================================================

echo [Verifica 4/4] Controllo cartelle...

if not exist "generated_posts\" mkdir generated_posts >nul 2>&1
if not exist "logs\" mkdir logs >nul 2>&1
if not exist "reports\" mkdir reports >nul 2>&1

echo [OK] Cartelle verificate

echo.
echo ========================================================================
echo                    AVVIO APPLICAZIONE
echo ========================================================================
echo.

REM ============================================================================
REM AVVIO APPLICAZIONE
REM ============================================================================

REM Chiedi quale modalità usare
echo Seleziona la modalità di avvio:
echo.
echo   [1] Launcher Grafico (Consigliato)
echo   [2] Pannello di Controllo
echo   [3] App Manuale (Generazione Singola)
echo   [4] Test Automazione
echo   [5] Esci
echo.
set /p MODE=Scegli [1-5]:

if "%MODE%"=="1" (
    echo.
    echo Avvio Launcher Grafico...
    start "" venv\Scripts\pythonw.exe main_launcher.py
    goto :success
)

if "%MODE%"=="2" (
    echo.
    echo Avvio Pannello di Controllo...
    start "" venv\Scripts\pythonw.exe control_panel.py
    goto :success
)

if "%MODE%"=="3" (
    echo.
    echo Avvio App Manuale...
    start "" venv\Scripts\pythonw.exe new_fetcher.py
    goto :success
)

if "%MODE%"=="4" (
    echo.
    echo Esecuzione Test Automazione...
    echo.
    call venv\Scripts\python.exe automation_test.py
    echo.
    echo Test completato. Premi un tasto per uscire...
    pause >nul
    exit /b
)

if "%MODE%"=="5" (
    echo.
    echo Uscita...
    exit /b 0
)

REM Scelta non valida
echo.
echo [X] Scelta non valida!
echo.
pause
goto :EOF

:success
echo.
echo ========================================================================
echo                    APPLICAZIONE AVVIATA
echo ========================================================================
echo.
echo L'applicazione è stata avviata in background.
echo Cerca la finestra dell'applicazione.
echo.
echo Se non vedi la finestra:
echo   - Controlla la barra delle applicazioni
echo   - Controlla il Task Manager (potrebbe essere nascosta)
echo.
echo Per chiudere l'applicazione, chiudi la sua finestra.
echo.
echo ========================================================================
echo.
timeout /t 3 /nobreak >nul
exit /b 0
