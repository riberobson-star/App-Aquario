from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__, static_folder='.')
CORS(app)

ARQUIVO_DADOS = "dados_salvos.json"

# Carregar dados salvos em arquivo
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "nome": "Meu Aquário",
        "volume": 0,
        "meus_peixes": [],
        "desejos": [],
        "plantas": [],
        "historico": [],
        "tarefas": [],
        "gastos": [],
        "fotos": [],
        "config": {"modo_escuro": False, "horas_luz": 8, "temperatura_ideal": [24, 28], "ph_ideal": [6.0, 7.5]}
    }

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

dados = carregar_dados()

banco_peixes = [
    {"id":1,"nome":"Tetra Neon","cientifico":"Paracheirodon innesi","tamanho":4,"vida":5,"origem":"América do Sul","alimentacao":"Onívoro","temp":[22,28],"ph":[5.0,7.5],"gh":[1,15],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"meio","tipo":"pequeno","compat_exclui":["Betta"]},
    {"id":2,"nome":"Tetra Cardeal","cientifico":"Paracheirodon axelrodi","tamanho":5,"vida":6,"origem":"Brasil","alimentacao":"Onívoro","temp":[23,29],"ph":[4.0,7.0],"gh":[1,8],"litros_min":50,"qtd_min":6,"comportamento":"pacifico","nivel":"meio","tipo":"pequeno","compat_exclui":["peixes grandes"]},
    {"id":3,"nome":"Guppy","cientifico":"Poecilia reticulata","tamanho":5,"vida":3,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[6.8,8.5],"gh":[8,30],"litros_min":30,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"superior","tipo":"pequeno","compat_exclui":[]},
    {"id":4,"nome":"Betta Macho","cientifico":"Betta splendens","tamanho":6,"vida":3,"origem":"Tailândia","alimentacao":"Carnívoro","temp":[24,30],"ph":[6.0,8.0],"gh":[5,20],"litros_min":20,"qtd_min":1,"comportamento":"territorial","nivel":"superior","tipo":"medio","compat_exclui":["Betta","peixes de nadar rápido"]},
    {"id":5,"nome":"Coridora Panda","cientifico":"Corydoras panda","tamanho":5,"vida":10,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":60,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno","compat_exclui":[]},
    {"id":6,"nome":"Coridora Anã","cientifico":"Corydoras pygmaeus","tamanho":3.5,"vida":8,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno","compat_exclui":[]},
    {"id":7,"nome":"Coridora Bronze","cientifico":"Corydoras aeneus","tamanho":7,"vida":10,"origem":"América do Sul","alimentacao":"Onívoro","temp":[20,28],"ph":[5.5,7.5],"gh":[2,15],"litros_min":80,"qtd_min":4,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno","compat_exclui":[]},
    {"id":8,"nome":"Platy","cientifico":"Xiphophorus maculatus","tamanho":6,"vida":4,"origem":"América Central","alimentacao":"Onívoro","temp":[18,28],"ph":[6.8,8.0],"gh":[10,25],"litros_min":40,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"meio","tipo":"pequeno","compat_exclui":[]},
    {"id":9,"nome":"Espada","cientifico":"Xiphophorus hellerii","tamanho":10,"vida":5,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[7.0,8.5],"gh":[10,30],"litros_min":60,"qtd_min":"1M+2F","comportamento":"ativo","nivel":"meio","tipo":"medio","compat_exclui":[]},
    {"id":10,"nome":"Ancistrus (Limpeza)","cientifico":"Ancistrus sp.","tamanho":12,"vida":12,"origem":"América do Sul","alimentacao":"Herbívoro","temp":[20,28],"ph":[6.0,7.5],"gh":[5,20],"litros_min":80,"qtd_min":1,"comportamento":"pacifico","nivel":"fundo-vidro","tipo":"medio","compat_exclui":[]},
    {"id":11,"nome":"Ramirezi","cientifico":"Mikrogeophagus ramirezi","tamanho":5,"vida":3,"origem":"Colômbia/Venezuela","alimentacao":"Onívoro","temp":[26,30],"ph":[5.0,7.0],"gh":[2,10],"litros_min":40,"qtd_min":"casal","comportamento":"calmo","nivel":"meio","tipo":"pequeno","compat_exclui":["peixes muito ativos"]},
    {"id":12,"nome":"Discus","cientifico":"Symphysodon spp.","tamanho":20,"vida":10,"origem":"Amazônia","alimentacao":"Carnívoro","temp":[28,32],"ph":[5.0,6.5],"gh":[1,8],"litros_min":250,"qtd_min":4,"comportamento":"calmo","nivel":"meio-superior","tipo":"grande","compat_exclui":["peixes ativos","peixes grandes"]},
    {"id":13,"nome":"Danio Zebra","cientifico":"Danio rerio","tamanho":5,"vida":5,"origem":"Ásia","alimentacao":"Onívoro","temp":[18,28],"ph":[6.0,8.0],"gh":[5,20],"litros_min":40,"qtd_min":6,"comportamento":"muito_ativo","nivel":"meio-superior","tipo":"pequeno","compat_exclui":["peixes calmos"]},
    {"id":14,"nome":"Molinésia","cientifico":"Poecilia sphenops","tamanho":10,"vida":4,"origem":"América Central","alimentacao":"Onívoro","temp":[22,28],"ph":[7.0,8.5],"gh":[10,30],"litros_min":80,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"meio-superior","tipo":"medio","compat_exclui":[]},
    {"id":15,"nome":"Acará Bandeira","cientifico":"Pterophyllum scalare","tamanho":15,"vida":10,"origem":"América do Sul","alimentacao":"Carnívoro/Onívoro","temp":[24,30],"ph":[6.0,7.5],"gh":[3,15],"litros_min":150,"qtd_min":"casal/grupo","comportamento":"calmo/territorial","nivel":"meio","tipo":"grande","compat_exclui":["peixes pequenos que cabem na boca","peixes muito ativos"]}
]

banco_plantas = [
    {"id":1,"nome":"Anubias Nana","luz":"Baixa","co2":"Não","substrato":"Não — fixar em raiz/pedra","crescimento":"Lento","indicacao":"Iniciante"},
    {"id":2,"nome":"Java Samambaia","luz":"Baixa/Média","co2":"Não","substrato":"Não — fixar em raiz/pedra","crescimento":"Médio","indicacao":"Iniciante"},
    {"id":3,"nome":"Vallisnéria","luz":"Média","co2":"Recomendado","substrato":"Sim","crescimento":"Rápido","indicacao":"Fundo"},
    {"id":4,"nome":"Echinodorus (Amazonica)","luz":"Baixa/Média","co2":"Não","substrato":"Sim","crescimento":"Médio","indicacao":"Meio/fundo"},
    {"id":5,"nome":"Hidrofila","luz":"Média/Alta","co2":"Recomendado","substrato":"Sim","crescimento":"Muito rápido","indicacao":"Fundo/meio"},
    {"id":6,"nome":"Grama de Java","luz":"Média","co2":"Recomendado","substrato":"Sim","crescimento":"Médio","indicacao":"Tapete/fundo"}
]

doencas = [
    {"sintoma":"manchas brancas","nome":"Íctio / Doença dos Pontos Brancos","causa":"Protozoário — espalha rápido por estresse/baixa temperatura","tratamento":"Elevar temperatura para 29–30°C gradualmente | Sal grosso 1 colher/chá por 10L | Medicamento específico por 7–10 dias seguidos","prevencao":"Quarentena de 2–3 semanas em peixes novos | Manter temperatura estável | Alimentação variada para imunidade"},
    {"sintoma":"barbatanas desfiadas","nome":"Podridão de Barbatana","causa":"Bactéria — água suja, agressão entre peixes, estresse","tratamento":"Troca de água 30% | Limpar filtro | Condicionador de água | Se piorar: antibiótico específico","prevencao":"Não superalimentar | Manutenção regular | Não superlotar o aquário"},
    {"sintoma":"peixe na superficie","nome":"Falta de Oxigênio","causa":"Água quente, excesso de matéria orgânica, filtro fraco, pouca circulação","tratamento":"Aumentar circulação/arejamento | Troca de água 25% | Não alimentar por 1 dia","prevencao":"Filtro com fluxo adequado | Plantas equilibradas | Temperatura estável"},
    {"sintoma":"agua turva branca","nome":"Nuvem Bacteriana","causa":"Bactérias se multiplicando — aquário novo, excesso de comida, matéria em decomposição","tratamento":"Paciência! É ciclo natural | Troca de água leve | Melhorar filtragem | Não usar clarificante agora","prevencao":"Ciclar o aquário 3–4 semanas antes dos peixes | Alimentar pouco e retirar sobras"},
    {"sintoma":"perda de cor","nome":"Estresse / Problema de Água","causa":"Variação brusca de pH, nitrato alto, temperatura, companheiros agressivos","tratamento":"Medir pH, amônia, nitrito, nitrato | Troca de água 25% | Adicionar plantas e esconderijos | Observar comportamento","prevencao":"Testes regulares | Trocas parciais semanais | Escolher espécies compatíveis"}
]

# Rotas
@app.route("/")
def inicio():
    return send_from_directory('.', 'index.html')

@app.route("/banco-peixes")
def bp():
    return jsonify(banco_peixes)

@app.route("/banco-plantas")
def bpl():
    return jsonify(banco_plantas)

@app.route("/doencas")
def d():
    return jsonify(doencas)

@app.route("/dados")
def get_dados():
    return jsonify(dados)

@app.route("/salvar-config", methods=["POST"])
def scfg():
    dados["config"].update(request.json)
    salvar_dados()
    return jsonify({"ok": True})

@app.route("/salvar-volume", methods=["POST"])
def sv():
    vol = request.json.get("volume")
    if vol is None:
        return jsonify({"ok": False, "erro": "Faltou o volume"}), 400
    dados["volume"] = vol
    salvar_dados()
    return jsonify({"ok": True})

@app.route("/adicionar-peixe", methods=["POST"])
def ap():
    p = request.json
    if not p or "nome" not in p:
        return jsonify({"ok": False, "erro": "Dados incompletos"}), 400
    p["id"] = len(dados["meus_peixes"]) + 1
    p["data_entrada"] = datetime.now().strftime("%d/%m/%Y")
    dados["meus_peixes"].append(p)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["meus_peixes"]})

