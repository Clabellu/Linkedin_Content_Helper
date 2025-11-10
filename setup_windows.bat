@echo off
title LinkedIn Content Helper - Setup e Installazione
color 0B

echo.
echo ========================================================================
echo           LINKEDIN CONTENT HELPER - INSTALLAZIONE AUTOMATICA
echo ========================================================================
echo.
echo Questo script installerà e configurerà automaticamente l'applicazione.
echo.
echo Requisiti:
echo   - Python 3.8 o superiore
echo   - Connessione Internet (per scaricare dipendenze)
echo   - API Keys: Anthropic Claude e OpenAI
echo.
echo ========================================================================
echo.
pause

REM Vai nella cartella del progetto
cd /d "%~dp0"

echo.
echo [1/7] Verifica installazione Python...
echo ========================================================================

REM Verifica Python installato
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [X] ERRORE: Python non trovato!
    echo.
    echo Scarica e installa Python da: https://www.python.org/downloads/
    echo Assicurati di selezionare "Add Python to PATH" durante l'installazione.
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python trovato!

echo.
echo [2/7] Verifica versione Python...
echo ========================================================================

REM Verifica versione Python >= 3.8
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versione rilevata: %PYTHON_VERSION%

REM Estrai major.minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo [X] ERRORE: Python 3.8+ richiesto. Versione trovata: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 8 (
    echo [X] ERRORE: Python 3.8+ richiesto. Versione trovata: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo [OK] Versione Python compatibile!

echo.
echo [3/7] Creazione ambiente virtuale...
echo ========================================================================

if exist "venv\" (
    echo Ambiente virtuale già esistente. Vuoi ricrearlo? (S/N)
    set /p RECREATE_VENV=^>
    if /i "%RECREATE_VENV%"=="S" (
        echo Rimozione ambiente virtuale esistente...
        rmdir /s /q venv
        echo Creazione nuovo ambiente virtuale...
        python -m venv venv
        if errorlevel 1 (
            echo [X] ERRORE: Impossibile creare ambiente virtuale
            pause
            exit /b 1
        )
        echo [OK] Nuovo ambiente virtuale creato!
    ) else (
        echo [OK] Utilizzo ambiente virtuale esistente
    )
) else (
    echo Creazione ambiente virtuale...
    python -m venv venv
    if errorlevel 1 (
        echo [X] ERRORE: Impossibile creare ambiente virtuale
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato!
)

echo.
echo [4/7] Installazione dipendenze...
echo ========================================================================
echo Questo potrebbe richiedere alcuni minuti...
echo.

call venv\Scripts\activate.bat

REM Aggiorna pip
echo Aggiornamento pip...
python -m pip install --upgrade pip >nul 2>&1

REM Installa dipendenze
echo Installazione pacchetti da requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [!] AVVISO: Alcuni pacchetti potrebbero non essere stati installati correttamente
    echo Controlla gli errori sopra. L'applicazione potrebbe comunque funzionare.
    echo.
    pause
) else (
    echo [OK] Tutte le dipendenze installate con successo!
)

echo.
echo [5/7] Configurazione API Keys...
echo ========================================================================

REM Verifica se .env esiste
if not exist ".env" (
    if exist ".env.example" (
        echo File .env non trovato. Creo da template...
        copy .env.example .env >nul
        echo [!] IMPORTANTE: Devi configurare le API Keys nel file .env
        echo.
        echo File .env creato. Vuoi configurare le API Keys ora? (S/N)
        set /p CONFIG_NOW=^>
        if /i "%CONFIG_NOW%"=="S" (
            echo.
            echo Avvio configurazione guidata...
            python first_run_config.py
            if errorlevel 1 (
                echo.
                echo [!] Configurazione guidata non disponibile
                echo Apri manualmente il file .env e inserisci le tue API keys
                echo.
                notepad .env
            )
        ) else (
            echo.
            echo [!] RICORDA: Devi configurare il file .env prima di usare l'app!
            echo Apri il file .env e inserisci le tue API keys:
            echo   - ANTHROPIC_API_KEY
            echo   - OPENAI_API_KEY
            echo.
        )
    ) else (
        echo [X] ERRORE: File .env.example non trovato!
        pause
        exit /b 1
    )
) else (
    echo [OK] File .env già esistente
    echo.
    echo Vuoi riconfigurare le API Keys? (S/N)
    set /p RECONFIG=^>
    if /i "%RECONFIG%"=="S" (
        python first_run_config.py
        if errorlevel 1 (
            notepad .env
        )
    )
)

echo.
echo [6/7] Creazione cartelle necessarie...
echo ========================================================================

if not exist "generated_posts\" mkdir generated_posts
if not exist "logs\" mkdir logs
if not exist "reports\" mkdir reports

echo [OK] Cartelle create:
echo   - generated_posts/
echo   - logs/
echo   - reports/

echo.
echo [7/7] Test configurazione...
echo ========================================================================
echo.
echo Vuoi eseguire un test per verificare che tutto funzioni? (S/N)
set /p RUN_TEST=^>

if /i "%RUN_TEST%"=="S" (
    echo.
    echo Esecuzione test...
    echo.
    python automation_test.py

    if errorlevel 1 (
        echo.
        echo [!] AVVISO: Alcuni test sono falliti
        echo Controlla i log sopra per dettagli.
        echo L'app potrebbe comunque funzionare parzialmente.
        echo.
    ) else (
        echo.
        echo [OK] Tutti i test superati!
        echo.
    )
)

echo.
echo ========================================================================
echo                    INSTALLAZIONE COMPLETATA!
echo ========================================================================
echo.
echo L'applicazione è pronta all'uso!
echo.
echo PROSSIMI PASSI:
echo   1. Verifica che le API Keys siano configurate in .env
echo   2. Avvia l'app con: AVVIA_APP.bat
echo   3. Oppure usa: python main_launcher.py
echo.
echo FILE IMPORTANTI:
echo   - .env                  : Configurazione API keys
echo   - automation_config.json: Configurazione automazione
echo   - feeds.txt             : Lista feed RSS
echo.
echo CARTELLE UTILI:
echo   - generated_posts/      : Post generati dall'automazione
echo   - logs/                 : File di log
echo.
echo ========================================================================
echo.

REM Chiedi se avviare l'app
echo Vuoi avviare l'applicazione ora? (S/N)
set /p START_APP=^>

if /i "%START_APP%"=="S" (
    echo.
    echo Avvio applicazione...
    start "" pythonw main_launcher.py
    timeout /t 2 /nobreak >nul
    echo.
    echo Applicazione avviata!
    echo Cerca la finestra "AI Content Helper - Launcher"
    echo.
)

echo.
echo Premi un tasto per chiudere questo setup...
pause >nul

call deactivate >nul 2>&1
exit /b 0
