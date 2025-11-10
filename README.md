# 🤖 LinkedIn Content Helper

> **Generatore automatico di contenuti LinkedIn basato su AI**
> Estrae notizie da feed RSS su AI/ML e genera post professionali con immagini AI

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 📋 Indice

- [Caratteristiche](#-caratteristiche)
- [Requisiti](#-requisiti)
- [Installazione Rapida](#-installazione-rapida)
- [Configurazione API Keys](#-configurazione-api-keys)
- [Come Usare](#-come-usare)
- [Struttura Progetto](#-struttura-progetto)
- [Automazione Giornaliera](#-automazione-giornaliera)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

---

## ✨ Caratteristiche

### 🎯 Funzionalità Principali

- **Raccolta Automatica**: Estrae articoli da 19+ feed RSS su AI/ML
- **Selezione Intelligente**: Scoring automatico per freshness + relevance
- **Generazione AI**: Post LinkedIn professionali (500-600 parole)
- **Immagini AI**: DALL-E 3 o Google Gemini per copertine
- **Automazione**: Generazione programmata giornaliera
- **GUI Intuitiva**: 3 interfacce grafiche per controllo completo

### 🔧 Componenti

1. **Main Launcher**: Hub centrale per tutte le funzionalità
2. **Control Panel**: Gestione automazione, RSS, configurazione
3. **Manual Mode**: Selezione e generazione manuale singoli post
4. **Automation**: Esecuzione automatica programmabile

### 🎨 AI Integrations

- **Claude AI** (Anthropic): Generazione testo post
- **OpenAI GPT-4**: Fallback generazione testo
- **GPT Image 1**: Generazione immagini (con fallback automatico a DALL-E 3)
- **Google Gemini**: Alternativa immagini

---

## 🔌 Requisiti

### Sistema

- **OS**: Windows 10/11
- **Python**: 3.8 o superiore
- **RAM**: 4GB minimo (8GB consigliato)
- **Spazio**: 500MB per installazione + dipendenze

### API Keys (Obbligatorie)

| Provider | Uso | Costo | Link |
|----------|-----|-------|------|
| **Anthropic Claude** | Generazione testo | ~$0.015 per post | [Ottieni chiave](https://console.anthropic.com/account/keys) |
| **OpenAI** | Generazione immagini | ~$0.04 per immagine | [Ottieni chiave](https://platform.openai.com/api-keys) |
| Google Gemini | Immagini (opzionale) | Variabile | [Ottieni chiave](https://makersuite.google.com/app/apikey) |

**Costo stimato**: ~$0.055 per post completo (testo + immagine)

---

## 🚀 Installazione Rapida

### Metodo 1: Setup Automatico (Consigliato)

```batch
# 1. Scarica e estrai il progetto
# 2. Apri una finestra terminale nella cartella
# 3. Esegui:
setup_windows.bat
```

Lo script installerà automaticamente:
- ✅ Ambiente virtuale Python
- ✅ Tutte le dipendenze
- ✅ Cartelle necessarie
- ✅ Configurazione guidata API keys

### Metodo 2: Installazione Manuale

```batch
# 1. Crea ambiente virtuale
python -m venv venv

# 2. Attiva ambiente
venv\Scripts\activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Configura API keys
copy .env.example .env
notepad .env  # Inserisci le tue chiavi
```

---

## 🔑 Configurazione API Keys

### Opzione A: Configurazione Guidata (GUI)

```batch
python first_run_config.py
```

Interfaccia grafica che:
- ✅ Guida nell'inserimento delle chiavi
- ✅ Testa la connessione in tempo reale
- ✅ Salva automaticamente nel file `.env`

### Opzione B: Manuale

1. Copia `.env.example` in `.env`
2. Apri `.env` con un editor di testo
3. Sostituisci i placeholder:

```env
# Prima (placeholder)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Dopo (chiave reale)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

### Come Ottenere le Chiavi

#### 1️⃣ Anthropic Claude

1. Vai su [console.anthropic.com](https://console.anthropic.com/)
2. Registrati / Accedi
3. Vai su **Account → API Keys**
4. Crea nuova chiave
5. Copia e incolla nel file `.env`

#### 2️⃣ OpenAI

1. Vai su [platform.openai.com](https://platform.openai.com/)
2. Accedi al tuo account
3. Vai su **API Keys**
4. Crea nuova chiave segreta
5. Copia e incolla nel file `.env`

---

## 🎮 Come Usare

### Avvio Rapido

```batch
# Doppio click su:
AVVIA_APP.bat
```

Oppure:

```batch
# Da terminale:
python main_launcher.py
```

### Modalità Disponibili

#### 1. 🎛️ Pannello di Controllo

**Accesso**: Main Launcher → "Pannello di Controllo"

**Funzionalità**:
- ⚙️ Abilita/Disabilita automazione
- 📰 Gestisci feed RSS (aggiungi/rimuovi)
- ⏰ Configura orario e numero post giornalieri
- 📊 Visualizza log e status sistema
- 🧪 Test manuale automazione

#### 2. 📝 Generazione Manuale

**Accesso**: Main Launcher → "App Originale (Manuale)"

**Funzionalità**:
- Vedi lista articoli recenti da tutti i feed
- Seleziona manualmente articolo interessante
- Genera post singolo on-demand
- Personalizza contenuto

#### 3. 🤖 Automazione Giornaliera

**Configurazione**:
1. Apri Control Panel
2. Imposta orario desiderato (es. "08:00")
3. Scegli numero post/giorno (1-5)
4. Abilita automazione

**Esecuzione**:
- Automatica: Task Scheduler Windows (vedi sotto)
- Manuale: `daily_ai_automation.bat`

#### 4. 🧪 Test Sistema

```batch
python automation_test.py
```

Esegue test completo di:
- ✅ Verifica API keys
- ✅ Raccolta articoli RSS
- ✅ Generazione contenuto
- ✅ Generazione immagine

---

## 📁 Struttura Progetto

```
Linkedin_Content_Helper/
│
├── 📄 AVVIA_APP.bat                 # ⭐ Launcher principale
├── 📄 setup_windows.bat             # Installer automatico
│
├── 🐍 main_launcher.py              # Hub GUI principale
├── 🐍 control_panel.py              # Pannello controllo
├── 🐍 new_fetcher.py                # Generazione manuale
├── 🐍 daily_ai_automation.py        # Automazione giornaliera
├── 🐍 automation_test.py            # Test sistema
├── 🐍 first_run_config.py           # Setup API keys (GUI)
├── 🐍 api_key_manager.py            # Gestione API keys
├── 🐍 create_desktop_shortcut.py    # Crea collegamento desktop
│
├── ⚙️ automation_config.json        # Configurazione automazione
├── 📋 feeds.txt                     # Lista feed RSS
├── 📋 requirements.txt              # Dipendenze Python
├── 🔐 .env                          # API keys (DA CREARE)
├── 🔐 .env.example                  # Template API keys
├── 🚫 .gitignore                    # File da ignorare
│
├── 📁 generated_posts/              # Post generati
│   └── YYYY/MM/DD/
│       ├── post_HHMMSS.docx
│       └── post_HHMMSS.png
│
├── 📁 logs/                         # File di log
└── 📁 reports/                      # Report generazione
```

---

## ⏰ Automazione Giornaliera

### Setup Task Scheduler (Windows)

#### Metodo Automatico

1. Apri Control Panel
2. Configura orario e post/giorno
3. Abilita automazione
4. Lo script `automated_ai_content.bat` gestisce tutto

#### Metodo Manuale

1. Apri **Task Scheduler** (Utilità di pianificazione)
2. Crea attività di base:
   - **Nome**: LinkedIn Content Helper
   - **Trigger**: Giornaliero alle 08:00
   - **Azione**: Avvia programma
   - **Programma**: `automated_ai_content.bat`
   - **Inizia in**: Cartella del progetto

### Funzionamento

L'automazione:
1. 📡 Raccoglie articoli da 19+ feed RSS
2. 🎯 Filtra per keyword AI (45+ termini)
3. ⭐ Assegna punteggi (freshness 40% + relevance 60%)
4. 📝 Genera post per i top N articoli
5. 🖼️ Crea immagini con DALL-E 3
6. 💾 Salva in `generated_posts/YYYY/MM/DD/`
7. 📊 Genera log e report

---

## 🐛 Troubleshooting

### Problemi Comuni

#### 1. "Python non trovato"

**Soluzione**:
```batch
# 1. Scarica Python da python.org
# 2. Durante installazione, seleziona "Add Python to PATH"
# 3. Riavvia il terminale
```

#### 2. "Errore importazione moduli"

**Soluzione**:
```batch
# Reinstalla dipendenze
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 3. "API key non valida"

**Soluzione**:
1. Verifica che `.env` esista (non `.env.example`)
2. Controlla che le chiavi non contengano spazi extra
3. Verifica che le chiavi inizino con il prefixo corretto:
   - Anthropic: `sk-ant-`
   - OpenAI: `sk-`
4. Testa le chiavi: `python automation_test.py`

#### 4. "Nessun articolo raccolto"

**Soluzione**:
1. Verifica connessione internet
2. Controlla i feed RSS in `automation_config.json`
3. Alcuni feed potrebbero essere temporaneamente offline
4. Prova a rimuovere/aggiungere feed dal Control Panel

#### 5. "Generazione immagine fallita"

**Soluzione**:
1. Verifica credito API OpenAI
2. L'app userà immagini template come fallback
3. Prova provider alternativo (Google Gemini):
   ```env
   GOOGLE_API_KEY=your_google_key
   ```

### Log e Debug

I log si trovano in `logs/`:
- `linkedin_generator_YYYYMMDD.log` - App manuale
- `enhanced_automation_YYYYMMDD.log` - Automazione
- `automation_test_YYYYMMDD.log` - Test

**Visualizza log**:
- Da Control Panel → Tab "Log"
- Oppure apri manualmente con Notepad

---

## ❓ FAQ

### Generali

**Q: Quanto costa usare l'app?**
A: L'app è gratuita. Paghi solo le API calls:
- ~$0.015 per post (Claude)
- ~$0.04 per immagine (DALL-E 3)
- Totale: ~$0.055 per post completo

**Q: Posso usare solo una delle API (es. solo Claude)?**
A: No, sono necessarie entrambe (Claude per testo + OpenAI per immagini). Google Gemini è opzionale.

**Q: I post vengono pubblicati automaticamente su LinkedIn?**
A: No, l'app genera solo i contenuti. Dovrai copiarli e pubblicarli manualmente.

**Q: Posso personalizzare lo stile dei post?**
A: Sì, modifica i prompt in `daily_ai_automation.py` o `new_fetcher.py`

### Tecnici

**Q: Funziona su Mac/Linux?**
A: Il codice Python è cross-platform, ma gli script `.bat` sono solo Windows. Su Mac/Linux usa direttamente i comandi Python.

**Q: Posso aggiungere nuovi feed RSS?**
A: Sì! Control Panel → Tab "Fonti RSS" → Aggiungi RSS

**Q: Come cambio il numero di post giornalieri?**
A: Control Panel → Tab "Configurazione" → Posts per giorno

**Q: Posso usare un altro modello AI?**
A: Sì, modifica il `model` in `daily_ai_automation.py`:
```python
model="claude-3-opus-20240229"  # Più potente ma costoso
```

**Q: L'app funziona offline?**
A: No, richiede connessione internet per:
- Scaricare articoli RSS
- Chiamare API AI

---

## 📝 Note sulla Privacy

- ✅ Le API keys sono salvate **localmente** in `.env`
- ✅ Il file `.env` è in `.gitignore` (mai committato)
- ✅ Nessun dato è inviato a server terzi (solo API ufficiali)
- ⚠️ **Non condividere mai** il file `.env`

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Sei libero di usarlo, modificarlo e distribuirlo.

---

## 🤝 Supporto

**Problemi?** Apri una issue su GitHub con:
- Descrizione del problema
- Log rilevanti (da `logs/`)
- Sistema operativo e versione Python

---

## 🎯 Prossimi Passi

Dopo l'installazione:

1. ✅ Configura le API keys
2. ✅ Esegui un test: `python automation_test.py`
3. ✅ Genera il primo post manualmente
4. ✅ Configura l'automazione giornaliera
5. ✅ Crea collegamento desktop: `python create_desktop_shortcut.py`

---

**Buona generazione di contenuti! 🚀**
