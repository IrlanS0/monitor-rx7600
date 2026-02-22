import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CHAT_ID_PERSON = os.environ["TELEGRAM_CHAT_ID_FLOW"]  
URL = "https://www.kabum.com.br/produto/463543/placa-de-video-rx-7600-series-graphics-cards-xfx-amd-radeon-8gb-gddr6-rx-76pqickby"
URL_INTEL = "https://www.kabum.com.br/produto/283718/processador-intel-core-i5-12400f-2-5ghz-4-4ghz-max-turbo-cache-18mb-lga-1700-bx8071512400f"
URL_RYZEN = "https://www.kabum.com.br/produto/356695/processador-amd-ryzen-5-5500-3-6ghz-cache-16mb-hexa-core-12-threads-am4-100-100000457box"

PRECO_ALERTA = 1599.99

def enviar_msg(mensagem, chat):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": chat,
        "text": mensagem
    })

def pegar_preco(string, url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    preco_elemento = driver.find_element(By.XPATH, string)
    texto = preco_elemento.text

    driver.quit()

    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
    return valor

XPATH_PRECO = "//div[@id='main-content']//h4[contains(text(),'R$')]"
preco = pegar_preco(XPATH_PRECO, URL)
preco_i5 = pegar_preco(XPATH_PRECO, URL_INTEL)
preco_ryzen = pegar_preco(XPATH_PRECO, URL_RYZEN)


enviar_msg(f"i5 12400F: R$ {preco_i5}", CHAT_ID_PERSON)
enviar_msg(f"Ryzen 5 5500: R$ {preco_ryzen}", CHAT_ID_PERSON)
if preco < PRECO_ALERTA:
    enviar_msg(f"🔥 RX 7600 caiu! Está R$ {preco}", CHAT_ID)
else:
    enviar_msg(f"Preço atual: R$ {preco}", CHAT_ID)
