# control_panel.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import sys
import os
import subprocess
import threading
from datetime import datetime


class AIContentControlPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.config_file = "automation_config.json"
        self.setup_window()
        self.load_config()
        self.setup_ui()
        self.update_status()
        
    def setup_window(self):
        """Configura la finestra principale"""
        self.root.title("AI Content Helper - Pannello di Controllo")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Centra la finestra
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
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
            messagebox.showerror("Errore", f"Impossibile salvare configurazione: {e}")
            return False
    
    def setup_ui(self):
        """Crea l'interfaccia utente"""
        # Notebook per tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab Principale
        self.create_main_tab()
        
        # Tab Fonti RSS
        self.create_rss_tab()
        
        # Tab Configurazione
        self.create_config_tab()
        
        # Tab Log
        self.create_log_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_main_tab(self):
        """Crea tab principale con controlli automazione"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Controllo Automazione")
        
        # Titolo
        title_label = tk.Label(main_frame, text="AI Content Helper", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame status automazione
        status_frame = ttk.LabelFrame(main_frame, text="Status Automazione", padding=15)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Status indicator
        self.status_frame_inner = tk.Frame(status_frame)
        self.status_frame_inner.pack(fill="x")
        
        self.status_label = tk.Label(self.status_frame_inner, text="🔄 Caricamento...", 
                                    font=("Arial", 12))
        self.status_label.pack(side="left")
        
        # Pulsante Enable/Disable
        self.toggle_button = tk.Button(self.status_frame_inner, text="Disabilita", 
                                      command=self.toggle_automation,
                                      bg="red", fg="white", font=("Arial", 10, "bold"))
        self.toggle_button.pack(side="right")
        
        # Informazioni configurazione
        info_frame = ttk.LabelFrame(main_frame, text="Configurazione Attuale", padding=15)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=6, bg="#f0f0f0", font=("Consolas", 10))
        self.info_text.pack(fill="both", expand=True)
        
        # Pulsanti azione
        action_frame = ttk.LabelFrame(main_frame, text="Azioni", padding=15)
        action_frame.pack(fill="x", padx=20, pady=10)
        
        button_frame = tk.Frame(action_frame)
        button_frame.pack(fill="x")
        
        # Pulsante Test
        test_button = tk.Button(button_frame, text="🧪 Test Manuale", 
                               command=self.run_manual_test,
                               bg="blue", fg="white", font=("Arial", 10, "bold"))
        test_button.pack(side="left", padx=5)
        
        # Pulsante Visualizza Log
        log_button = tk.Button(button_frame, text="📋 Visualizza Log", 
                              command=self.show_latest_log,
                              bg="green", fg="white", font=("Arial", 10, "bold"))
        log_button.pack(side="left", padx=5)
        
        # Pulsante Apri Cartella Post
        folder_button = tk.Button(button_frame, text="📁 Apri Cartella Post", 
                                 command=self.open_posts_folder,
                                 bg="orange", fg="white", font=("Arial", 10, "bold"))
        folder_button.pack(side="left", padx=5)
        
        # Pulsante Aggiorna
        refresh_button = tk.Button(button_frame, text="🔄 Aggiorna", 
                                  command=self.update_status,
                                  bg="purple", fg="white", font=("Arial", 10, "bold"))
        refresh_button.pack(side="right", padx=5)
    
    def create_rss_tab(self):
        """Crea tab per gestione fonti RSS"""
        rss_frame = ttk.Frame(self.notebook)
        self.notebook.add(rss_frame, text="Fonti RSS")
        
        # Titolo
        title_label = tk.Label(rss_frame, text="Gestione Fonti RSS", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame lista RSS
        list_frame = ttk.LabelFrame(rss_frame, text="Fonti RSS Attive", padding=15)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lista RSS con scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        self.rss_listbox = tk.Listbox(list_container, font=("Consolas", 9))
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.rss_listbox.yview)
        self.rss_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.rss_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Pulsanti gestione RSS
        rss_button_frame = tk.Frame(list_frame)
        rss_button_frame.pack(fill="x", pady=10)
        
        add_rss_button = tk.Button(rss_button_frame, text="➕ Aggiungi RSS", 
                                  command=self.add_rss_feed,
                                  bg="green", fg="white", font=("Arial", 10, "bold"))
        add_rss_button.pack(side="left", padx=5)
        
        remove_rss_button = tk.Button(rss_button_frame, text="➖ Rimuovi RSS", 
                                     command=self.remove_rss_feed,
                                     bg="red", fg="white", font=("Arial", 10, "bold"))
        remove_rss_button.pack(side="left", padx=5)
        
        test_rss_button = tk.Button(rss_button_frame, text="🧪 Test RSS", 
                                   command=self.test_rss_feed,
                                   bg="blue", fg="white", font=("Arial", 10, "bold"))
        test_rss_button.pack(side="left", padx=5)
        
        # Input per nuovo RSS
        input_frame = ttk.LabelFrame(rss_frame, text="Aggiungi Nuovo Feed RSS", padding=15)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        self.rss_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.rss_entry.pack(fill="x", pady=5)
        
        quick_add_button = tk.Button(input_frame, text="🚀 Aggiungi Veloce", 
                                    command=self.quick_add_rss,
                                    bg="darkgreen", fg="white", font=("Arial", 10, "bold"))
        quick_add_button.pack(pady=5)
        
        # Carica liste RSS
        self.refresh_rss_list()
    
    def create_config_tab(self):
        """Crea tab per configurazione"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configurazione")
        
        # Titolo
        title_label = tk.Label(config_frame, text="Configurazione Sistema", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame orario
        time_frame = ttk.LabelFrame(config_frame, text="Orario Esecuzione", padding=15)
        time_frame.pack(fill="x", padx=20, pady=10)
        
        time_container = tk.Frame(time_frame)
        time_container.pack(fill="x")
        
        tk.Label(time_container, text="Orario giornaliero:", font=("Arial", 10)).pack(side="left")
        self.time_entry = tk.Entry(time_container, font=("Arial", 10), width=10)
        self.time_entry.pack(side="left", padx=10)
        self.time_entry.insert(0, self.config["schedule"]["execution_time"])
        
        # Frame numero post
        posts_frame = ttk.LabelFrame(config_frame, text="Numero Post", padding=15)
        posts_frame.pack(fill="x", padx=20, pady=10)
        
        posts_container = tk.Frame(posts_frame)
        posts_container.pack(fill="x")
        
        tk.Label(posts_container, text="Post per giorno:", font=("Arial", 10)).pack(side="left")
        self.posts_spinbox = tk.Spinbox(posts_container, from_=1, to=5, font=("Arial", 10), width=10)
        self.posts_spinbox.pack(side="left", padx=10)
        self.posts_spinbox.insert(0, str(self.config["schedule"]["posts_per_day"]))
        
        # Pulsante salva configurazione
        save_button = tk.Button(config_frame, text="💾 Salva Configurazione", 
                               command=self.save_configuration,
                               bg="darkblue", fg="white", font=("Arial", 12, "bold"))
        save_button.pack(pady=20)
        
        # Frame configurazione avanzata
        advanced_frame = ttk.LabelFrame(config_frame, text="Configurazione Avanzata", padding=15)
        advanced_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.config_text = scrolledtext.ScrolledText(advanced_frame, font=("Consolas", 9))
        self.config_text.pack(fill="both", expand=True)
        
        # Carica configurazione nel text widget
        self.load_config_text()
        
        # Pulsanti configurazione avanzata
        advanced_buttons = tk.Frame(advanced_frame)
        advanced_buttons.pack(fill="x", pady=5)
        
        save_advanced_button = tk.Button(advanced_buttons, text="💾 Salva Avanzata", 
                                        command=self.save_advanced_config,
                                        bg="darkred", fg="white", font=("Arial", 10, "bold"))
        save_advanced_button.pack(side="left", padx=5)
        
        reset_button = tk.Button(advanced_buttons, text="🔄 Reset Default", 
                                command=self.reset_config,
                                bg="gray", fg="white", font=("Arial", 10, "bold"))
        reset_button.pack(side="left", padx=5)
    
    def create_log_tab(self):
        """Crea tab per visualizzazione log"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Log")
        
        # Titolo
        title_label = tk.Label(log_frame, text="Log Sistema", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Pulsanti log
        log_buttons = tk.Frame(log_frame)
        log_buttons.pack(fill="x", padx=20, pady=5)
        
        refresh_log_button = tk.Button(log_buttons, text="🔄 Aggiorna Log", 
                                      command=self.refresh_log,
                                      bg="blue", fg="white", font=("Arial", 10, "bold"))
        refresh_log_button.pack(side="left", padx=5)
        
        clear_log_button = tk.Button(log_buttons, text="🗑️ Pulisci Log", 
                                    command=self.clear_log,
                                    bg="red", fg="white", font=("Arial", 10, "bold"))
        clear_log_button.pack(side="left", padx=5)
        
        # Area log
        log_container = ttk.LabelFrame(log_frame, text="Log Recenti", padding=15)
        log_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_container, font=("Consolas", 9), 
                                                 bg="black", fg="white")
        self.log_text.pack(fill="both", expand=True)
        
        # Carica log iniziale
        self.refresh_log()
    
    def create_status_bar(self):
        """Crea barra di stato"""
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def toggle_automation(self):
        """Abilita/disabilita automazione"""
        current_status = self.config["schedule"].get("enabled", True)
        new_status = not current_status
        
        self.config["schedule"]["enabled"] = new_status
        
        if self.save_config():
            self.update_status()
            status_msg = "abilitata" if new_status else "disabilitata"
            messagebox.showinfo("Successo", f"Automazione {status_msg} con successo!")
        else:
            # Ripristina stato precedente se salvataggio fallisce
            self.config["schedule"]["enabled"] = current_status
    
    def update_status(self):
        """Aggiorna display dello status"""
        enabled = self.config["schedule"].get("enabled", True)
        
        if enabled:
            self.status_label.config(text="🟢 Automazione ATTIVA", fg="green")
            self.toggle_button.config(text="🔴 Disabilita", bg="red")
        else:
            self.status_label.config(text="🔴 Automazione DISATTIVA", fg="red")
            self.toggle_button.config(text="🟢 Abilita", bg="green")
        
        # Aggiorna info configurazione
        self.update_info_display()
        
        # Aggiorna status bar
        self.status_bar.config(text=f"Aggiornato: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_info_display(self):
        """Aggiorna display informazioni configurazione"""
        self.info_text.delete(1.0, tk.END)
        
        info = f"""📅 Orario Esecuzione: {self.config['schedule']['execution_time']}
📊 Post per Giorno: {self.config['schedule']['posts_per_day']}
📰 Fonti RSS: {len(self.config['ai_sources']['rss_feeds'])}
🔄 Status: {'Attiva' if self.config['schedule'].get('enabled', True) else 'Disattiva'}

🎯 Prossima Esecuzione: Domani alle {self.config['schedule']['execution_time']}
📁 Cartella Post: generated_posts/
"""
        self.info_text.insert(1.0, info)
    
    def refresh_rss_list(self):
        """Aggiorna lista RSS"""
        self.rss_listbox.delete(0, tk.END)
        
        for i, rss_url in enumerate(self.config["ai_sources"]["rss_feeds"], 1):
            self.rss_listbox.insert(tk.END, f"{i}. {rss_url}")
    
    def add_rss_feed(self):
        """Aggiungi feed RSS tramite dialog"""
        from tkinter import simpledialog
        
        new_rss = simpledialog.askstring("Aggiungi RSS", 
                                        "Inserisci URL del feed RSS:")
        
        if new_rss and new_rss.strip():
            new_rss = new_rss.strip()
            if new_rss not in self.config["ai_sources"]["rss_feeds"]:
                self.config["ai_sources"]["rss_feeds"].append(new_rss)
                if self.save_config():
                    self.refresh_rss_list()
                    messagebox.showinfo("Successo", "Feed RSS aggiunto con successo!")
                else:
                    self.config["ai_sources"]["rss_feeds"].remove(new_rss)
            else:
                messagebox.showwarning("Attenzione", "Questo feed RSS è già presente!")
    
    def quick_add_rss(self):
        """Aggiungi RSS dall'entry field"""
        new_rss = self.rss_entry.get().strip()
        
        if new_rss:
            if new_rss not in self.config["ai_sources"]["rss_feeds"]:
                self.config["ai_sources"]["rss_feeds"].append(new_rss)
                if self.save_config():
                    self.refresh_rss_list()
                    self.rss_entry.delete(0, tk.END)
                    messagebox.showinfo("Successo", "Feed RSS aggiunto con successo!")
                else:
                    self.config["ai_sources"]["rss_feeds"].remove(new_rss)
            else:
                messagebox.showwarning("Attenzione", "Questo feed RSS è già presente!")
        else:
            messagebox.showwarning("Attenzione", "Inserisci un URL valido!")
    
    def remove_rss_feed(self):
        """Rimuovi feed RSS selezionato"""
        selection = self.rss_listbox.curselection()
        
        if selection:
            index = selection[0]
            rss_url = self.config["ai_sources"]["rss_feeds"][index]
            
            result = messagebox.askyesno("Conferma", 
                                        f"Vuoi rimuovere questo feed RSS?\n\n{rss_url}")
            
            if result:
                self.config["ai_sources"]["rss_feeds"].pop(index)
                if self.save_config():
                    self.refresh_rss_list()
                    messagebox.showinfo("Successo", "Feed RSS rimosso con successo!")
        else:
            messagebox.showwarning("Attenzione", "Seleziona un feed RSS da rimuovere!")
    
    def test_rss_feed(self):
        """Test feed RSS selezionato"""
        selection = self.rss_listbox.curselection()
        
        if selection:
            index = selection[0]
            rss_url = self.config["ai_sources"]["rss_feeds"][index]
            
            # Test in thread separato per non bloccare GUI
            def test_worker():
                try:
                    import feedparser
                    feed = feedparser.parse(rss_url)
                    
                    if feed.entries:
                        message = f"✅ Feed RSS valido!\n\nTitolo: {feed.feed.get('title', 'N/A')}\nArticoli: {len(feed.entries)}"
                        self.root.after(0, lambda: messagebox.showinfo("Test RSS", message))
                    else:
                        self.root.after(0, lambda: messagebox.showwarning("Test RSS", "❌ Feed RSS vuoto o non valido"))
                        
                except Exception as error:
                    error_msg = str(error)
                    self.root.after(0, lambda: messagebox.showerror("Test RSS", f"❌ Errore: {error_msg}"))
            
            threading.Thread(target=test_worker, daemon=True).start()
            
        else:
            messagebox.showwarning("Attenzione", "Seleziona un feed RSS da testare!")
    
    def save_configuration(self):
        """Salva configurazione base"""
        try:
            # Aggiorna configurazione con valori GUI
            self.config["schedule"]["execution_time"] = self.time_entry.get()
            self.config["schedule"]["posts_per_day"] = int(self.posts_spinbox.get())
            
            if self.save_config():
                self.update_status()
                messagebox.showinfo("Successo", "Configurazione salvata con successo!")
            
        except ValueError:
            messagebox.showerror("Errore", "Numero post deve essere un numero valido!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")
    
    def load_config_text(self):
        """Carica configurazione nel text widget"""
        self.config_text.delete(1.0, tk.END)
        config_json = json.dumps(self.config, indent=2, ensure_ascii=False)
        self.config_text.insert(1.0, config_json)
    
    def save_advanced_config(self):
        """Salva configurazione avanzata dal text widget"""
        try:
            config_text = self.config_text.get(1.0, tk.END)
            new_config = json.loads(config_text)
            
            # Validazione base
            if "schedule" not in new_config or "ai_sources" not in new_config:
                raise ValueError("Configurazione mancante di sezioni obbligatorie")
            
            self.config = new_config
            
            if self.save_config():
                self.update_status()
                self.refresh_rss_list()
                messagebox.showinfo("Successo", "Configurazione avanzata salvata!")
            
        except json.JSONDecodeError:
            messagebox.showerror("Errore", "Formato JSON non valido!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel salvataggio: {e}")
    
    def reset_config(self):
        """Reset configurazione ai valori default"""
        result = messagebox.askyesno("Conferma", 
                                    "Vuoi ripristinare la configurazione ai valori predefiniti?")
        
        if result:
            # Configurazione default
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
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, "08:00")
                self.posts_spinbox.delete(0, tk.END)
                self.posts_spinbox.insert(0, "2")
                
                self.load_config_text()
                self.update_status()
                self.refresh_rss_list()
                messagebox.showinfo("Successo", "Configurazione ripristinata ai valori predefiniti!")
    
    def run_manual_test(self):
        """Esegue test manuale dell'automazione"""
        result = messagebox.askyesno("Test Manuale", 
                                    "Vuoi eseguire un test manuale dell'automazione?\n\n"
                                    "Questo genererà post reali con le impostazioni attuali.")
        
        if result:
            def test_worker():
                try:
                    self.root.after(0, lambda: self.status_bar.config(text="Test in esecuzione..."))
                    
                    venv_python = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')

                    if os.path.exists(venv_python):
                        result = subprocess.run([venv_python, "daily_ai_automation.py"],
                                                cwd=os.getcwd(),
                                                timeout=300)
                    else:
                        result = subprocess.run([sys.executable, "daily_ai_automation.py"],
                                                cwd=os.getcwd(),
                                                timeout=300)

                    if result.returncode == 0:
                        self.root.after(0, lambda: messagebox.showinfo("Test Completato", 
                                                                      "✅ Test completato con successo!\n\n"
                                                                      "Controlla la cartella generated_posts per i risultati."))
                    else:
                        self.root.after(0, lambda: messagebox.showerror("Test Fallito", 
                                                                        f"❌ Test fallito:\n\n{result.stderr}"))
                    
                except Exception as error:
                    error_msg = str(error)
                    self.root.after(0, lambda: messagebox.showerror("Errore Test", f"Errore durante il test: {error_msg}"))

                finally:
                    self.root.after(0, lambda: self.status_bar.config(text="Test completato"))
            
            threading.Thread(target=test_worker, daemon=True).start()
    
    def show_latest_log(self):
        """Mostra log più recente"""
        self.notebook.select(3)  # Seleziona tab log
        self.refresh_log()
    
    def refresh_log(self):
        """Aggiorna contenuto log"""
        self.log_text.delete(1.0, tk.END)
        
        # Cerca file log più recente
        log_dir = "logs"
        if os.path.exists(log_dir):
            log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
            
            if log_files:
                latest_log = max(log_files, key=lambda f: os.path.getmtime(os.path.join(log_dir, f)))
                log_path = os.path.join(log_dir, latest_log)
                
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                        self.log_text.insert(1.0, log_content)
                        self.log_text.see(tk.END)  # Scroll to bottom
                        
                except Exception as e:
                    self.log_text.insert(1.0, f"Errore lettura log: {e}")
            else:
                self.log_text.insert(1.0, "Nessun file log trovato")
        else:
            self.log_text.insert(1.0, "Cartella logs non trovata")
    
    def clear_log(self):
        """Pulisce area log"""
        result = messagebox.askyesno("Conferma", "Vuoi pulire la visualizzazione del log?")
        
        if result:
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(1.0, "Log pulito - usa 'Aggiorna Log' per ricaricare")
    
    def open_posts_folder(self):
        """Apre cartella post generati"""
        posts_dir = "generated_posts"
        
        if os.path.exists(posts_dir):
            if os.name == 'nt':  # Windows
                os.startfile(posts_dir)
            else:  # Linux/Mac
                subprocess.run(["xdg-open", posts_dir])
        else:
            messagebox.showwarning("Attenzione", "Cartella post non trovata!\n\n"
                                  "Esegui prima un test per generare dei post.")
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AIContentControlPanel()
    app.run()