@app.route("/adicionar-desejo", methods=["POST"])
def ad():
    p = request.json
    if not p or "nome" not in p:
        return jsonify({"ok": False, "erro": "Dados incompletos"}), 400
    p["id"] = len(dados["desejos"]) + 1
    dados["desejos"].append(p)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["desejos"]})

@app.route("/apagar-desejo/<int:i>", methods=["DELETE"])
def adeld(i):
    if 0 <= i < len(dados["desejos"]):
        dados["desejos"].pop(i)
        salvar_dados()
        return jsonify({"ok": True})
    return jsonify({"ok": False, "erro": "Índice inválido"}), 404

@app.route("/apagar-peixe/<int:i>", methods=["DELETE"])
def dp(i):
    if 0 <= i < len(dados["meus_peixes"]):
        dados["meus_peixes"].pop(i)
        salvar_dados()
        return jsonify({"ok": True})
    return jsonify({"ok": False, "erro": "Índice inválido"}), 404

@app.route("/adicionar-medicao", methods=["POST"])
def am():
    m = request.json
    m["data"] = datetime.now().strftime("%d/%m %H:%M")
    m["dia"] = datetime.now().strftime("%d/%m")
    dados["historico"].append(m)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["historico"]})

@app.route("/adicionar-tarefa", methods=["POST"])
def at():
    t = request.json
    if not t or "nome" not in t:
        return jsonify({"ok": False, "erro": "Dados incompletos"}), 400
    t["id"] = len(dados["tarefas"]) + 1
    t["concluida"] = False
    t["data_criada"] = datetime.now().strftime("%d/%m/%Y")
    dados["tarefas"].append(t)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["tarefas"]})

