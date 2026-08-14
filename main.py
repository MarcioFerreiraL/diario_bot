import schedule
import time
import logging
from config import TERMOS_CEPE, TERMOS_AMUPE
from scraper import iniciar_varredura
from telegram_bot import enviar_mensagem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    logging.info("Iniciando rotina de varredura nos Diários Oficiais...")
    resultados = iniciar_varredura(TERMOS_CEPE, TERMOS_AMUPE)
    
    if resultados:
        mensagem = "🚨 *Novidades nos Diários Oficiais!*\n\n"
        for res in resultados:
            mensagem += f"🏛 *Órgão:* {res['origem']}\n"
            mensagem += f"🔎 *Encontrado:* {res['termo']}\n"
            mensagem += f"🔗 [Acessar Busca]({res['link']})\n\n"
        
        enviar_mensagem(mensagem)
        logging.info("Notificações enviadas com sucesso no Telegram.")
    else:
        logging.info("Nenhuma ocorrência encontrada para os termos configurados hoje.")

if __name__ == "__main__":
    logging.info("Container iniciado. Executando primeira checagem...")
    job() 
    
    schedule.every().day.at("07:00").do(job)
    logging.info("Agendamento configurado para as 07:00 diariamente.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)