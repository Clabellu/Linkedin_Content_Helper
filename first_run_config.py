# first_run_config.py
"""
Configurazione guidata per il primo avvio dell'applicazione.
Permette di configurare le API keys in modo semplice e user-friendly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
from pathlib import Path


class FirstRunConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LinkedIn Content Helper - Configurazione Iniziale")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # Variabili per le API keys
        self.anthropic_key = tk.StringVar()
        self.openai_key = tk.StringVar()
        self.google_key = tk.StringVar()

        # Carica valori esistenti se .env esiste
        self.load_existing_env()

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"700x650+{x}+{y}")

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
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🤖 Configurazione LinkedIn Content Helper",
                              font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=25)

        # Main content
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Intro text
        intro_text = tk.Label(main_frame,
                             text="Benvenuto! Configura le tue API keys per iniziare a usare l'applicazione.\n"
                                  "Le API keys sono necessarie per generare contenuti AI per LinkedIn.",
                             font=("Arial", 10), bg="#ecf0f1", justify="left", wraplength=650)
        intro_text.pack(pady=(0, 15))

        # Anthropic API Key (Obbligatorio)
        self.create_api_key_section(
            main_frame,
            title="Anthropic Claude API Key (Obbligatorio)",
            description="Usata per generare il testo dei post LinkedIn.\n"
                       "Ottienila da: https://console.anthropic.com/account/keys",
            variable=self.anthropic_key,
            required=True,
            test_command=self.test_anthropic_key
        )

        # OpenAI API Key (Obbligatorio)
        self.create_api_key_section(
            main_frame,
            title="OpenAI API Key (Obbligatorio)",
            description="Usata per generare immagini con DALL-E 3.\n"
                       "Ottienila da: https://platform.openai.com/api-keys",
            variable=self.openai_key,
            required=True,
            test_command=self.test_openai_key
        )

        # Google Gemini API Key (Opzionale)
        self.create_api_key_section(
            main_frame,
            title="Google Gemini API Key (Opzionale)",
            description="Usata come alternativa per generare immagini.\n"
                       "Ottienila da: https://makersuite.google.com/app/apikey",
            variable=self.google_key,
            required=False,
            test_command=self.test_google_key
        )

        # Buttons
        button_frame = tk.Frame(self.root, bg="#ecf0f1")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        save_button = tk.Button(button_frame, text="💾 Salva e Continua",
                               command=self.save_and_continue,
                               bg="#27ae60", fg="white",
                               font=("Arial", 12, "bold"),
                               padx=20, pady=10)
        save_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="❌ Annulla",
                                 command=self.cancel,
                                 bg="#e74c3c", fg="white",
                                 font=("Arial", 12, "bold"),
                                 padx=20, pady=10)
        cancel_button.pack(side="right", padx=5)

        # Footer info
        footer_text = tk.Label(self.root,
                              text="Le API keys verranno salvate nel file .env (non condiviso pubblicamente)",
                              font=("Arial", 8), fg="#7f8c8d", bg="#ecf0f1")
        footer_text.pack(pady=(0, 10))

    def create_api_key_section(self, parent, title, description, variable, required, test_command):
        """Crea una sezione per inserire una API key"""
        # Frame principale
        section_frame = tk.LabelFrame(parent, text=title, font=("Arial", 10, "bold"),
                                     bg="#ecf0f1", padx=10, pady=10)
        section_frame.pack(fill="x", pady=5)

        # Descrizione
        desc_label = tk.Label(section_frame, text=description,
                             font=("Arial", 9), bg="#ecf0f1",
                             justify="left", anchor="w")
        desc_label.pack(fill="x", pady=(0, 5))

        # Entry e pulsante test
        entry_frame = tk.Frame(section_frame, bg="#ecf0f1")
        entry_frame.pack(fill="x", pady=5)

        # Badge "Obbligatorio/Opzionale"
        if required:
            badge = tk.Label(entry_frame, text="OBBLIGATORIO", bg="#e74c3c", fg="white",
                           font=("Arial", 8, "bold"), padx=5, pady=2)
        else:
            badge = tk.Label(entry_frame, text="OPZIONALE", bg="#95a5a6", fg="white",
                           font=("Arial", 8, "bold"), padx=5, pady=2)
        badge.pack(side="left", padx=(0, 5))

        # Entry
        entry = tk.Entry(entry_frame, textvariable=variable, font=("Consolas", 9),
                        show="*", width=50)
        entry.pack(side="left", fill="x", expand=True, padx=5)

        # Pulsante mostra/nascondi
        def toggle_visibility():
            if entry.cget('show') == '*':
                entry.config(show='')
                toggle_btn.config(text="👁️")
            else:
                entry.config(show='*')
                toggle_btn.config(text="👁️‍🗨️")

        toggle_btn = tk.Button(entry_frame, text="👁️‍🗨️", command=toggle_visibility,
                              font=("Arial", 10), width=3)
        toggle_btn.pack(side="left", padx=2)

        # Pulsante test
        test_btn = tk.Button(entry_frame, text="🧪 Test", command=test_command,
                           bg="#3498db", fg="white", font=("Arial", 9, "bold"), width=8)
        test_btn.pack(side="left", padx=2)

    def validate_api_key(self, key, name, required=True):
        """Valida formato API key"""
        if not key and required:
            messagebox.showerror("Errore", f"{name} è obbligatoria!")
            return False

        if key and (key.startswith('your_') or len(key) < 20):
            messagebox.showerror("Errore", f"{name} non sembra valida!\nInserisci una chiave reale.")
            return False

        return True

    def test_anthropic_key(self):
        """Testa la chiave Anthropic"""
        key = self.anthropic_key.get().strip()

        if not key:
            messagebox.showwarning("Test API", "Inserisci prima la chiave Anthropic!")
            return

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
                messagebox.showinfo("Test Successo", "✅ Chiave Anthropic valida e funzionante!")

        except Exception as e:
            messagebox.showerror("Test Fallito", f"❌ Chiave Anthropic non valida:\n\n{str(e)[:200]}")

    def test_openai_key(self):
        """Testa la chiave OpenAI"""
        key = self.openai_key.get().strip()

        if not key:
            messagebox.showwarning("Test API", "Inserisci prima la chiave OpenAI!")
            return

        try:
            import openai
            client = openai.OpenAI(api_key=key)

            # Test rapido (lista modelli)
            models = client.models.list()

            if models:
                messagebox.showinfo("Test Successo", "✅ Chiave OpenAI valida e funzionante!")

        except Exception as e:
            messagebox.showerror("Test Fallito", f"❌ Chiave OpenAI non valida:\n\n{str(e)[:200]}")

    def test_google_key(self):
        """Testa la chiave Google"""
        key = self.google_key.get().strip()

        if not key:
            messagebox.showwarning("Test API", "Inserisci prima la chiave Google!")
            return

        try:
            from google import genai
            genai.configure(api_key=key)
            client = genai.Client()

            # Test rapido
            response = client.models.list()

            if response:
                messagebox.showinfo("Test Successo", "✅ Chiave Google Gemini valida e funzionante!")

        except Exception as e:
            messagebox.showerror("Test Fallito", f"❌ Chiave Google non valida:\n\n{str(e)[:200]}")

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

            messagebox.showinfo("Successo",
                              "✅ Configurazione salvata con successo!\n\n"
                              "Le API keys sono state salvate nel file .env\n"
                              "Ora puoi usare l'applicazione.")

            self.root.quit()

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile salvare la configurazione:\n\n{e}")

    def cancel(self):
        """Annulla la configurazione"""
        result = messagebox.askyesno("Conferma",
                                    "Vuoi annullare la configurazione?\n\n"
                                    "Dovrai configurare manualmente il file .env")
        if result:
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
