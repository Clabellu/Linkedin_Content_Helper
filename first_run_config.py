# first_run_config.py
"""
LinkedIn Content Helper - First Run Configuration (Modernized with ttkbootstrap)
Wizard di configurazione guidata per le API keys al primo avvio
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os
import re
from pathlib import Path


class FirstRunConfigGUI:
    def __init__(self):
        # Crea finestra principale con tema moderno
        self.root = ttk.Window(
            title="LinkedIn Content Helper - Configurazione Iniziale",
            themename="superhero",  # Tema scuro e moderno per wizard
            size=(800, 750),
            resizable=(False, False)
        )

        # Variabili per le API keys
        self.anthropic_key = ttk.StringVar()
        self.openai_key = ttk.StringVar()
        self.google_key = ttk.StringVar()

        # Stati di validazione
        self.anthropic_tested = False
        self.openai_tested = False
        self.google_tested = False

        # Carica valori esistenti se .env esiste
        self.load_existing_env()

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"800x750+{x}+{y}")

    def load_existing_env(self):
        """Carica le API keys esistenti dal file .env"""
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Cerca le API keys
                    anthropic_match = re.search(r'ANTHROPIC_API_KEY=(.+)', content)
                    openai_match = re.search(r'OPENAI_API_KEY=(.+)', content)
                    google_match = re.search(r'GOOGLE_API_KEY=(.+)', content)

                    if anthropic_match and not anthropic_match.group(1).startswith('your_'):
                        self.anthropic_key.set(anthropic_match.group(1).strip())

                    if openai_match and not openai_match.group(1).startswith('your_'):
                        self.openai_key.set(openai_match.group(1).strip())

                    if google_match and not google_match.group(1).startswith('your_'):
                        self.google_key.set(google_match.group(1).strip())

            except Exception as e:
                print(f"Errore durante il caricamento del file .env: {e}")

    def setup_ui(self):
        """Crea l'interfaccia utente"""

        # ============================================
        # HEADER
        # ============================================
        header_frame = ttk.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X)

        header_content = ttk.Frame(header_frame, bootstyle="primary")
        header_content.pack(pady=30)

        ttk.Label(
            header_content,
            text="🚀 Configurazione Iniziale",
            font=("Segoe UI", 28, "bold"),
            bootstyle="inverse-primary"
        ).pack()

        ttk.Label(
            header_content,
            text="LinkedIn Content Helper",
            font=("Segoe UI", 14),
            bootstyle="inverse-primary"
        ).pack(pady=(10, 0))

        # ============================================
        # INTRO
        # ============================================
        intro_frame = ttk.Frame(self.root)
        intro_frame.pack(fill=X, padx=30, pady=20)

        ttk.Label(
            intro_frame,
            text="Benvenuto! Configura le tue API keys per iniziare.",
            font=("Segoe UI", 12),
            bootstyle="secondary"
        ).pack()

        ttk.Label(
            intro_frame,
            text="Le API keys sono necessarie per generare contenuti AI per LinkedIn.",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        ).pack(pady=(5, 0))

        # Separatore
        ttk.Separator(self.root, bootstyle="secondary").pack(fill=X, padx=30, pady=10)

        # ============================================
        # API KEYS SECTION
        # ============================================
        keys_container = ttk.Frame(self.root)
        keys_container.pack(fill=BOTH, expand=True, padx=30, pady=10)

        # Anthropic API Key (Obbligatorio)
        self.create_api_key_card(
            keys_container,
            title="Anthropic Claude API Key",
            badge="OBBLIGATORIA",
            badge_style="danger",
            description="Usata per generare il testo dei post LinkedIn.\n"
                       "Ottienila da: https://console.anthropic.com/account/keys",
            variable=self.anthropic_key,
            test_command=self.test_anthropic_key,
            test_attr="anthropic_tested"
        )

        # OpenAI API Key (Obbligatorio)
        self.create_api_key_card(
            keys_container,
            title="OpenAI API Key",
            badge="OBBLIGATORIA",
            badge_style="danger",
            description="Usata per generare immagini con DALL-E 3.\n"
                       "Ottienila da: https://platform.openai.com/api-keys",
            variable=self.openai_key,
            test_command=self.test_openai_key,
            test_attr="openai_tested"
        )

        # Google Gemini API Key (Opzionale)
        self.create_api_key_card(
            keys_container,
            title="Google Gemini API Key",
            badge="OPZIONALE",
            badge_style="secondary",
            description="Usata come alternativa per generare immagini.\n"
                       "Ottienila da: https://makersuite.google.com/app/apikey",
            variable=self.google_key,
            test_command=self.test_google_key,
            test_attr="google_tested"
        )

        # ============================================
        # FOOTER - Buttons
        # ============================================
        ttk.Separator(self.root, bootstyle="secondary").pack(fill=X, padx=30, pady=15)

        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=X, padx=30, pady=(0, 25))

        ttk.Button(
            footer_frame,
            text="💾 Salva e Continua",
            command=self.save_and_continue,
            bootstyle="success",
            width=20
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            footer_frame,
            text="❌ Annulla",
            command=self.cancel,
            bootstyle="danger-outline",
            width=15
        ).pack(side=RIGHT, padx=5)

        # Info footer
        ttk.Label(
            footer_frame,
            text="Le API keys verranno salvate nel file .env (non condiviso pubblicamente)",
            font=("Segoe UI", 8),
            bootstyle="secondary"
        ).pack(side=RIGHT, padx=20)

    def create_api_key_card(self, parent, title, badge, badge_style, description, variable, test_command, test_attr):
        """
        Crea una card moderna per inserire una API key

        Args:
            parent: Widget padre
            title: Titolo della card
            badge: Testo badge (OBBLIGATORIA/OPZIONALE)
            badge_style: Stile bootstrap del badge
            description: Descrizione della key
            variable: StringVar per la key
            test_command: Comando per testare la key
            test_attr: Nome attributo per stato test
        """
        # Card frame
        card = ttk.Labelframe(
            parent,
            text="",
            bootstyle=badge_style,
            padding=20
        )
        card.pack(fill=X, pady=10)

        # Header con titolo e badge
        header = ttk.Frame(card)
        header.pack(fill=X, pady=(0, 10))

        ttk.Label(
            header,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bootstyle="light"
        ).pack(side=LEFT)

        ttk.Label(
            header,
            text=badge,
            font=("Segoe UI", 9, "bold"),
            bootstyle=f"inverse-{badge_style}",
            padding=(8, 4)
        ).pack(side=RIGHT)

        # Descrizione
        ttk.Label(
            card,
            text=description,
            font=("Segoe UI", 9),
            bootstyle="secondary",
            wraplength=700
        ).pack(fill=X, pady=(0, 15))

        # Entry container
        entry_container = ttk.Frame(card)
        entry_container.pack(fill=X)

        # Entry field
        entry_frame = ttk.Frame(entry_container)
        entry_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        entry = ttk.Entry(
            entry_frame,
            textvariable=variable,
            font=("Consolas", 10),
            show="•",
            bootstyle="light"
        )
        entry.pack(fill=X)

        # Pulsanti container
        buttons_frame = ttk.Frame(entry_container)
        buttons_frame.pack(side=RIGHT)

        # Pulsante mostra/nascondi
        show_var = ttk.BooleanVar(value=False)

        def toggle_visibility():
            if show_var.get():
                entry.config(show="")
                toggle_btn.config(text="👁️")
            else:
                entry.config(show="•")
                toggle_btn.config(text="👁️‍🗨️")
            show_var.set(not show_var.get())

        toggle_btn = ttk.Button(
            buttons_frame,
            text="👁️‍🗨️",
            command=toggle_visibility,
            bootstyle="secondary-outline",
            width=5
        )
        toggle_btn.pack(side=LEFT, padx=5)

        # Pulsante test
        test_btn = ttk.Button(
            buttons_frame,
            text="🧪 Test",
            command=test_command,
            bootstyle="info",
            width=12
        )
        test_btn.pack(side=LEFT)

        # Status label (apparirà dopo test)
        status_label = ttk.Label(
            card,
            text="",
            font=("Segoe UI", 9, "italic"),
            bootstyle="secondary"
        )
        status_label.pack(pady=(10, 0))

        # Salva riferimento per aggiornamenti
        setattr(self, f"{test_attr}_label", status_label)

    def validate_api_key(self, key, name, required=True):
        """Valida formato API key"""
        if not key and required:
            Messagebox.show_error(
                f"{name} è obbligatoria!",
                "Errore Validazione",
                parent=self.root
            )
            return False

        if key and (key.startswith('your_') or len(key) < 20):
            Messagebox.show_error(
                f"{name} non sembra valida!\nInserisci una chiave reale.",
                "Errore Validazione",
                parent=self.root
            )
            return False

        return True

    def test_anthropic_key(self):
        """Testa la chiave Anthropic"""
        key = self.anthropic_key.get().strip()

        if not key:
            Messagebox.show_warning(
                "Inserisci prima la chiave Anthropic!",
                "Test API",
                parent=self.root
            )
            return

        # Mostra status in corso
        self.anthropic_tested_label.config(
            text="⏳ Test in corso...",
            bootstyle="warning"
        )
        self.root.update()

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=key)

            # Test rapido
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )

            if response:
                self.anthropic_tested = True
                self.anthropic_tested_label.config(
                    text="✅ Chiave valida e funzionante!",
                    bootstyle="success"
                )
                Messagebox.show_info(
                    "Chiave Anthropic valida e funzionante!",
                    "Test Successo",
                    parent=self.root
                )

        except Exception as e:
            self.anthropic_tested = False
            self.anthropic_tested_label.config(
                text=f"❌ Test fallito: {str(e)[:50]}...",
                bootstyle="danger"
            )
            Messagebox.show_error(
                f"Chiave Anthropic non valida:\n\n{str(e)[:200]}",
                "Test Fallito",
                parent=self.root
            )

    def test_openai_key(self):
        """Testa la chiave OpenAI"""
        key = self.openai_key.get().strip()

        if not key:
            Messagebox.show_warning(
                "Inserisci prima la chiave OpenAI!",
                "Test API",
                parent=self.root
            )
            return

        # Mostra status in corso
        self.openai_tested_label.config(
            text="⏳ Test in corso...",
            bootstyle="warning"
        )
        self.root.update()

        try:
            import openai
            client = openai.OpenAI(api_key=key)

            # Test rapido (lista modelli)
            models = client.models.list()

            if models:
                self.openai_tested = True
                self.openai_tested_label.config(
                    text="✅ Chiave valida e funzionante!",
                    bootstyle="success"
                )
                Messagebox.show_info(
                    "Chiave OpenAI valida e funzionante!",
                    "Test Successo",
                    parent=self.root
                )

        except Exception as e:
            self.openai_tested = False
            self.openai_tested_label.config(
                text=f"❌ Test fallito: {str(e)[:50]}...",
                bootstyle="danger"
            )
            Messagebox.show_error(
                f"Chiave OpenAI non valida:\n\n{str(e)[:200]}",
                "Test Fallito",
                parent=self.root
            )

    def test_google_key(self):
        """Testa la chiave Google"""
        key = self.google_key.get().strip()

        if not key:
            Messagebox.show_warning(
                "Inserisci prima la chiave Google!",
                "Test API",
                parent=self.root
            )
            return

        # Mostra status in corso
        self.google_tested_label.config(
            text="⏳ Test in corso...",
            bootstyle="warning"
        )
        self.root.update()

        try:
            from google import genai
            genai.configure(api_key=key)
            client = genai.Client()

            # Test rapido
            response = client.models.list()

            if response:
                self.google_tested = True
                self.google_tested_label.config(
                    text="✅ Chiave valida e funzionante!",
                    bootstyle="success"
                )
                Messagebox.show_info(
                    "Chiave Google Gemini valida e funzionante!",
                    "Test Successo",
                    parent=self.root
                )

        except Exception as e:
            self.google_tested = False
            self.google_tested_label.config(
                text=f"❌ Test fallito: {str(e)[:50]}...",
                bootstyle="danger"
            )
            Messagebox.show_error(
                f"Chiave Google non valida:\n\n{str(e)[:200]}",
                "Test Fallito",
                parent=self.root
            )

    def save_and_continue(self):
        """Salva le configurazioni e chiude"""
        # Valida le chiavi obbligatorie
        anthropic = self.anthropic_key.get().strip()
        openai = self.openai_key.get().strip()
        google = self.google_key.get().strip()

        if not self.validate_api_key(anthropic, "Anthropic API Key", required=True):
            return

        if not self.validate_api_key(openai, "OpenAI API Key", required=True):
            return

        # Avviso se non sono state testate
        if not self.anthropic_tested or not self.openai_tested:
            result = Messagebox.yesno(
                "Non hai testato tutte le chiavi obbligatorie!\n\n"
                "Vuoi salvare comunque?\n"
                "(Le chiavi potrebbero non funzionare)",
                "Conferma Salvataggio",
                parent=self.root
            )

            if result != "Yes":
                return

        # Salva nel file .env
        try:
            # Leggi template da .env.example se esiste
            env_example = Path(".env.example")
            if env_example.exists():
                with open(env_example, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                # Template base se .env.example non esiste
                content = """# LinkedIn Content Helper - API Keys

ANTHROPIC_API_KEY=your_anthropic_key_here
CLAUDE_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
# GOOGLE_API_KEY=your_google_key_here
"""

            # Sostituisci le chiavi
            content = re.sub(r'ANTHROPIC_API_KEY=.+', f'ANTHROPIC_API_KEY={anthropic}', content)
            content = re.sub(r'CLAUDE_API_KEY=.+', f'CLAUDE_API_KEY={anthropic}', content)
            content = re.sub(r'OPENAI_API_KEY=.+', f'OPENAI_API_KEY={openai}', content)

            if google:
                # Se c'è la chiave Google, assicurati che sia decommentata
                if '# GOOGLE_API_KEY=' in content:
                    content = content.replace('# GOOGLE_API_KEY=', 'GOOGLE_API_KEY=')
                content = re.sub(r'GOOGLE_API_KEY=.+', f'GOOGLE_API_KEY={google}', content)

            # Salva
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)

            Messagebox.show_info(
                "✅ Configurazione salvata con successo!\n\n"
                "Le API keys sono state salvate nel file .env\n"
                "Ora puoi usare l'applicazione.",
                "Successo",
                parent=self.root
            )

            self.root.quit()

        except Exception as e:
            Messagebox.show_error(
                f"Impossibile salvare la configurazione:\n\n{e}",
                "Errore Salvataggio",
                parent=self.root
            )

    def cancel(self):
        """Annulla la configurazione"""
        result = Messagebox.yesno(
            "Vuoi annullare la configurazione?\n\n"
            "Dovrai configurare manualmente il file .env",
            "Conferma Annullamento",
            parent=self.root
        )

        if result == "Yes":
            self.root.quit()

    def run(self):
        """Avvia l'interfaccia"""
        self.root.mainloop()


def main():
    """Funzione principale"""
    app = FirstRunConfigGUI()
    app.run()


if __name__ == "__main__":
    main()
