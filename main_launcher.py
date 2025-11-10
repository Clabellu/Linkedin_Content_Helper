# main_launcher.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class MainLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Configura la finestra principale"""
        self.root.title("AI Content Helper - Launcher")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.minsize(500, 500)
        
        # Centra la finestra
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"600x600+{x}+{y}")
        
        # Sfondo
        self.root.configure(bg="#f0f0f0")
    
    def setup_ui(self):
        """Crea l'interfaccia utente"""
        # Titolo principale
        title_label = tk.Label(self.root, text="🤖 AI Content Helper", 
                              font=("Arial", 20, "bold"), 
                              bg="#f0f0f0", fg="#333")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.root, text="Generatore Automatico Post LinkedIn AI", 
                                 font=("Arial", 12), 
                                 bg="#f0f0f0", fg="#666")
        subtitle_label.pack(pady=5)
        
        # Separatore
        separator = tk.Frame(self.root, height=2, bg="#ddd")
        separator.pack(fill="x", padx=50, pady=20)
        
        # Pulsanti principali
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Pulsante Pannello di Controllo
        control_button = tk.Button(button_frame, 
                                  text="🎛️ Pannello di Controllo",
                                  font=("Arial", 14, "bold"),
                                  bg="#4CAF50", fg="white",
                                  pady=15,
                                  command=self.open_control_panel)
        control_button.pack(fill="x", pady=10)
        
        control_desc = tk.Label(button_frame, 
                               text="Gestisci automazione, fonti RSS, configurazione e log",
                               font=("Arial", 9),
                               bg="#f0f0f0", fg="#666")
        control_desc.pack(pady=5)
        
        # Pulsante App Originale
        original_button = tk.Button(button_frame, 
                                   text="📰 App Originale (Manuale)",
                                   font=("Arial", 14, "bold"),
                                   bg="#2196F3", fg="white",
                                   pady=15,
                                   command=self.open_original_app)
        original_button.pack(fill="x", pady=10)
        
        original_desc = tk.Label(button_frame, 
                                text="Usa l'interfaccia originale per generazione manuale",
                                font=("Arial", 9),
                                bg="#f0f0f0", fg="#666")
        original_desc.pack(pady=5)
        
        # Pulsante Test Automazione
        test_button = tk.Button(button_frame, 
                               text="🧪 Test Automazione",
                               font=("Arial", 14, "bold"),
                               bg="#FF9800", fg="white",
                               pady=15,
                               command=self.run_automation_test)
        test_button.pack(fill="x", pady=10)
        
        test_desc = tk.Label(button_frame, 
                            text="Esegui un test dell'automazione giornaliera",
                            font=("Arial", 9),
                            bg="#f0f0f0", fg="#666")
        test_desc.pack(pady=5)
        
        # Separatore
        separator2 = tk.Frame(self.root, height=1, bg="#ddd")
        separator2.pack(fill="x", padx=50, pady=20)
        
        # Pulsanti secondari
        secondary_frame = tk.Frame(self.root, bg="#f0f0f0")
        secondary_frame.pack(fill="x", padx=50, pady=10)
        
        # Pulsante Apri Cartella
        folder_button = tk.Button(secondary_frame, 
                                 text="📁 Apri Cartella Post",
                                 font=("Arial", 10),
                                 bg="#607D8B", fg="white",
                                 command=self.open_posts_folder)
        folder_button.pack(side="left", padx=5)
        
        # Pulsante Guida
        help_button = tk.Button(secondary_frame, 
                               text="❓ Guida",
                               font=("Arial", 10),
                               bg="#9C27B0", fg="white",
                               command=self.show_help)
        help_button.pack(side="left", padx=5)
        
        # Pulsante Esci
        exit_button = tk.Button(secondary_frame, 
                               text="🚪 Esci",
                               font=("Arial", 10),
                               bg="#f44336", fg="white",
                               command=self.root.quit)
        exit_button.pack(side="right", padx=5)
    
    def open_control_panel(self):
        """Apre il pannello di controllo"""
        try:
            subprocess.Popen([sys.executable, "control_panel.py"])
            self.root.iconify()  # Minimizza il launcher
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il pannello di controllo:\n{e}")
    
    def open_original_app(self):
        """Apre l'app originale"""
        try:
            subprocess.Popen([sys.executable, "new_fetcher.py"])
            self.root.iconify()  # Minimizza il launcher
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire l'app originale:\n{e}")
    
    def run_automation_test(self):
        """Esegue test automazione"""
        result = messagebox.askyesno("Test Automazione", 
                                    "Vuoi eseguire un test dell'automazione?\n\n"
                                    "Questo genererà post reali con le impostazioni attuali.")
        
        if result:
            try:
                # Nascondi finestra durante test
                self.root.withdraw()
                
                venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'Scripts', 'python.exe')
                if os.path.exists(venv_python):
                    result = subprocess.run([venv_python, "automation_test.py"],
                                             capture_output=True, text=True)
                else:
                    result = subprocess.run([sys.executable, "daily_ai_automation.py"],
                                            capture_output=True, text=True)

                # Mostra finestra
                self.root.deiconify()
                
                if result.returncode == 0:
                    messagebox.showinfo("Test Completato", 
                                      "✅ Test automazione completato con successo!\n\n"
                                      "Controlla la cartella generated_posts per i risultati.")
                else:
                    messagebox.showerror("Test Fallito", 
                                        f"❌ Test fallito:\n\n{result.stderr}")
                    
            except Exception as e:
                self.root.deiconify()
                messagebox.showerror("Errore", f"Errore durante il test: {e}")
    
    def open_posts_folder(self):
        """Apre cartella post generati"""
        posts_dir = "generated_posts"
        
        if os.path.exists(posts_dir):
            if os.name == 'nt':  # Windows
                os.startfile(posts_dir)
            else:  # Linux/Mac
                subprocess.run(["xdg-open", posts_dir])
        else:
            messagebox.showwarning("Attenzione", 
                                  "Cartella post non trovata!\n\n"
                                  "Esegui prima un test per generare dei post.")
    
    def show_help(self):
        """Mostra guida rapida"""
        help_text = """🤖 AI Content Helper - Guida Rapida

📋 PANNELLO DI CONTROLLO:
• Gestisci automazione (abilita/disabilita)
• Aggiungi/rimuovi fonti RSS
• Modifica orario e numero post
• Visualizza log e status

📰 APP ORIGINALE:
• Interfaccia manuale classica
• Selezione articoli manuale
• Generazione post singoli

🧪 TEST AUTOMAZIONE:
• Testa il sistema automatico
• Genera post reali di prova
• Verifica funzionamento

⚙️ CONFIGURAZIONE:
• File: automation_config.json
• Orario: modificabile da pannello
• Fonti RSS: gestibili da pannello

🗂️ FILE GENERATI:
• Post: generated_posts/YYYY/MM/DD/
• Log: logs/automation_YYYYMMDD.log
• Report: reports/daily_report_YYYYMMDD.json

❓ SUPPORTO:
• Controlla log per errori
• Verifica API keys nel file .env
• Testa connessione internet"""
        
        messagebox.showinfo("Guida AI Content Helper", help_text)
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainLauncher()
    app.run()