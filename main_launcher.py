# main_launcher.py
"""
LinkedIn Content Helper - Main Launcher (Modernized with ttkbootstrap)
Hub centrale per accedere a tutte le funzionalità dell'applicazione
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import subprocess
import os
import sys


class MainLauncher:
    def __init__(self):
        # Crea finestra principale con tema moderno
        self.root = ttk.Window(
            title="LinkedIn Content Helper",
            themename="cosmo",  # Tema moderno e pulito
            size=(900, 700),
            resizable=(True, True)
        )
        self.root.minsize(800, 600)

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")

    def setup_ui(self):
        """Crea l'interfaccia utente moderna"""

        # ============================================
        # HEADER
        # ============================================
        header_frame = ttk.Frame(self.root, bootstyle="dark")
        header_frame.pack(fill=X, pady=0)

        # Titolo con icona
        title_container = ttk.Frame(header_frame, bootstyle="dark")
        title_container.pack(pady=30)

        title_label = ttk.Label(
            title_container,
            text="🤖 AI Content Helper",
            font=("Segoe UI", 32, "bold"),
            bootstyle="inverse-dark"
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_container,
            text="Generatore Automatico di Contenuti LinkedIn con AI",
            font=("Segoe UI", 12),
            bootstyle="inverse-dark"
        )
        subtitle_label.pack(pady=(10, 0))

        # Separatore decorativo
        separator = ttk.Separator(self.root, bootstyle="primary")
        separator.pack(fill=X, padx=50, pady=20)

        # ============================================
        # MAIN CONTENT - Cards Container
        # ============================================
        main_container = ttk.Frame(self.root)
        main_container.pack(expand=True, fill=BOTH, padx=40, pady=20)

        # Grid di cards (2 colonne)
        # Row 1: Pannello Controllo | App Manuale
        self.create_feature_card(
            main_container,
            row=0, column=0,
            title="🎛️ Pannello di Controllo",
            description="Gestisci l'automazione giornaliera, configura fonti RSS, visualizza log e monitora lo status del sistema",
            button_text="Apri Pannello",
            button_style="success",
            command=self.open_control_panel
        )

        self.create_feature_card(
            main_container,
            row=0, column=1,
            title="📰 Generazione Manuale",
            description="Interfaccia originale per selezionare manualmente articoli e generare post singoli on-demand",
            button_text="Apri App",
            button_style="info",
            command=self.open_original_app
        )

        # Row 2: Test Automazione | Apri Cartella
        self.create_feature_card(
            main_container,
            row=1, column=0,
            title="🧪 Test Automazione",
            description="Esegui un test completo del sistema di automazione con le impostazioni correnti",
            button_text="Esegui Test",
            button_style="warning",
            command=self.run_automation_test
        )

        self.create_feature_card(
            main_container,
            row=1, column=1,
            title="📁 Post Generati",
            description="Accedi rapidamente alla cartella contenente tutti i post generati dall'applicazione",
            button_text="Apri Cartella",
            button_style="secondary",
            command=self.open_posts_folder
        )

        # ============================================
        # FOOTER - Action Buttons
        # ============================================
        separator2 = ttk.Separator(self.root, bootstyle="secondary")
        separator2.pack(fill=X, padx=50, pady=20)

        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=X, padx=40, pady=(0, 30))

        # Pulsanti secondari con icone
        help_button = ttk.Button(
            footer_frame,
            text="❓ Guida",
            command=self.show_help,
            bootstyle="info-outline",
            width=15
        )
        help_button.pack(side=LEFT, padx=5)

        config_button = ttk.Button(
            footer_frame,
            text="⚙️ Configurazione",
            command=self.open_config,
            bootstyle="secondary-outline",
            width=18
        )
        config_button.pack(side=LEFT, padx=5)

        # Pulsante esci a destra
        exit_button = ttk.Button(
            footer_frame,
            text="🚪 Esci",
            command=self.root.quit,
            bootstyle="danger-outline",
            width=12
        )
        exit_button.pack(side=RIGHT, padx=5)

        # Info version
        version_label = ttk.Label(
            footer_frame,
            text="v2.0 | Powered by Claude AI & OpenAI",
            font=("Segoe UI", 8),
            bootstyle="secondary"
        )
        version_label.pack(side=RIGHT, padx=20)

    def create_feature_card(self, parent, row, column, title, description, button_text, button_style, command):
        """
        Crea una card moderna per una feature

        Args:
            parent: Widget padre
            row: Riga nella grid
            column: Colonna nella grid
            title: Titolo della card
            description: Descrizione della feature
            button_text: Testo del pulsante
            button_style: Stile bootstrap del pulsante
            command: Comando da eseguire al click
        """
        # Frame card con bordo
        card_frame = ttk.Labelframe(
            parent,
            text="",
            bootstyle="secondary",
            padding=20
        )
        card_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")

        # Configura grid weights per espansione uniforme
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(column, weight=1)

        # Titolo card
        title_label = ttk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=(0, 15))

        # Descrizione
        desc_label = ttk.Label(
            card_frame,
            text=description,
            font=("Segoe UI", 10),
            wraplength=320,
            justify=CENTER
        )
        desc_label.pack(pady=(0, 20))

        # Pulsante azione
        action_button = ttk.Button(
            card_frame,
            text=button_text,
            command=command,
            bootstyle=button_style,
            width=20
        )
        action_button.pack(pady=10)

    def open_control_panel(self):
        """Apre il pannello di controllo"""
        try:
            subprocess.Popen([sys.executable, "control_panel.py"])
            self.root.iconify()  # Minimizza il launcher
        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Impossibile aprire il pannello di controllo:\n\n{e}",
                parent=self.root
            )

    def open_original_app(self):
        """Apre l'app originale"""
        try:
            subprocess.Popen([sys.executable, "new_fetcher.py"])
            self.root.iconify()  # Minimizza il launcher
        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Impossibile aprire l'app originale:\n\n{e}",
                parent=self.root
            )

    def run_automation_test(self):
        """Esegue test automazione"""
        result = messagebox.askyesno(
            "Test Automazione",
            "Vuoi eseguire un test dell'automazione?\n\n"
            "Questo genererà post reali con le impostazioni attuali.\n"
            "Il processo potrebbe richiedere alcuni minuti.",
            parent=self.root
        )

        if result:
            try:
                # Nascondi finestra durante test
                self.root.withdraw()

                # Cerca python del venv
                venv_python = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'venv',
                    'Scripts',
                    'python.exe'
                )

                if os.path.exists(venv_python):
                    result = subprocess.run(
                        [venv_python, "automation_test.py"],
                        capture_output=True,
                        text=True
                    )
                else:
                    result = subprocess.run(
                        [sys.executable, "daily_ai_automation.py"],
                        capture_output=True,
                        text=True
                    )

                # Mostra finestra
                self.root.deiconify()

                if result.returncode == 0:
                    messagebox.showinfo(
                        "Test Completato",
                        "✅ Test automazione completato con successo!\n\n"
                        "Controlla la cartella generated_posts per i risultati.",
                        parent=self.root
                    )
                else:
                    messagebox.showerror(
                        "Test Fallito",
                        f"❌ Test fallito:\n\n{result.stderr}",
                        parent=self.root
                    )

            except Exception as e:
                self.root.deiconify()
                messagebox.showerror(
                    "Errore",
                    f"Errore durante il test:\n\n{e}",
                    parent=self.root
                )

    def open_posts_folder(self):
        """Apre cartella post generati"""
        posts_dir = "generated_posts"

        if os.path.exists(posts_dir):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(posts_dir)
                else:  # Linux/Mac
                    subprocess.run(["xdg-open", posts_dir])
            except Exception as e:
                messagebox.showerror(
                    "Errore",
                    f"Impossibile aprire la cartella:\n\n{e}",
                    parent=self.root
                )
        else:
            messagebox.showwarning(
                "Attenzione",
                "Cartella post non trovata!\n\n"
                "Esegui prima un test per generare dei post.",
                parent=self.root
            )

    def open_config(self):
        """Apre file di configurazione"""
        config_file = "automation_config.json"

        if os.path.exists(config_file):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(config_file)
                else:  # Linux/Mac
                    subprocess.run(["xdg-open", config_file])
            except Exception as e:
                messagebox.showerror(
                    "Errore",
                    f"Impossibile aprire il file di configurazione:\n\n{e}",
                    parent=self.root
                )
        else:
            messagebox.showwarning(
                "Attenzione",
                "File di configurazione non trovato!",
                parent=self.root
            )

    def show_help(self):
        """Mostra guida rapida"""
        help_window = ttk.Toplevel(self.root)
        help_window.title("Guida AI Content Helper")
        help_window.geometry("700x600")

        # Centra la finestra di aiuto
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (help_window.winfo_screenheight() // 2) - (600 // 2)
        help_window.geometry(f"700x600+{x}+{y}")

        # Header
        header = ttk.Frame(help_window, bootstyle="primary")
        header.pack(fill=X)

        title = ttk.Label(
            header,
            text="📖 Guida Rapida",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=20)

        # Contenuto scrollabile
        text_frame = ttk.Frame(help_window, padding=20)
        text_frame.pack(fill=BOTH, expand=True)

        scrolled_text = ttk.ScrolledText(
            text_frame,
            wrap="word",
            font=("Segoe UI", 10),
            autohide=True
        )
        scrolled_text.pack(fill=BOTH, expand=True)

        help_text = """
🎛️ PANNELLO DI CONTROLLO

Il pannello di controllo è il cuore dell'automazione. Da qui puoi:

• Abilitare/disabilitare l'automazione giornaliera
• Gestire le fonti RSS (aggiungere, rimuovere, testare)
• Configurare orario di esecuzione e numero di post al giorno
• Visualizzare log e monitorare lo status del sistema
• Eseguire test manuali dell'automazione


📰 GENERAZIONE MANUALE

L'interfaccia originale per creare post singoli:

• Visualizza lista articoli recenti da tutti i feed RSS
• Seleziona manualmente l'articolo che ti interessa
• Genera un post personalizzato on-demand
• Controllo completo sul processo di generazione


🧪 TEST AUTOMAZIONE

Verifica che tutto funzioni correttamente:

• Esegue l'intero processo di automazione una volta
• Genera post reali con le impostazioni correnti
• Utile per testare dopo aver modificato la configurazione
• I post vengono salvati in generated_posts/


📁 POST GENERATI

Accesso rapido ai contenuti creati:

• Apre la cartella generated_posts/
• I post sono organizzati per data: YYYY/MM/DD/
• Ogni post include file .docx (testo) e .png (immagine)


⚙️ CONFIGURAZIONE

File automation_config.json contiene:

• schedule: orario e numero post giornalieri
• ai_sources: lista feed RSS da monitorare
• Modificabile manualmente o tramite il pannello


📊 AUTOMAZIONE GIORNALIERA

Come funziona:

1. Raccolta: scarica articoli da tutti i feed RSS
2. Filtraggio: cerca keyword AI/ML rilevanti
3. Scoring: assegna punteggi per freshness + relevance
4. Selezione: sceglie i migliori N articoli
5. Generazione: crea post con Claude AI
6. Immagini: genera copertine con DALL-E 3
7. Salvataggio: organizza tutto per data


💡 SUGGERIMENTI

• Esegui un test prima di attivare l'automazione
• Controlla regolarmente i log per eventuali errori
• Aggiungi feed RSS specifici al tuo settore
• Personalizza i prompt in daily_ai_automation.py


🔑 API KEYS

Le chiavi API sono nel file .env:

• ANTHROPIC_API_KEY: per generazione testo (obbligatoria)
• OPENAI_API_KEY: per generazione immagini (obbligatoria)
• GOOGLE_API_KEY: alternativa immagini (opzionale)


❓ SUPPORTO

In caso di problemi:

1. Controlla i log in logs/
2. Verifica le API keys nel file .env
3. Testa la connessione internet
4. Esegui automation_test.py per diagnostica


💾 COSTI

Stima per post completo:

• Claude (testo): ~$0.015
• DALL-E 3 (immagine): ~$0.040
• Totale: ~$0.055 per post

Con 2 post/giorno: ~$3.30/mese
"""

        scrolled_text.insert("1.0", help_text)
        scrolled_text.configure(state="disabled")

        # Pulsante chiudi
        close_button = ttk.Button(
            help_window,
            text="Chiudi",
            command=help_window.destroy,
            bootstyle="secondary",
            width=15
        )
        close_button.pack(pady=15)

    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainLauncher()
    app.run()
