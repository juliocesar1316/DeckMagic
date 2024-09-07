from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.headless = True  # Executa o Chrome em modo headless (sem interface gráfica)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.ligamagic.com.br/?view=dks/decks&filtro_formato=9')

time.sleep(5)  # Aguarda o carregamento completo da página

html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')

# Continuar com a extração dos dados
divs_deckhome = soup.find_all('div', class_='deckhome')
print(f'divs de deckhome: {len(divs_deckhome)}')

deck_urls = [div.find('a', href=True)['href'] for div in divs_deckhome if div.find('a', href=True)]
deck_urls = [f'https://www.ligamagic.com.br{url}' for url in deck_urls]
print(f'URLs dos decks encontrados: {deck_urls}')

def extrair_cartas_do_deck(deck_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(deck_urls)

    time.sleep(5)  # Aguarda o carregamento completo da página

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Dicionário para armazenar as cartas
    cartas = {
        'Comandante': [], 'Criaturas': [], 'Planeswalkers': [],
        'Mágicas': [], 'Artefatos': [], 'Encantamentos': [], 'Terrenos': []
    }
    
# Função auxiliar para extrair cartas de uma seção específica
def extrair_cartas(secao_div):
    cartas_secao = []
    table = secao_div.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows:
                card_name_td = row.find('td', class_='deck-card')
                quantity_td = row.find('td', class_='deck-qty')
                if card_name_td and quantity_td:
                    card_name = card_name_td.text.strip()
                    quantity = quantity_td.text.strip()
                    cartas_secao.append(f'{card_name} ({quantity})')
        return cartas_secao
    
    # Identificar os títulos das seções
    titulos = ['Comandante', 'Criaturas', 'Planeswalkers', 'Mágicas', 'Artefatos', 'Encantamentos', 'Terrenos']
    
    # Encontrar todos os títulos e suas respectivas seções
    secao_atual = None
    for tr in soup.find_all('tr', class_='deck-type'):
        titulo = tr.get_text(strip=True)
        if titulo in titulos:
            # Captura a seção anterior antes de mudar para a nova seção
            if secao_atual:
                secao_div = tr.find_next_sibling('div', class_='pdeck-block')
                if secao_div:
                    cartas[secao_atual] = extrair_cartas(secao_div)
            secao_atual = titulo
    
    # Captura a última seção após o último título encontrado
    if secao_atual:
        secao_div = tr.find_next_sibling('div', class_='pdeck-block')
        if secao_div:
            cartas[secao_atual] = extrair_cartas(secao_div)
    
    return cartas
