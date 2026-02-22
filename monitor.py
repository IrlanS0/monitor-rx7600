import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
URL = "https://www.kabum.com.br/produto/463543/placa-de-video-rx-7600-series-graphics-cards-xfx-amd-radeon-8gb-gddr6-rx-76pqickby"
PRECO_ALERTA = 1599.99

def enviar_msg(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensagem
    })

def pegar_preco():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(5)

    preco_elemento = driver.find_element(By.XPATH, "//div[@id='main-content']//h4[contains(text(),'R$')]")
    texto = preco_elemento.text

    driver.quit()

    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
    return valor

preco = pegar_preco()

if preco < PRECO_ALERTA:
    enviar_msg(f"🔥 RX 7600 caiu! Está R$ {preco}")
else:
    enviar_msg(f"Preço atual: R$ {preco}")
