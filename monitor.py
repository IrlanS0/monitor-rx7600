import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"
URL = "LINK_DO_SITE"
PRECO_ALERTA = 1600


def enviar_msg(mensagem):
    url = f"https//api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensagem
    })

def pegar_preco():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver
    driver.get(URL)
    time.sleep(5)

    preco_elemento = driver.find_element(By.TAG_NAME, "h4")
    texto = preco_elemento.text

    driver.quit()

    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))
    return valor

preco = pegar_preco()

if preco <= PRECO_ALERTA:
    enviar_msg(f"🔥 RX 7600 caiu! Está R$ {preco}")
else:
    enviar_msg(f"Preço atual: R$ {preco}")