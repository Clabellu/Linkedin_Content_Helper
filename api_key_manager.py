# api_key_manager.py
"""
Modulo per la gestione delle API keys.
Fornisce funzioni per leggere, validare e gestire le chiavi API.
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv, set_key


class APIKeyManager:
    """Gestisce le API keys dell'applicazione"""

    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self.env_example = Path(".env.example")
        self.load_env()

    def load_env(self):
        """Carica le variabili d'ambiente dal file .env"""
        if self.env_file.exists():
            load_dotenv(self.env_file)
        else:
            # Se .env non esiste, prova a crearlo da .env.example
            if self.env_example.exists():
                self.env_example.rename(self.env_file)
                load_dotenv(self.env_file)

    def get_key(self, key_name: str) -> Optional[str]:
        """
        Ottiene una API key dalle variabili d'ambiente

        Args:
            key_name: Nome della chiave (es. 'ANTHROPIC_API_KEY')

        Returns:
            La chiave se trovata e valida, None altrimenti
        """
        key = os.getenv(key_name)

        if not key:
            return None

        # Controlla se è un placeholder
        if key.startswith('your_') or key.startswith('sk-') and len(key) < 20:
            return None

        return key.strip()

    def get_anthropic_key(self) -> Optional[str]:
        """Ottiene la chiave Anthropic/Claude"""
        # Prova entrambi i nomi
        key = self.get_key('ANTHROPIC_API_KEY')
        if not key:
            key = self.get_key('CLAUDE_API_KEY')
        return key

    def get_openai_key(self) -> Optional[str]:
        """Ottiene la chiave OpenAI"""
        return self.get_key('OPENAI_API_KEY')

    def get_google_key(self) -> Optional[str]:
        """Ottiene la chiave Google Gemini"""
        return self.get_key('GOOGLE_API_KEY')

    def get_all_keys(self) -> Dict[str, Optional[str]]:
        """
        Ottiene tutte le API keys configurate

        Returns:
            Dizionario con tutte le chiavi
        """
        return {
            'anthropic': self.get_anthropic_key(),
            'openai': self.get_openai_key(),
            'google': self.get_google_key()
        }

    def set_key(self, key_name: str, key_value: str) -> bool:
        """
        Imposta una API key nel file .env

        Args:
            key_name: Nome della chiave
            key_value: Valore della chiave

        Returns:
            True se salvato con successo, False altrimenti
        """
        try:
            # Assicurati che il file .env esista
            if not self.env_file.exists():
                self.env_file.touch()

            # Usa dotenv per salvare
            set_key(str(self.env_file), key_name, key_value)

            # Ricarica le variabili d'ambiente
            load_dotenv(self.env_file, override=True)

            return True

        except Exception as e:
            print(f"Errore durante il salvataggio della chiave {key_name}: {e}")
            return False

    def validate_key_format(self, key: str, key_type: str = 'generic') -> Tuple[bool, str]:
        """
        Valida il formato di una API key

        Args:
            key: La chiave da validare
            key_type: Tipo di chiave ('anthropic', 'openai', 'google', 'generic')

        Returns:
            Tupla (valido, messaggio_errore)
        """
        if not key or not key.strip():
            return False, "La chiave non può essere vuota"

        key = key.strip()

        # Controlli comuni
        if key.startswith('your_'):
            return False, "Inserisci una chiave reale, non il placeholder"

        if len(key) < 20:
            return False, "La chiave sembra troppo corta per essere valida"

        # Controlli specifici per tipo
        if key_type == 'anthropic':
            if not key.startswith('sk-ant-'):
                return False, "Le chiavi Anthropic devono iniziare con 'sk-ant-'"

        elif key_type == 'openai':
            if not key.startswith('sk-'):
                return False, "Le chiavi OpenAI devono iniziare con 'sk-'"

        elif key_type == 'google':
            # Google API keys hanno un formato più variabile
            if len(key) < 30:
                return False, "La chiave Google sembra troppo corta"

        return True, "Chiave valida (formato)"

    def test_anthropic_key(self, key: Optional[str] = None) -> Tuple[bool, str]:
        """
        Testa la connessione con l'API Anthropic

        Args:
            key: Chiave da testare (usa quella salvata se None)

        Returns:
            Tupla (successo, messaggio)
        """
        if key is None:
            key = self.get_anthropic_key()

        if not key:
            return False, "Nessuna chiave Anthropic configurata"

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=key)

            # Test minimo
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Test"}]
            )

            if response:
                return True, "Connessione Anthropic riuscita"

        except ImportError:
            return False, "Libreria 'anthropic' non installata"
        except Exception as e:
            return False, f"Errore connessione Anthropic: {str(e)[:100]}"

    def test_openai_key(self, key: Optional[str] = None) -> Tuple[bool, str]:
        """
        Testa la connessione con l'API OpenAI

        Args:
            key: Chiave da testare (usa quella salvata se None)

        Returns:
            Tupla (successo, messaggio)
        """
        if key is None:
            key = self.get_openai_key()

        if not key:
            return False, "Nessuna chiave OpenAI configurata"

        try:
            import openai

            client = openai.OpenAI(api_key=key)

            # Test minimo (lista modelli)
            models = client.models.list()

            if models:
                return True, "Connessione OpenAI riuscita"

        except ImportError:
            return False, "Libreria 'openai' non installata"
        except Exception as e:
            return False, f"Errore connessione OpenAI: {str(e)[:100]}"

    def test_google_key(self, key: Optional[str] = None) -> Tuple[bool, str]:
        """
        Testa la connessione con l'API Google Gemini

        Args:
            key: Chiave da testare (usa quella salvata se None)

        Returns:
            Tupla (successo, messaggio)
        """
        if key is None:
            key = self.get_google_key()

        if not key:
            return False, "Nessuna chiave Google configurata"

        try:
            from google import genai

            genai.configure(api_key=key)
            client = genai.Client()

            # Test minimo
            models = client.models.list()

            if models:
                return True, "Connessione Google Gemini riuscita"

        except ImportError:
            return False, "Libreria 'google-generativeai' non installata"
        except Exception as e:
            return False, f"Errore connessione Google: {str(e)[:100]}"

    def verify_all_required_keys(self) -> Tuple[bool, list]:
        """
        Verifica che tutte le chiavi obbligatorie siano configurate

        Returns:
            Tupla (tutte_presenti, lista_chiavi_mancanti)
        """
        missing = []

        if not self.get_anthropic_key():
            missing.append("ANTHROPIC_API_KEY (obbligatoria)")

        if not self.get_openai_key():
            missing.append("OPENAI_API_KEY (obbligatoria)")

        return len(missing) == 0, missing

    def get_status_report(self) -> str:
        """
        Genera un report dello stato delle API keys

        Returns:
            Stringa formattata con lo stato
        """
        report = "📊 STATO API KEYS\n"
        report += "=" * 50 + "\n\n"

        # Anthropic
        anthropic = self.get_anthropic_key()
        if anthropic:
            success, msg = self.test_anthropic_key()
            status = "✅" if success else "⚠️"
            report += f"{status} Anthropic: Configurata ({msg})\n"
        else:
            report += "❌ Anthropic: NON configurata (obbligatoria)\n"

        # OpenAI
        openai = self.get_openai_key()
        if openai:
            success, msg = self.test_openai_key()
            status = "✅" if success else "⚠️"
            report += f"{status} OpenAI: Configurata ({msg})\n"
        else:
            report += "❌ OpenAI: NON configurata (obbligatoria)\n"

        # Google
        google = self.get_google_key()
        if google:
            success, msg = self.test_google_key()
            status = "✅" if success else "⚠️"
            report += f"{status} Google Gemini: Configurata ({msg})\n"
        else:
            report += "⚪ Google Gemini: NON configurata (opzionale)\n"

        report += "\n" + "=" * 50

        return report


# Funzioni di utilità per accesso rapido
_manager = None


def get_manager() -> APIKeyManager:
    """Ottiene l'istanza singleton del manager"""
    global _manager
    if _manager is None:
        _manager = APIKeyManager()
    return _manager


def get_anthropic_key() -> Optional[str]:
    """Shortcut per ottenere la chiave Anthropic"""
    return get_manager().get_anthropic_key()


def get_openai_key() -> Optional[str]:
    """Shortcut per ottenere la chiave OpenAI"""
    return get_manager().get_openai_key()


def get_google_key() -> Optional[str]:
    """Shortcut per ottenere la chiave Google"""
    return get_manager().get_google_key()


def verify_required_keys() -> bool:
    """Shortcut per verificare le chiavi obbligatorie"""
    all_present, missing = get_manager().verify_all_required_keys()
    return all_present


# CLI per test
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   API KEY MANAGER - TEST")
    print("=" * 60 + "\n")

    manager = APIKeyManager()

    # Verifica chiavi presenti
    all_present, missing = manager.verify_all_required_keys()

    if not all_present:
        print("⚠️ Chiavi mancanti:")
        for key in missing:
            print(f"  - {key}")
        print()

    # Report completo
    print(manager.get_status_report())
    print()
