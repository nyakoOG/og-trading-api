from flask import Flask, request, jsonify
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

app = Flask(__name__)

@app.route('/price', methods=['GET'])
def get_price():
    symbol = request.args.get('symbol', default='BTCUSDT')
    client = Client()
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return jsonify({'price': ticker['price'], 'symbol': ticker['symbol']})
    except BinanceAPIException as e:
        return jsonify({'error': str(e)}), 400

@app.route('/balance', methods=['POST'])
def get_balance():
    data = request.json
    api_key = data.get('api_key')
    api_secret = data.get('api_secret')
    asset = data.get('asset', 'USDT')
    
    client = Client(api_key, api_secret)
    try:
        balance = client.get_asset_balance(asset=asset)
        return jsonify({'asset': asset, 'balance': balance})
    except BinanceAPIException as e:
        return jsonify({'error': str(e)}), 400

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    api_key = data.get('api_key')
    api_secret = data.get('api_secret')
    symbol = data.get('symbol')
    side = data.get('side')  # BUY or SELL
    type_order = data.get('type', 'MARKET')  # Default is MARKET
    quantity = data.get('quantity')

    client = Client(api_key, api_secret)
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=type_order,
            quantity=quantity
        )
        return jsonify(order)
    except BinanceAPIException as e:
        return jsonify({'error': str(e)}), 400

# Esto es CLAVE para que Render detecte el puerto
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

