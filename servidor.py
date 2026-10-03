from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

dados_aquario = {
    "nome": "Meu Aquário",
    "tamanho": "60 litros",
    "tipo": "Água Doce",
    "ph": 6.8,
    "kh": 6,
    "gh": 8,
    "temperatura": 26,
    "amonia": "0",
    "nitrito": "0",
    "nitrato": "15",
    "habitantes": [
        {"id": 1, "nome": "Coridora", "quantidade": 6, "tipo": "Peixe"}
    ],
    "agenda": []
}

@app.route("/")
def inicio():
    return jsonify({"mensagem": "🐠 App Aquarismo Online!"})

@app.route("/aquario", methods=["GET"])
def ver_aquario():
    return jsonify(dados_aquario)

@app.route("/atualizar", methods=["POST"])
def atualizar():
    info = request.json
    dados_aquario.update(info)
    return jsonify({"status": "✅ Salvo!", "dados": dados_aquario})

@app.route("/adicionar-peixe", methods=["POST"])
def add_peixe():
    peixe = request.json
    peixe["id"] = len(dados_aquario["habitantes"]) + 1
    dados_aquario["habitantes"].append(peixe)
    return jsonify({"status": "✅ Adicionado!", "lista": dados_aquario["habitantes"]})

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)