@app.route("/concluir-tarefa/<int:i>", methods=["PUT"])
def ct(i):
    if 0 <= i < len(dados["tarefas"]):
        dados["tarefas"][i]["concluida"] = not dados["tarefas"][i]["concluida"]
        if dados["tarefas"][i]["concluida"]:
            dados["tarefas"][i]["data_concluida"] = datetime.now().strftime("%d/%m %H:%M")
        else:
            dados["tarefas"][i]["data_concluida"] = None
        salvar_dados()
        return jsonify({"ok": True})
    return jsonify({"ok": False, "erro": "Índice inválido"}), 404

@app.route("/apagar-tarefa/<int:i>", methods=["DELETE"])
def dt(i):
    if 0 <= i < len(dados["tarefas"]):
        dados["tarefas"].pop(i)
        salvar_dados()
        return jsonify({"ok": True})
    return jsonify({"ok": False, "erro": "Índice inválido"}), 404

@app.route("/adicionar-gasto", methods=["POST"])
def ag():
    g = request.json
    if not g or "descricao" not in g:
        return jsonify({"ok": False, "erro": "Dados incompletos"}), 400
    g["id"] = len(dados["gastos"]) + 1
    g["data"] = datetime.now().strftime("%d/%m/%Y")
    dados["gastos"].append(g)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["gastos"]})

@app.route("/adicionar-foto", methods=["POST"])
def af():
    f = request.json
    f["id"] = len(dados["fotos"]) + 1
    f["data"] = datetime.now().strftime("%d/%m/%Y")
    dados["fotos"].append(f)
    salvar_dados()
    return jsonify({"ok": True, "lista": dados["fotos"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
