import requests
from bs4 import BeautifulSoup

# URL da página de decks (tente a URL principal sem parâmetros se a URL atual não funcionar)
url_decks = 'https://www.ligamagic.com.br/?view=dks/decks&filtro_formato=9'

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url_decks, headers=headers)
    response.raise_for_status()  # Verifica se houve algum erro na requisição

    # Verificar e descompactar o conteúdo se necessário
    if response.headers.get('Content-Encoding') == 'gzip':
        import gzip
        from io import BytesIO
        buf = BytesIO(response.content)
        f = gzip.GzipFile(fileobj=buf)
        html_content = f.read().decode('utf-8')
    else:
        html_content = response.text  # Use text em vez de content para resposta não compactada

    # Analisar o conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Debug: Imprimir o início do conteúdo HTML para verificar a estrutura
    print(soup.prettify()[:2000])  # Imprime os primeiros 2000 caracteres do HTML

    # Encontrar todas as divs com a classe 'dks-search' (ajustar se necessário)
    divs_deck = soup.find_all('div', class_='dks-search')
    print(f'divs de busca: {len(divs_deck)}')  # Verifica quantas divs foram encontradas

    # Encontrar todas as divs com a classe 'deckhome' (ajustar se necessário)
    divs_deckhome = soup.find_all('div', class_='deckhome')
    print(f'divs de deckhome: {len(divs_deckhome)}')  # Verifica quantas divs foram encontradas


    # Extrair URLs dos decks
    deck_urls = []
    for div in divs_deckhome:
        a_tag = div.find('a', href=True)  # Encontrar o link dentro da div
        print(f'tag: {a_tag}')
        if a_tag:
            deck_urls.append(a_tag['href'])

    # Converter URLs relativas em absolutas
    #deck_urls = [f'https://www.ligamagic.com.br{url}' for url in deck_urls]

    print(f'URLs dos decks encontrados: {deck_urls}')

except requests.exceptions.HTTPError as err:
    print(f'Erro HTTP: {err}')
except Exception as e:
    print(f'Ocorreu um erro: {e}')

def extrair_cartas_do_deck(deck_url):
    # Fazer a requisição HTTP para o deck específico
    response = requests.get(deck_url)
    response.raise_for_status()
    
    # Analisar o conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Dicionário para armazenar as cartas
    cartas = {'Criaturas': [], 'Mágicas': [], 'Terrenos': []}

    # Função auxiliar para extrair cartas de uma seção específica
    def extrair_cartas_por_titulo(titulo):
        cartas_secao = []
        secao_div = soup.find('div', class_='pdeck-block')
        if secao_div:
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

    # Extraindo cartas de cada seção
    cartas['Criaturas'] = extrair_cartas_por_titulo('Criaturas')
    cartas['Mágicas'] = extrair_cartas_por_titulo('Mágicas')
    cartas['Terrenos'] = extrair_cartas_por_titulo('Terrenos')
    
    return cartas

# Scraping dos detalhes de cada deck
#for url in deck_urls:
    #print(f'\nDetalhes do deck: {url}')
    #cartas_do_deck = extrair_cartas_do_deck(url)
    #print('Criaturas:', cartas_do_deck['Criaturas'])
    #print('Mágicas:', cartas_do_deck['Mágicas'])
    #print('Terrenos:', cartas_do_deck['Terrenos'])
