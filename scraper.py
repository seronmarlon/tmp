import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

TOKEN = '6398074781:AAG3_kAjaUtHl13ZVlQo-IVFA6zPN4gc26Y'
CHAT_ID = "-1002130780564"
URL = "https://service.berlin.de/terminvereinbarung/termin/day/"
INTERVALO_MINUTOS = 1

bot = Bot(token=TOKEN)

async def fetch_details():
    try:
        session = requests.Session()
        response = session.get('https://service.berlin.de/terminvereinbarung/termin/all/120686/')
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.find_all('td', class_='buchbar')
        if not tds:
            logger.info("Nenhum dia disponível para agendamento.")
            return []

        messages = []
        for td in tds:
            day = td.text.strip()
            link_tag = td.find('a')
            if link_tag:
                link = link_tag['href']
                message = f"Dia disponível para agendar: {day}\nLink para agendar: https://service.berlin.de{link}"
                messages.append(message)
            else:
                logger.warning("Link não encontrado para um dos dias disponíveis.")
        return messages

    except RequestException as e:
        logger.error(f"Erro ao acessar {URL}: {e}")
        return []

async def send_messages(messages):
    for message in messages:
        await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        logger.info("Iniciando a busca por novos agendamentos disponíveis.")
        messages = loop.run_until_complete(fetch_details())
        if messages:
            logger.info(f"{len(messages)} novos agendamentos encontrados. Enviando mensagens.")
            loop.run_until_complete(send_messages(messages))
        logger.info("Aguardando para a próxima verificação.")
        loop.run_until_complete(asyncio.sleep(INTERVALO_MINUTOS * 60))
