# automation_test.py
"""
Script di test per l'automazione LinkedIn Content Helper
Esegue un test completo del sistema senza pubblicare nulla.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Importa le funzioni dal sistema principale
from daily_ai_automation import (
    EnhancedArticleCollector,
    generate_post_with_ai,
    create_post_image
)

# Carica variabili d'ambiente
load_dotenv()

def setup_test_logging():
    """Setup del sistema di logging per test"""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/automation_test_{date_str}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return log_file

def check_api_keys():
    """Verifica che le API keys siano configurate"""
    issues = []

    anthropic_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')

    if not anthropic_key:
        issues.append("❌ ANTHROPIC_API_KEY non configurata")
    else:
        logging.info("✅ ANTHROPIC_API_KEY trovata")

    if not openai_key:
        issues.append("❌ OPENAI_API_KEY non configurata")
    else:
        logging.info("✅ OPENAI_API_KEY trovata")

    if not google_key:
        logging.warning("⚠️ GOOGLE_API_KEY non configurata (opzionale)")
    else:
        logging.info("✅ GOOGLE_API_KEY trovata")

    return issues

def test_rss_collection():
    """Testa la raccolta articoli da RSS"""
    try:
        logging.info("\n" + "="*60)
        logging.info("TEST 1: Raccolta Articoli da RSS")
        logging.info("="*60)

        collector = EnhancedArticleCollector()
        articles = collector.collect_all_articles()

        if not articles:
            logging.error("❌ Nessun articolo raccolto dai feed RSS")
            return False, None

        logging.info(f"✅ Raccolti {len(articles)} articoli dai feed RSS")

        # Seleziona i migliori articoli
        selected = collector.select_top_articles(articles)

        if not selected:
            logging.error("❌ Nessun articolo selezionato dopo scoring")
            return False, None

        logging.info(f"✅ Selezionati {len(selected)} articoli migliori")

        # Mostra i primi 3
        for i, article in enumerate(selected[:3], 1):
            logging.info(f"\n  {i}. {article.get('title', 'N/A')}")
            logging.info(f"     Source: {article.get('source', 'N/A')}")
            logging.info(f"     Score: {article.get('score', 0):.3f}")
            logging.info(f"     Link: {article.get('link', 'N/A')}")

        return True, selected[0] if selected else None

    except Exception as e:
        logging.error(f"❌ Errore durante test raccolta RSS: {e}")
        return False, None

def test_content_generation(test_article):
    """Testa la generazione contenuto con AI"""
    try:
        logging.info("\n" + "="*60)
        logging.info("TEST 2: Generazione Contenuto AI")
        logging.info("="*60)

        if not test_article:
            logging.error("❌ Nessun articolo disponibile per test")
            return False, None

        logging.info(f"Generazione post per: {test_article.get('title', 'N/A')}")

        # Genera post
        post_content = generate_post_with_ai(test_article)

        if not post_content:
            logging.error("❌ Generazione post fallita")
            return False, None

        logging.info("✅ Post generato con successo")
        logging.info(f"\nAnteprima post ({len(post_content)} caratteri):")
        logging.info("-" * 60)
        preview = post_content[:300] + "..." if len(post_content) > 300 else post_content
        logging.info(preview)
        logging.info("-" * 60)

        return True, post_content

    except Exception as e:
        logging.error(f"❌ Errore durante test generazione contenuto: {e}")
        return False, None

def test_image_generation(test_article, post_content):
    """Testa la generazione immagine con AI"""
    try:
        logging.info("\n" + "="*60)
        logging.info("TEST 3: Generazione Immagine AI")
        logging.info("="*60)

        if not test_article or not post_content:
            logging.error("❌ Dati mancanti per test immagine")
            return False

        # Genera immagine temporanea
        test_image_path = f"test_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        logging.info("Generazione immagine in corso...")
        image_path = create_post_image(test_article, post_content, provider="openai")

        if image_path and os.path.exists(image_path):
            # Rinomina per riconoscerla come file di test
            if os.path.exists(test_image_path):
                os.remove(test_image_path)
            os.rename(image_path, test_image_path)

            file_size = os.path.getsize(test_image_path)
            logging.info(f"✅ Immagine generata con successo: {test_image_path}")
            logging.info(f"   Dimensione: {file_size / 1024:.2f} KB")

            # Pulisci file di test
            try:
                os.remove(test_image_path)
                logging.info("   File di test rimosso")
            except:
                pass

            return True
        else:
            logging.error("❌ Generazione immagine fallita")
            return False

    except Exception as e:
        logging.error(f"❌ Errore durante test generazione immagine: {e}")
        return False

def main():
    """Funzione principale del test"""
    print("\n" + "="*70)
    print("    LINKEDIN CONTENT HELPER - TEST AUTOMAZIONE")
    print("="*70 + "\n")

    # Setup logging
    log_file = setup_test_logging()
    logging.info("Test avviato")
    logging.info(f"Log file: {log_file}")

    # Risultati test
    test_results = {
        'api_keys': False,
        'rss_collection': False,
        'content_generation': False,
        'image_generation': False
    }

    # 1. Verifica API Keys
    logging.info("\n" + "="*60)
    logging.info("VERIFICA API KEYS")
    logging.info("="*60)

    api_issues = check_api_keys()
    if api_issues:
        logging.error("\nProblemi con le API keys:")
        for issue in api_issues:
            logging.error(f"  {issue}")
        logging.error("\nConfigura le API keys nel file .env prima di continuare")
        logging.error("Vedi .env.example per un template")
        return False
    else:
        logging.info("✅ Tutte le API keys obbligatorie sono configurate")
        test_results['api_keys'] = True

    # 2. Test Raccolta RSS
    success, test_article = test_rss_collection()
    test_results['rss_collection'] = success

    if not success:
        logging.error("\n❌ Test raccolta RSS fallito. Interruzione test.")
        print_summary(test_results)
        return False

    # 3. Test Generazione Contenuto
    success, post_content = test_content_generation(test_article)
    test_results['content_generation'] = success

    if not success:
        logging.warning("\n⚠️ Test generazione contenuto fallito. Continuo con test immagine...")

    # 4. Test Generazione Immagine
    if test_article and post_content:
        success = test_image_generation(test_article, post_content)
        test_results['image_generation'] = success
    else:
        logging.warning("⚠️ Skip test immagine - dati mancanti")

    # Riepilogo finale
    print_summary(test_results)

    # Return code
    all_passed = all(test_results.values())
    return 0 if all_passed else 1

def print_summary(results):
    """Stampa riepilogo risultati test"""
    logging.info("\n" + "="*70)
    logging.info("RIEPILOGO TEST")
    logging.info("="*70)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        test_label = test_name.replace('_', ' ').title()
        logging.info(f"{status}  {test_label}")

    logging.info("="*70)

    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    if passed_count == total_count:
        logging.info(f"\n🎉 TUTTI I TEST SUPERATI ({passed_count}/{total_count})")
        logging.info("Il sistema è pronto per l'uso!")
    else:
        logging.warning(f"\n⚠️ ALCUNI TEST FALLITI ({passed_count}/{total_count} superati)")
        logging.warning("Controlla i log sopra per dettagli")

    logging.info("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logging.info("\n\nTest interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        logging.error(f"\n\nErrore fatale durante il test: {e}", exc_info=True)
        sys.exit(1)
