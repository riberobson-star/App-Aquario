from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='.')
CORS(app)

dados = {
    "nome": "Meu Aquário",
    "volume": 0,
    "tipo_agua": "doce",
    "meus_peixes": [],
    "desejos": [],
    "plantas": [],
    "historico": [],
    "tarefas": [],
    "gastos": [],
    "config": {"modo_escuro": False, "horas_luz": 8}
}

banco_peixes = [
    {"id":1,"nome":"Tetra Neon","cientifico":"Paracheirodon innesi","tamanho":4,"vida":5,"origem":"América do Sul","alimentacao":"Onívoro","temp":[22,28],"ph":[5.0,7.5],"gh":[1,15],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"meio","tipo":"pequeno","compativel":["todos"]},
    {"id":2,"nome":"Guppy","cientifico":"Poecilia reticulata","tamanho":5,"vida":3,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[6.8,8.5],"gh":[8,30],"litros_min":30,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"superior","tipo":"pequeno","compativel":["todos"]},
    {"id":3,"nome":"Betta Macho","cientifico":"Betta splendens","tamanho":6,"vida":3,"origem":"Tailândia","alimentacao":"Carnívoro","temp":[24,30],"ph":[6.0,8.0],"gh":[5,20],"litros_min":20,"qtd_min":1,"comportamento":"territorial","nivel":"superior","tipo":"medio","compativel":["nao_betta"]},
    {"id":4,"nome":"Coridora Panda","cientifico":"Corydoras panda","tamanho":5,"vida":10,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":60,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno","compativel":["todos"]},
    {"id":5,"nome":"Coridora Anã","cientifico":"Corydoras pygmaeus","tamanho":3.5,"vida":8,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno","compativel":["todos"]},
    {"id":6,"nome":"Platy","cientifico":"Xiphophorus maculatus","tamanho":6,"vida":4,"origem":"América Central","alimentacao":"Onívoro","temp":[18,28],"ph":[6.8,8.0],"gh":[10,25],"litros_min":40,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"meio","tipo":"pequeno","compativel":["todos"]},
    {"id":7,"nome":"Espada","cientifico":"Xiphophorus hellerii","tamanho":10,"vida":5,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[7.0,8.5],"gh":[10,30],"litros_min":60,"qtd_min":"1M+2F","comportamento":"ativo","nivel":"meio","tipo":"medio","compativel":["todos"]},
    {"id":8,"nome":"Ancistrus (Bristlenose)","cientifico":"Ancistrus sp.","tamanho":12,"vida":12,"origem":"América do Sul","alimentacao":"Herbívoro","temp":[20,28],"ph":[6.0,7.5],"gh":[5,20],"litros_min":80,"qtd_min":1,"comportamento":"pacifico","nivel":"fundo-vidro","tipo":"medio","compativel":["todos"]},
    {"id":9,"nome":"Ramirezi","cientifico":"Mikrogeophagus ramirezi","tamanho":5,"vida":3,"origem":"Colômbia/Venezuela","alimentacao":"Onívoro","temp":[26,30],"ph":[5.0,7.0],"gh":[2,10],"litros_min":40,"qtd_min":"casal","comportamento":"calmo","nivel":"meio","tipo":"pequeno","compativel":["pequeno"]},
    {"id":10,"nome":"Discus","cientifico":"Symphysodon spp.","tamanho":20,"vida":10,"origem":"Amazônia","alimentacao":"Carnívoro","temp":[28,32],"ph":[5.0,6.5],"gh":[1,8],"litros_min":250,"qtd_min":4,"comportamento":"calmo","nivel":"meio-superior","tipo":"grande","compativel":["calmo"]}
]

banco_plantas = [
    {"id":1,"nome":"Anubias Nana","luz":"Baixa","co2":"Não","substrato":"Não — raiz/pedra","crescimento":"Lento"},
    {"id":2,"nome":"Java Fern","luz":"Baixa/Média","co2":"Não","substrato":"Não — raiz/pedra","crescimento":"Médio"},
    {"id":3,"nome":"Vallisnéria","luz":"Média","co2":"Recomendado","substrato":"Sim","crescimento":"Rápido"},
    {"id":4,"nome":"Amazonica","luz":"Baixa/Média","co2":"Não","substrato":"Sim","crescimento":"Médio"},
    {"id":5,"nome":"Eléocharis (Grama)","luz":"Média/Alta","co2":"Recomendado","substrato":"Sim","crescimento":"Médio/Rápido"}
]

doencas = [
    {"sintoma":"manchas brancas","nome":"Íctio","causa":"protozoário","tratamento":"Elevar temp para 30°C + medicamento específico + sal grosso","prevencao":"Quarentena peixes novos, evitar estresse"},
    {"sintoma":"barbatanas desfiadas","nome":"Podridão de barbatana","causa":"bactéria / maus tratos","tratamento":"Troca de água + condicionador + medicamento se piorar","prevencao":"Não superlotar, manter qualidade da água"},
    {"sintoma":"peixe na superficie","nome":"Falta de oxigênio","causa":"calor, excesso de matéria orgânica","tratamento":"Aumentar circulação/arejamento, troca de água","prevencao":"Manter filtro limpo, não superalimentar"},
    {"sintoma":"agua turva branca","nome":"Ciclo bacteriano","causa":"bactérias em fase de crescimento","tratamento":"Paciência! Melhorar circulação, não mexer muito","prevencao":"Ciclar o aquário antes dos peixes"}
]

@app.route("/")
def inicio(): return send_from_directory('.', 'index.html')
@app.route("/banco-peixes")
def bp(): return jsonify(banco_peixes)
@app.route("/banco-plantas")
def bpl(): return jsonify(banco_plantas)
@app.route("/doencas")
def d(): return jsonify(doencas)
@app.route("/dados")
def get_dados(): return jsonify(dados)

@app.route("/salvar-volume", methods=["POST"])
def sv():
    dados["volume"] = request.json["volume"]
    return jsonify({"ok":True})

@app.route("/adicionar-peixe", methods=["POST"])
def ap():
    p = request.json
    p["id"] = len(dados["meus_peixes"])+1
    p["data"] = datetime.now().strftime("%d/%m/%Y")
    dados["meus_peixes"].append(p)
    return jsonify({"ok":True,"lista":dados["meus_peixes"]})

@app.route("/apagar-peixe/<int:i>", methods=["DELETE"])
def dp(i):
    if 0<=i<len(dados["meus_peixes"]): dados["meus_peixes"].pop(i)
    return jsonify({"ok":True})

@app.route("/adicionar-medicao", methods=["POST"])
def am():
    m = request.json
    m["data"] = datetime.now().strftime("%d/%m %H:%M")
    dados["historico"].append(m)
    return jsonify({"ok":True,"lista":dados["historico"]})

@app.route("/adicionar-tarefa", methods=["POST"])
def at():
    t = request.json
    t["id"] = len(dados["tarefas"])+1
    t["concluida"] = False
    dados["tarefas"].append(t)
    return jsonify({"ok":True,"lista":dados["tarefas"]})

@app.route("/concluir-tarefa/<int:i>", methods=["PUT"])
def ct(i):
    if 0<=i<len(dados["tarefas"]):
        dados["tarefas"][i]["concluida"] = not dados["tarefas"][i]["concluida"]
    return jsonify({"ok":True})

@app.route("/adicionar-gasto", methods=["POST"])
def ag():
    g = request.json
    g["id"] = len(dados["gastos"])+1
    g["data"] = datetime.now().strftime("%d/%m/%Y")
    dados["gastos"].append(g)
    return jsonify({"ok":True,"lista":dados["gastos"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
