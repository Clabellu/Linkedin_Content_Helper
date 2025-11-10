# create_desktop_shortcut.py
"""
Script per creare un collegamento sul desktop di Windows
"""

import os
import sys
from pathlib import Path


def create_desktop_shortcut():
    """Crea un collegamento sul desktop per AVVIA_APP.bat"""

    try:
        # Import winshell solo su Windows
        if sys.platform != 'win32':
            print("Questo script funziona solo su Windows!")
            return False

        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            print("\n" + "="*60)
            print("Installazione moduli necessari...")
            print("="*60)
            print("\nInstallando pywin32 e winshell...\n")

            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "winshell"])

            print("\nModuli installati! Riavvia questo script.")
            return False

        # Percorso del desktop
        desktop = winshell.desktop()

        # Percorso del progetto (directory corrente)
        project_dir = Path(__file__).parent.absolute()

        # Percorso del file batch da linkare
        batch_file = project_dir / "AVVIA_APP.bat"

        if not batch_file.exists():
            print(f"Errore: File {batch_file} non trovato!")
            return False

        # Percorso del collegamento
        shortcut_path = os.path.join(desktop, "LinkedIn Content Helper.lnk")

        # Crea il collegamento
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = str(batch_file)
        shortcut.WorkingDirectory = str(project_dir)
        shortcut.Description = "LinkedIn Content Helper - Generatore Automatico Post AI"

        # Cerca un'icona (se esiste)
        icon_path = project_dir / "assets" / "icon.ico"
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)

        shortcut.save()

        print("\n" + "="*60)
        print("✅ COLLEGAMENTO CREATO CON SUCCESSO!")
        print("="*60)
        print(f"\nPercorso: {shortcut_path}")
        print("\nOra puoi avviare l'applicazione dal desktop!")
        print("\nCollegamento: 'LinkedIn Content Helper'")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Errore durante la creazione del collegamento: {e}\n")
        return False


def create_simple_bat_shortcut():
    """
    Metodo alternativo: crea un file .bat sul desktop
    (non richiede librerie esterne)
    """
    try:
        # Trova il desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        if not os.path.exists(desktop):
            # Prova percorso alternativo
            desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")

        if not os.path.exists(desktop):
            print("Impossibile trovare il desktop!")
            return False

        # Percorso del progetto
        project_dir = Path(__file__).parent.absolute()
        batch_file = project_dir / "AVVIA_APP.bat"

        # Crea un batch launcher sul desktop
        launcher_content = f"""@echo off
REM Launcher per LinkedIn Content Helper
cd /d "{project_dir}"
call AVVIA_APP.bat
"""

        launcher_path = os.path.join(desktop, "LinkedIn Content Helper.bat")

        with open(launcher_path, 'w') as f:
            f.write(launcher_content)

        print("\n" + "="*60)
        print("✅ LAUNCHER CREATO CON SUCCESSO!")
        print("="*60)
        print(f"\nPercorso: {launcher_path}")
        print("\nOra puoi avviare l'applicazione dal desktop!")
        print("\nFile: 'LinkedIn Content Helper.bat'")
        print("\nNOTA: Puoi rinominarlo o creare un collegamento personalizzato")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Errore: {e}\n")
        return False


def main():
    """Funzione principale"""
    print("\n" + "="*70)
    print("     CREAZIONE COLLEGAMENTO DESKTOP - LINKEDIN CONTENT HELPER")
    print("="*70 + "\n")

    print("Scegli il metodo di creazione:\n")
    print("  [1] Collegamento .lnk (Consigliato, richiede pywin32)")
    print("  [2] File .bat sul desktop (Semplice, nessuna dipendenza)")
    print("  [3] Annulla\n")

    choice = input("Scelta [1-3]: ").strip()

    if choice == "1":
        print("\nCreazione collegamento .lnk...\n")
        success = create_desktop_shortcut()

        if not success:
            print("\nProvo il metodo alternativo...\n")
            create_simple_bat_shortcut()

    elif choice == "2":
        print("\nCreazione launcher .bat...\n")
        create_simple_bat_shortcut()

    elif choice == "3":
        print("\nAnnullato.\n")
        return

    else:
        print("\nScelta non valida!\n")
        return

    input("\nPremi INVIO per chiudere...")


if __name__ == "__main__":
    main()
