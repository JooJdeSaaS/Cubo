from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Necessário para o site conseguir ler os dados

# Dicionário global para armazenar a última leitura
air_data = {
    "temp": 0, "hum": 0, "mq135": 0,
    "co": 0, "nh3": 0, "no2": 0, "pm25": 0
}


@app.route('/update', methods=['POST'])
def update():
    global air_data
    data = request.json

    # Validação simples para evitar erros no site caso o ESP32 envie lixo
    if data:
        air_data.update(data)
        print(f"Dados Recebidos: {air_data}")  # Útil para debug no Ubuntu
        return {"status": "recebido"}, 200
    return {"status": "erro", "message": "JSON vazio"}, 400

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(air_data)  # Envia os dados para o Site

if __name__ == '__main__':
    # Rode no IP 0.0.0.0 para ser visível na sua rede local
    app.run(host='0.0.0.0', port=5000, debug=True)