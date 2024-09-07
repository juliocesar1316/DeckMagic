from scraping_decks_v2 import CaptureUrlDeck
from flask import Flask, jsonify

app = Flask(__name__)

# Rota que executa a função de carregar decks
@app.route('/decks', methods=['GET'])
def get_decks():
    try:
        deck_urls = CaptureUrlDeck()  # Chama a função de scraping
        return jsonify({'status': 'success', 'decks': deck_urls})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/')
def home():
    return "Hello, World!"

# Função principal
if __name__ == '__main__':
    app.run(debug=True)