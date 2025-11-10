# control_panel.py
"""
LinkedIn Content Helper - Control Panel (Modernized with ttkbootstrap)
Dashboard completa per gestire automazione, RSS, configurazione e log
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
import json
import sys
import os
import subprocess
import threading
from datetime import datetime


class AIContentControlPanel:
    def __init__(self):
        # Crea finestra principale con tema moderno
        self.root = ttk.Window(
            title="AI Content Helper - Pannello di Controllo",
            themename="flatly",  # Tema moderno e professionale
            size=(1100, 750),
            resizable=(True, True)
        )

        self.config_file = "automation_config.json"
        self.load_config()
        self.setup_ui()
        self.update_status()
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"1100x750+{x}+{y}")

    def load_config(self):
        """Carica configurazione da file JSON"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Configurazione default se file non esiste
            self.config = {
                "schedule": {
                    "execution_time": "08:00",
                    "posts_per_day": 2,
                    "enabled": True
                },
                "ai_sources": {
                    "rss_feeds": [
                        "https://feeds.feedburner.com/oreilly/radar",
                        "https://www.wired.com/feed/tag/ai/latest/rss"
                    ]
                }
            }
            self.save_config()

    def save_config(self):
        """Salva configurazione su file JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Messagebox.show_error(
                f"Impossibile salvare configurazione:\n{e}",
                "Errore Salvataggio",
                parent=self.root
            )
            return False

    def setup_ui(self):
        """Crea l'interfaccia utente moderna"""

        # ============================================
        # HEADER
        # ============================================
        header_frame = ttk.Frame(self.root, bootstyle="primary")
        header_frame.pack(fill=X)

        header_content = ttk.Frame(header_frame, bootstyle="primary")
        header_content.pack(pady=20, padx=30)

        title_label = ttk.Label(
            header_content,
            text="🎛️ Pannello di Controllo",
            font=("Segoe UI", 26, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(side=LEFT)

        # Status indicator (aggiornato dinamicamente)
        self.header_status_label = ttk.Label(
            header_content,
            text="",
            font=("Segoe UI", 12, "bold"),
            bootstyle="inverse-primary"
        )
        self.header_status_label.pack(side=RIGHT, padx=20)

        # ============================================
        # NOTEBOOK con TAB
        # ============================================
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11))

        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=15, pady=15)

        # Tab Dashboard
        self.create_dashboard_tab()

        # Tab Fonti RSS
        self.create_rss_tab()

        # Tab Configurazione
        self.create_config_tab()

        # Tab Log
        self.create_log_tab()

        # ============================================
        # STATUS BAR
        # ============================================
        self.status_bar = ttk.Label(
            self.root,
            text="Pronto",
            relief=SUNKEN,
            anchor=W,
            bootstyle="secondary",
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(side=BOTTOM, fill=X)

    def create_dashboard_tab(self):
        """Crea tab dashboard con status e controlli"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="  📊 Dashboard  ")

        # Scrollable container
        scrolled = ScrolledFrame(dashboard_frame, autohide=True)
        scrolled.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ============================================
        # STATUS AUTOMAZIONE - Card
        # ============================================
        status_card = ttk.Labelframe(
            scrolled,
            text="Status Automazione",
            bootstyle="success",
            padding=20
        )
        status_card.pack(fill=X, padx=10, pady=10)

        status_content = ttk.Frame(status_card)
        status_content.pack(fill=X)

        # Meter circolare per status (usa Label per ora, ttkbootstrap ha Meter widget)
        status_left = ttk.Frame(status_content)
        status_left.pack(side=LEFT, fill=BOTH, expand=True)

        self.status_icon_label = ttk.Label(
            status_left,
            text="🟢",
            font=("Segoe UI", 72)
        )
        self.status_icon_label.pack(pady=10)

        self.status_text_label = ttk.Label(
            status_left,
            text="AUTOMAZIONE ATTIVA",
            font=("Segoe UI", 16, "bold"),
            bootstyle="success"
        )
        self.status_text_label.pack()

        # Toggle button
        self.toggle_button = ttk.Button(
            status_left,
            text="🔴 Disabilita Automazione",
            command=self.toggle_automation,
            bootstyle="danger",
            width=25
        )
        self.toggle_button.pack(pady=15)

        # Info status
        status_right = ttk.Frame(status_content)
        status_right.pack(side=RIGHT, fill=BOTH, expand=True, padx=30)

        self.info_text = ttk.Text(
            status_right,
            height=10,
            font=("Segoe UI", 11),
            wrap=WORD
        )
        self.info_text.pack(fill=BOTH, expand=True)

        # ============================================
        # AZIONI RAPIDE - Card
        # ============================================
        actions_card = ttk.Labelframe(
            scrolled,
            text="Azioni Rapide",
            bootstyle="info",
            padding=20
        )
        actions_card.pack(fill=X, padx=10, pady=10)

        actions_grid = ttk.Frame(actions_card)
        actions_grid.pack(fill=X)

        # Grid 2x2 di pulsanti
        ttk.Button(
            actions_grid,
            text="🧪 Test Manuale",
            command=self.run_manual_test,
            bootstyle="primary",
            width=25
        ).grid(row=0, column=0, padx=10, pady=10, sticky=EW)

        ttk.Button(
            actions_grid,
            text="📋 Visualizza Log",
            command=self.show_latest_log,
            bootstyle="info",
            width=25
        ).grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        ttk.Button(
            actions_grid,
            text="📁 Apri Cartella Post",
            command=self.open_posts_folder,
            bootstyle="warning",
            width=25
        ).grid(row=1, column=0, padx=10, pady=10, sticky=EW)

        ttk.Button(
            actions_grid,
            text="🔄 Aggiorna Dashboard",
            command=self.update_status,
            bootstyle="success",
            width=25
        ).grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        actions_grid.grid_columnconfigure(0, weight=1)
        actions_grid.grid_columnconfigure(1, weight=1)

        # ============================================
        # STATISTICHE - Card
        # ============================================
        stats_card = ttk.Labelframe(
            scrolled,
            text="Statistiche",
            bootstyle="secondary",
            padding=20
        )
        stats_card.pack(fill=X, padx=10, pady=10)

        stats_grid = ttk.Frame(stats_card)
        stats_grid.pack(fill=X)

        # Stat 1: Fonti RSS
        self.create_stat_box(
            stats_grid, 0, 0,
            "📰 Fonti RSS",
            str(len(self.config['ai_sources']['rss_feeds'])),
            "info"
        )

        # Stat 2: Post per giorno
        self.create_stat_box(
            stats_grid, 0, 1,
            "📊 Post/Giorno",
            str(self.config['schedule']['posts_per_day']),
            "primary"
        )

        # Stat 3: Orario
        self.create_stat_box(
            stats_grid, 0, 2,
            "⏰ Orario",
            self.config['schedule']['execution_time'],
            "warning"
        )

        # Stat 4: Status
        enabled_text = "Attiva" if self.config['schedule'].get('enabled', True) else "Disattiva"
        enabled_style = "success" if self.config['schedule'].get('enabled', True) else "danger"
        self.create_stat_box(
            stats_grid, 0, 3,
            "🔄 Status",
            enabled_text,
            enabled_style
        )

        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1)

    def create_stat_box(self, parent, row, column, title, value, bootstyle):
        """Crea una statbox colorata"""
        frame = ttk.Frame(parent, bootstyle=bootstyle, relief=RAISED)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky=EW)

        ttk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10),
            bootstyle=f"inverse-{bootstyle}"
        ).pack(pady=(10, 5))

        ttk.Label(
            frame,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bootstyle=f"inverse-{bootstyle}"
        ).pack(pady=(0, 10))

    def create_rss_tab(self):
        """Crea tab per gestione fonti RSS"""
        rss_frame = ttk.Frame(self.notebook)
        self.notebook.add(rss_frame, text="  📰 Fonti RSS  ")

        # Top controls
        controls_frame = ttk.Frame(rss_frame)
        controls_frame.pack(fill=X, padx=15, pady=15)

        ttk.Label(
            controls_frame,
            text="Gestione Fonti RSS",
            font=("Segoe UI", 18, "bold")
        ).pack(side=LEFT)

        # Lista RSS
        list_frame = ttk.Labelframe(
            rss_frame,
            text=f"Fonti RSS Attive ({len(self.config['ai_sources']['rss_feeds'])})",
            bootstyle="info",
            padding=15
        )
        list_frame.pack(fill=BOTH, expand=True, padx=15, pady=10)

        # Listbox con scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_container, bootstyle="info-round")
        scrollbar.pack(side=RIGHT, fill=Y)

        self.rss_listbox = tk.Listbox(
            list_container,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            selectmode=SINGLE
        )
        self.rss_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.rss_listbox.yview)

        # Pulsanti gestione
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(fill=X, pady=15)

        ttk.Button(
            buttons_frame,
            text="➕ Aggiungi RSS",
            command=self.add_rss_feed,
            bootstyle="success",
            width=18
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text="➖ Rimuovi RSS",
            command=self.remove_rss_feed,
            bootstyle="danger",
            width=18
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text="🧪 Test RSS",
            command=self.test_rss_feed,
            bootstyle="info",
            width=18
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text="🔄 Aggiorna Lista",
            command=self.refresh_rss_list,
            bootstyle="secondary",
            width=18
        ).pack(side=RIGHT, padx=5)

        # Input per nuovo RSS
        input_frame = ttk.Labelframe(
            rss_frame,
            text="Aggiungi Nuovo Feed RSS",
            bootstyle="success",
            padding=15
        )
        input_frame.pack(fill=X, padx=15, pady=(0, 15))

        entry_container = ttk.Frame(input_frame)
        entry_container.pack(fill=X)

        self.rss_entry = ttk.Entry(
            entry_container,
            font=("Segoe UI", 11),
            bootstyle="success"
        )
        self.rss_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        ttk.Button(
            entry_container,
            text="🚀 Aggiungi",
            command=self.quick_add_rss,
            bootstyle="success",
            width=15
        ).pack(side=RIGHT)

        # Carica lista
        self.refresh_rss_list()

    def create_config_tab(self):
        """Crea tab per configurazione"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="  ⚙️ Configurazione  ")

        # Scrollable
        scrolled = ScrolledFrame(config_frame, autohide=True)
        scrolled.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ============================================
        # CONFIGURAZIONE BASE
        # ============================================
        basic_card = ttk.Labelframe(
            scrolled,
            text="Configurazione Base",
            bootstyle="primary",
            padding=20
        )
        basic_card.pack(fill=X, padx=10, pady=10)

        # Orario
        time_frame = ttk.Frame(basic_card)
        time_frame.pack(fill=X, pady=10)

        ttk.Label(
            time_frame,
            text="⏰ Orario Esecuzione Giornaliera:",
            font=("Segoe UI", 11, "bold")
        ).pack(side=LEFT, padx=(0, 15))

        self.time_entry = ttk.Entry(
            time_frame,
            font=("Segoe UI", 11),
            width=15,
            bootstyle="primary"
        )
        self.time_entry.pack(side=LEFT)
        self.time_entry.insert(0, self.config["schedule"]["execution_time"])

        ttk.Label(
            time_frame,
            text="(Formato: HH:MM, es. 08:00)",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(side=LEFT, padx=15)

        # Numero post
        posts_frame = ttk.Frame(basic_card)
        posts_frame.pack(fill=X, pady=10)

        ttk.Label(
            posts_frame,
            text="📊 Post per Giorno:",
            font=("Segoe UI", 11, "bold")
        ).pack(side=LEFT, padx=(0, 15))

        self.posts_spinbox = ttk.Spinbox(
            posts_frame,
            from_=1,
            to=5,
            font=("Segoe UI", 11),
            width=15,
            bootstyle="primary"
        )
        self.posts_spinbox.pack(side=LEFT)
        self.posts_spinbox.set(str(self.config["schedule"]["posts_per_day"]))

        ttk.Label(
            posts_frame,
            text="(1-5 post al giorno)",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(side=LEFT, padx=15)

        # Pulsante salva
        ttk.Button(
            basic_card,
            text="💾 Salva Configurazione Base",
            command=self.save_configuration,
            bootstyle="success",
            width=30
        ).pack(pady=20)

        # ============================================
        # CONFIGURAZIONE AVANZATA (JSON)
        # ============================================
        advanced_card = ttk.Labelframe(
            scrolled,
            text="Configurazione Avanzata (JSON)",
            bootstyle="warning",
            padding=20
        )
        advanced_card.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ttk.Label(
            advanced_card,
            text="⚠️ Modifica solo se sai cosa stai facendo!",
            font=("Segoe UI", 10, "italic"),
            bootstyle="warning"
        ).pack(pady=(0, 10))

        self.config_text = ScrolledText(
            advanced_card,
            height=15,
            font=("Consolas", 10),
            autohide=True,
            bootstyle="warning"
        )
        self.config_text.pack(fill=BOTH, expand=True, pady=10)

        # Carica configurazione
        self.load_config_text()

        # Pulsanti
        advanced_buttons = ttk.Frame(advanced_card)
        advanced_buttons.pack(fill=X, pady=10)

        ttk.Button(
            advanced_buttons,
            text="💾 Salva JSON",
            command=self.save_advanced_config,
            bootstyle="warning",
            width=20
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            advanced_buttons,
            text="🔄 Ricarica",
            command=self.load_config_text,
            bootstyle="info",
            width=20
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            advanced_buttons,
            text="♻️ Reset Default",
            command=self.reset_config,
            bootstyle="danger",
            width=20
        ).pack(side=RIGHT, padx=5)

    def create_log_tab(self):
        """Crea tab per visualizzazione log"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="  📋 Log  ")

        # Top controls
        controls_frame = ttk.Frame(log_frame)
        controls_frame.pack(fill=X, padx=15, pady=15)

        ttk.Label(
            controls_frame,
            text="Log Sistema",
            font=("Segoe UI", 18, "bold")
        ).pack(side=LEFT)

        # Pulsanti
        ttk.Button(
            controls_frame,
            text="🔄 Aggiorna",
            command=self.refresh_log,
            bootstyle="info",
            width=15
        ).pack(side=RIGHT, padx=5)

        ttk.Button(
            controls_frame,
            text="🗑️ Pulisci",
            command=self.clear_log,
            bootstyle="danger-outline",
            width=15
        ).pack(side=RIGHT, padx=5)

        # Log area
        log_container = ttk.Labelframe(
            log_frame,
            text="Log Recenti",
            bootstyle="secondary",
            padding=15
        )
        log_container.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))

        self.log_text = ScrolledText(
            log_container,
            font=("Consolas", 9),
            autohide=True,
            bootstyle="dark"
        )
        self.log_text.pack(fill=BOTH, expand=True)

        # Carica log iniziale
        self.refresh_log()

    # ============================================
    # METODI FUNZIONALI
    # ============================================

    def toggle_automation(self):
        """Abilita/disabilita automazione"""
        current_status = self.config["schedule"].get("enabled", True)
        new_status = not current_status

        self.config["schedule"]["enabled"] = new_status

        if self.save_config():
            self.update_status()
            status_msg = "abilitata" if new_status else "disabilitata"
            Messagebox.show_info(
                f"Automazione {status_msg} con successo!",
                "Successo",
                parent=self.root
            )
        else:
            # Ripristina stato precedente se salvataggio fallisce
            self.config["schedule"]["enabled"] = current_status

    def update_status(self):
        """Aggiorna display dello status"""
        enabled = self.config["schedule"].get("enabled", True)

        # Aggiorna dashboard status
        if enabled:
            self.status_icon_label.config(text="🟢")
            self.status_text_label.config(
                text="AUTOMAZIONE ATTIVA",
                bootstyle="success"
            )
            self.toggle_button.config(
                text="🔴 Disabilita Automazione",
                bootstyle="danger"
            )
            self.header_status_label.config(text="🟢 ATTIVA")
        else:
            self.status_icon_label.config(text="🔴")
            self.status_text_label.config(
                text="AUTOMAZIONE DISATTIVA",
                bootstyle="danger"
            )
            self.toggle_button.config(
                text="🟢 Abilita Automazione",
                bootstyle="success"
            )
            self.header_status_label.config(text="🔴 DISATTIVA")

        # Aggiorna info text
        self.update_info_display()

        # Aggiorna status bar
        self.status_bar.config(
            text=f"Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}"
        )

    def update_info_display(self):
        """Aggiorna display informazioni configurazione"""
        self.info_text.delete("1.0", END)

        enabled = self.config['schedule'].get('enabled', True)
        status_emoji = "🟢" if enabled else "🔴"
        status_text = "Attiva" if enabled else "Disattiva"

        info = f"""
{status_emoji} STATUS: {status_text}

📅 ORARIO ESECUZIONE
   {self.config['schedule']['execution_time']}

📊 POST PER GIORNO
   {self.config['schedule']['posts_per_day']} post

📰 FONTI RSS CONFIGURATE
   {len(self.config['ai_sources']['rss_feeds'])} feed attivi

🎯 PROSSIMA ESECUZIONE
   Domani alle {self.config['schedule']['execution_time']}

📁 CARTELLA OUTPUT
   generated_posts/YYYY/MM/DD/

💾 FILE CONFIGURAZIONE
   automation_config.json
"""
        self.info_text.insert("1.0", info)
        self.info_text.config(state="disabled")

    def refresh_rss_list(self):
        """Aggiorna lista RSS"""
        self.rss_listbox.delete(0, END)

        for i, rss_url in enumerate(self.config["ai_sources"]["rss_feeds"], 1):
            self.rss_listbox.insert(END, f"{i}. {rss_url}")

    def add_rss_feed(self):
        """Aggiungi feed RSS tramite dialog"""
        from ttkbootstrap.dialogs import Querybox

        new_rss = Querybox.get_string(
            prompt="Inserisci URL del feed RSS:",
            title="Aggiungi RSS",
            parent=self.root
        )

        if new_rss and new_rss.strip():
            new_rss = new_rss.strip()
            if new_rss not in self.config["ai_sources"]["rss_feeds"]:
                self.config["ai_sources"]["rss_feeds"].append(new_rss)
                if self.save_config():
                    self.refresh_rss_list()
                    Messagebox.show_info(
                        "Feed RSS aggiunto con successo!",
                        "Successo",
                        parent=self.root
                    )
                else:
                    self.config["ai_sources"]["rss_feeds"].remove(new_rss)
            else:
                Messagebox.show_warning(
                    "Questo feed RSS è già presente!",
                    "Attenzione",
                    parent=self.root
                )

    def quick_add_rss(self):
        """Aggiungi RSS dall'entry field"""
        new_rss = self.rss_entry.get().strip()

        if new_rss:
            if new_rss not in self.config["ai_sources"]["rss_feeds"]:
                self.config["ai_sources"]["rss_feeds"].append(new_rss)
                if self.save_config():
                    self.refresh_rss_list()
                    self.rss_entry.delete(0, END)
                    Messagebox.show_info(
                        "Feed RSS aggiunto con successo!",
                        "Successo",
                        parent=self.root
                    )
                else:
                    self.config["ai_sources"]["rss_feeds"].remove(new_rss)
            else:
                Messagebox.show_warning(
                    "Questo feed RSS è già presente!",
                    "Attenzione",
                    parent=self.root
                )
        else:
            Messagebox.show_warning(
                "Inserisci un URL valido!",
                "Attenzione",
                parent=self.root
            )

    def remove_rss_feed(self):
        """Rimuovi feed RSS selezionato"""
        selection = self.rss_listbox.curselection()

        if selection:
            index = selection[0]
            rss_url = self.config["ai_sources"]["rss_feeds"][index]

            result = Messagebox.yesno(
                f"Vuoi rimuovere questo feed RSS?\n\n{rss_url}",
                "Conferma",
                parent=self.root
            )

            if result == "Yes":
                self.config["ai_sources"]["rss_feeds"].pop(index)
                if self.save_config():
                    self.refresh_rss_list()
                    Messagebox.show_info(
                        "Feed RSS rimosso con successo!",
                        "Successo",
                        parent=self.root
                    )
        else:
            Messagebox.show_warning(
                "Seleziona un feed RSS da rimuovere!",
                "Attenzione",
                parent=self.root
            )

    def test_rss_feed(self):
        """Test feed RSS selezionato"""
        selection = self.rss_listbox.curselection()

        if selection:
            index = selection[0]
            rss_url = self.config["ai_sources"]["rss_feeds"][index]

            # Test in thread separato
            def test_worker():
                try:
                    import feedparser
                    feed = feedparser.parse(rss_url)

                    if feed.entries:
                        message = f"✅ Feed RSS valido!\n\nTitolo: {feed.feed.get('title', 'N/A')}\nArticoli: {len(feed.entries)}"
                        self.root.after(0, lambda: Messagebox.show_info(message, "Test RSS", parent=self.root))
                    else:
                        self.root.after(0, lambda: Messagebox.show_warning("❌ Feed RSS vuoto o non valido", "Test RSS", parent=self.root))

                except Exception as error:
                    error_msg = str(error)
                    self.root.after(0, lambda: Messagebox.show_error(f"❌ Errore: {error_msg}", "Test RSS", parent=self.root))

            threading.Thread(target=test_worker, daemon=True).start()

        else:
            Messagebox.show_warning(
                "Seleziona un feed RSS da testare!",
                "Attenzione",
                parent=self.root
            )

    def save_configuration(self):
        """Salva configurazione base"""
        try:
            self.config["schedule"]["execution_time"] = self.time_entry.get()
            self.config["schedule"]["posts_per_day"] = int(self.posts_spinbox.get())

            if self.save_config():
                self.update_status()
                Messagebox.show_info(
                    "Configurazione salvata con successo!",
                    "Successo",
                    parent=self.root
                )

        except ValueError:
            Messagebox.show_error(
                "Numero post deve essere un numero valido!",
                "Errore",
                parent=self.root
            )
        except Exception as e:
            Messagebox.show_error(
                f"Errore nel salvataggio:\n{e}",
                "Errore",
                parent=self.root
            )

    def load_config_text(self):
        """Carica configurazione nel text widget"""
        self.config_text.delete("1.0", END)
        config_json = json.dumps(self.config, indent=2, ensure_ascii=False)
        self.config_text.insert("1.0", config_json)

    def save_advanced_config(self):
        """Salva configurazione avanzata dal text widget"""
        try:
            config_text = self.config_text.get("1.0", END)
            new_config = json.loads(config_text)

            # Validazione base
            if "schedule" not in new_config or "ai_sources" not in new_config:
                raise ValueError("Configurazione mancante di sezioni obbligatorie")

            self.config = new_config

            if self.save_config():
                self.update_status()
                self.refresh_rss_list()
                Messagebox.show_info(
                    "Configurazione avanzata salvata!",
                    "Successo",
                    parent=self.root
                )

        except json.JSONDecodeError:
            Messagebox.show_error(
                "Formato JSON non valido!",
                "Errore",
                parent=self.root
            )
        except Exception as e:
            Messagebox.show_error(
                f"Errore nel salvataggio:\n{e}",
                "Errore",
                parent=self.root
            )

    def reset_config(self):
        """Reset configurazione ai valori default"""
        result = Messagebox.yesno(
            "Vuoi ripristinare la configurazione ai valori predefiniti?",
            "Conferma Reset",
            parent=self.root
        )

        if result == "Yes":
            self.config = {
                "schedule": {
                    "execution_time": "08:00",
                    "posts_per_day": 2,
                    "enabled": True
                },
                "ai_sources": {
                    "rss_feeds": [
                        "https://feeds.feedburner.com/oreilly/radar",
                        "https://www.wired.com/feed/tag/ai/latest/rss"
                    ]
                }
            }

            if self.save_config():
                self.time_entry.delete(0, END)
                self.time_entry.insert(0, "08:00")
                self.posts_spinbox.set("2")

                self.load_config_text()
                self.update_status()
                self.refresh_rss_list()
                Messagebox.show_info(
                    "Configurazione ripristinata ai valori predefiniti!",
                    "Successo",
                    parent=self.root
                )

    def run_manual_test(self):
        """Esegue test manuale dell'automazione"""
        result = Messagebox.yesno(
            "Vuoi eseguire un test manuale dell'automazione?\n\n"
            "Questo genererà post reali con le impostazioni attuali.",
            "Test Manuale",
            parent=self.root
        )

        if result == "Yes":
            def test_worker():
                try:
                    self.root.after(0, lambda: self.status_bar.config(text="⏳ Test in esecuzione..."))

                    venv_python = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')

                    if os.path.exists(venv_python):
                        result = subprocess.run(
                            [venv_python, "daily_ai_automation.py"],
                            cwd=os.getcwd(),
                            timeout=300
                        )
                    else:
                        result = subprocess.run(
                            [sys.executable, "daily_ai_automation.py"],
                            cwd=os.getcwd(),
                            timeout=300
                        )

                    if result.returncode == 0:
                        self.root.after(0, lambda: Messagebox.show_info(
                            "✅ Test completato con successo!\n\n"
                            "Controlla la cartella generated_posts per i risultati.",
                            "Test Completato",
                            parent=self.root
                        ))
                    else:
                        self.root.after(0, lambda: Messagebox.show_error(
                            f"❌ Test fallito:\n\n{result.stderr}",
                            "Test Fallito",
                            parent=self.root
                        ))

                except Exception as error:
                    error_msg = str(error)
                    self.root.after(0, lambda: Messagebox.show_error(
                        f"Errore durante il test:\n{error_msg}",
                        "Errore Test",
                        parent=self.root
                    ))

                finally:
                    self.root.after(0, lambda: self.status_bar.config(text="✅ Test completato"))

            threading.Thread(target=test_worker, daemon=True).start()

    def show_latest_log(self):
        """Mostra log più recente"""
        self.notebook.select(3)  # Seleziona tab log
        self.refresh_log()

    def refresh_log(self):
        """Aggiorna contenuto log"""
        self.log_text.delete("1.0", END)

        log_dir = "logs"
        if os.path.exists(log_dir):
            log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]

            if log_files:
                latest_log = max(log_files, key=lambda f: os.path.getmtime(os.path.join(log_dir, f)))
                log_path = os.path.join(log_dir, latest_log)

                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                        self.log_text.insert("1.0", log_content)
                        self.log_text.see(END)

                except Exception as e:
                    self.log_text.insert("1.0", f"Errore lettura log: {e}")
            else:
                self.log_text.insert("1.0", "Nessun file log trovato")
        else:
            self.log_text.insert("1.0", "Cartella logs non trovata")

    def clear_log(self):
        """Pulisce area log"""
        result = Messagebox.yesno(
            "Vuoi pulire la visualizzazione del log?",
            "Conferma",
            parent=self.root
        )

        if result == "Yes":
            self.log_text.delete("1.0", END)
            self.log_text.insert("1.0", "Log pulito - usa 'Aggiorna' per ricaricare")

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
                Messagebox.show_error(
                    f"Impossibile aprire la cartella:\n{e}",
                    "Errore",
                    parent=self.root
                )
        else:
            Messagebox.show_warning(
                "Cartella post non trovata!\n\n"
                "Esegui prima un test per generare dei post.",
                "Attenzione",
                parent=self.root
            )

    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()


# Importa tk per Listbox (ttkbootstrap non ha Listbox)
import tkinter as tk


if __name__ == "__main__":
    app = AIContentControlPanel()
    app.run()
