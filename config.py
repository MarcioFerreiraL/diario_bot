import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Monitoramento no Diário Estadual (CEPE)
TERMOS_CEPE = [
    "MARCIO FERREIRA LIMA"
]

# Monitoramento no Diário Municipal (AMUPE)
TERMOS_AMUPE = [
    "MARCIO FERREIRA LIMA",
    "Surubim processo seletivo",
    "Surubim resultado processo seletivo"
]