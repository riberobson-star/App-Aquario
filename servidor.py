from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import uuid
import hashlib

app = Flask(__name__, static_folder='.')
CORS(app)

# 🔐 SENHA DO ADMINISTRADOR — ALTERE ABAIXO PARA SUA!
SENHA_ADMIN = "ives123"  # ← COLOQUE A SENHA QUE VOCÊ QUISER!

# BANCO DE DADOS
usuarios = {}
sessoes = {}
sessoes_admin = set()

banco_peixes = [
    {"id":1,"nome":"Tetra Neon","cientifico":"Paracheirodon innesi","tamanho":4,"vida":5,"origem":"América do Sul","alimentacao":"Onívoro","temp":[22,28],"ph":[5.0,7.5],"gh":[1,15],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"meio","tipo":"pequeno"},
    {"id":2,"nome":"Guppy","cientifico":"Poecilia reticulata","tamanho":5,"vida":3,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[6.8,8.5],"gh":[8,30],"litros_min":30,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"superior","tipo":"pequeno"},
    {"id":3,"nome":"Betta Macho","cientifico":"Betta splendens","tamanho":6,"vida":3,"origem":"Tailândia","alimentacao":"Carnívoro","temp":[24,30],"ph":[6.0,8.0],"gh":[5,20],"litros_min":20,"qtd_min":1,"comportamento":"territorial","nivel":"superior","tipo":"medio"},
    {"id":4,"nome":"Coridora Panda","cientifico":"Corydoras panda","tamanho":5,"vida":10,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":60,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno"},
    {"id":5,"nome":"Coridora Anã","cientifico":"Corydoras pygmaeus","tamanho":3.5,"vida":8,"origem":"Brasil","alimentacao":"Onívoro","temp":[22,28],"ph":[6.0,7.5],"gh":[4,12],"litros_min":40,"qtd_min":6,"comportamento":"pacifico","nivel":"fundo","tipo":"pequeno"},
    {"id":6,"nome":"Ancistrus","cientifico":"Ancistrus sp.","tamanho":12,"vida":12,"origem":"América do Sul","alimentacao":"Herbívoro","temp":[20,28],"ph":[6.0,7.5],"gh":[5,20],"litros_min":80,"qtd_min":1,"comportamento":"pacifico","nivel":"fundo-vidro","tipo":"medio"},
    {"id":7,"nome":"Platy","cientifico":"Xiphophorus maculatus","tamanho":6,"vida":4,"origem":"América Central","alimentacao":"Onívoro","temp":[18,28],"ph":[6.8,8.0],"gh":[10,25],"litros_min":40,"qtd_min":"1M+2F","comportamento":"pacifico","nivel":"meio","tipo":"pequeno"},
    {"id":8,"nome":"Espada","cientifico":"Xiphophorus hellerii","tamanho":10,"vida":5,"origem":"América Central","alimentacao":"Onívoro","temp":[20,28],"ph":[7.0,8.5],"gh":[10,30],"litros_min":60,"qtd_min":"1M+2F","comportamento":"ativo","nivel":"meio","tipo":"medio"}
]

banco_plantas = [
    {"id":1,"nome":"Anubias Nana","luz":"Baixa","co2":"Não","substrato":"Não — fixar em raiz","crescimento":"Lento"},
    {"id":2,"nome":"Java Samambaia","luz":"Baixa/Média","co2":"Não","substrato":"Não — fixar em raiz","crescimento":"Médio"},
    {"id":3,"nome":"Vallisnéria","luz":"Média","co2":"Recomendado","substrato":"Sim","crescimento":"Rápido"},
    {"id":4,"nome":"Amazonica","luz":"Baixa/Média","co2":"Não","substrato":"Sim","crescimento":"Médio"}
]

doencas = [
    {"sintoma":"manchas brancas","nome":"Íctio","causa":"Protozoário","tratamento":"Elevar temp p/29-30°C + sal + medicamento específico por 7-10 dias","prevencao":"Quarentena, evitar estresse, temp estável"},
    {"sintoma":"barbatanas desfiadas","nome":"Podridão de Barbatana","causa":"Bactéria / água suja","tratamento":"Troca 30% água + condicionador + medicamento se piorar","prevencao":"Não superalimentar, manutenção regular"},
    {"sintoma":"peixe na superficie","nome":"Falta de Oxigênio","causa":"Água quente, filtro fraco","tratamento":"Aumentar circulação + troca de água","prevencao":"Filtro adequado, não superlotar"},
    {"sintoma":"agua turva branca","nome":"Nuvem Bacteriana","causa":"Ciclo iniciando / excesso de matéria","tratamento":"Paciência! Melhorar filtragem, trocas leves","prevencao":"Ciclar 3-4 semanas antes de peixes"}
]

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ROTAS PÚBLICAS
@app.route("/")
def inicio(): return send_from_directory('.', 'index.html')
@app.route("/banco-peixes")
def bp(): return jsonify(banco_peixes)
@app.route("/banco-plantas")
def bpl(): return jsonify(banco_plantas)
@app.route("/doencas")
def d(): return jsonify(doencas)

# === LOGIN DO ADMINISTRADOR / IVES ===
@app.route("/admin-login", methods=["POST"])
def admin_login():
    dados = request.json
    if dados.get("senha") == SENHA_ADMIN:
        token_admin = str(uuid.uuid4())
        sessoes_admin.add(token_admin)
        return jsonify({"ok": True, "admin_token": token_admin, "nome_dono": "Ives"})
    return jsonify({"ok": False, "erro": "Senha do administrador incorreta"}), 401

# === PAINEL DO DONO — VER TODOS OS USUÁRIOS ===
@app.route("/admin/todos-usuarios", methods=["POST"])
def admin_todos_usuarios():
    token = request.json.get("admin_token")
    if token not in sessoes_admin:
        return jsonify({"ok": False, "erro": "Acesso negado"}), 403
    
    lista = []
    for email, user in usuarios.items():
        lista.append({
            "id": user["id"],
            "nome": user["nome"],
            "email": user["email"],
            "whatsapp": user["whatsapp"],
            "estado": user["estado"],
            "cidade": user["cidade"],
            "data_cadastro": user["data_cadastro"],
            "volume_aquario": user["volume"],
            "qtd_peixes": len(user["meus_peixes"]),
            "qtd_tarefas": len(user["tarefas"]),
            "qtd_gastos": len(user["gastos"]),
            "ultima_atividade": user["historico"][-1]["data"] if user["historico"] else "Sem registro"
        })
    return jsonify({"ok": True, "total": len(lista), "usuarios": lista})

# === VER DADOS COMPLETOS DE 1 USUÁRIO ===
@app.route("/admin/usuario/<email_usuario>", methods=["POST"])
def admin_detalhes_usuario(email_usuario):
    token = request.json.get("admin_token")
    if token not in sessoes_admin:
        return jsonify({"ok": False, "erro": "Acesso negado"}), 403
    if email_usuario not in usuarios:
        return jsonify({"ok": False, "erro": "Usuário não encontrado"}), 404
    
    u = usuarios[email_usuario]
    return jsonify({
        "ok": True,
        "dados": {
            "nome": u["nome"],
            "email": u["email"],
            "whatsapp": u["whatsapp"],
            "estado": u["estado"],
            "cidade": u["cidade"],
            "data_cadastro": u["data_cadastro"],
            "volume": u["volume"],
            "meus_peixes": u["meus_peixes"],
            "historico": u["historico"],
            "tarefas": u["tarefas"],
            "gastos": u["gastos"],
            "desejos": u["desejos"]
        }
    })

# === EXCLUIR USUÁRIO ===
@app.route("/admin/excluir-usuario", methods=["POST"])
def admin_excluir_usuario():
    token = request.json.get("admin_token")
    email = request.json.get("email")
    if token not in sessoes_admin:
        return jsonify({"ok": False, "erro": "Acesso negado"}), 403
    if email in usuarios:
        del usuarios[email]
        for sessao, e in list(sessoes.items()):
            if e == email: del sessoes[sessao]
        return jsonify({"ok": True, "mensagem": "Usuário excluído com sucesso"})
    return jsonify({"ok": False, "erro": "Usuário não encontrado"}), 404

# === SAIR DO PAINEL ADMIN ===
@app.route("/admin-sair", methods=["POST"])
def admin_sair():
    token = request.json.get("admin_token")
    if token in sessoes_admin: sessoes_admin.remove(token)
    return jsonify({"ok": True})

# === CADASTRO DE USUÁRIO ===
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    dados = request.json
    obrigatorios = ["nome", "email", "senha", "whatsapp", "estado", "cidade"]
    for campo in obrigatorios:
        if not dados.get(campo, "").strip():
            return jsonify({"ok":False, "erro":f"Preencha o campo: {campo}"}), 400
    
    email = dados["email"].strip().lower()
    if email in usuarios:
        return jsonify({"ok":False, "erro":"E-mail já cadastrado!"}), 409
    
    user_id = str(uuid.uuid4())
    usuarios[email] = {
        "id": user_id,
        "nome": dados["nome"].strip(),
        "email": email,
        "senha_hash": hash_senha(dados["senha"]),
        "whatsapp": dados["whatsapp"].strip(),
        "estado": dados["estado"].strip().upper(),
        "cidade": dados["cidade"].strip(),
        "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "volume": 0,
        "meus_peixes": [],
        "desejos": [],
        "historico": [],
        "tarefas": [],
        "gastos": [],
        "config": {"modo_escuro":False}
    }
    return jsonify({"ok":True, "mensagem":"Cadastro realizado! Faça login."})

# === LOGIN USUÁRIO ===
@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")
    
    if email not in usuarios:
        return jsonify({"ok":False, "erro":"E-mail não encontrado"}), 404
    if usuarios[email]["senha_hash"] != hash_senha(senha):
        return jsonify({"ok":False, "erro":"Senha incorreta"}), 401
    
    sessao_id = str(uuid.uuid4())
    sessoes[sessao_id] = email
    return jsonify({
        "ok":True,
        "sessao": sessao_id,
        "usuario": {
            "nome": usuarios[email]["nome"],
            "email": usuarios[email]["email"],
            "whatsapp": usuarios[email]["whatsapp"],
            "estado": usuarios[email]["estado"],
            "cidade": usuarios[email]["cidade"]
        }
    })

# === DADOS DO USUÁRIO ===
@app.route("/meus-dados", methods=["POST"])
def meus_dados():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes:
        return jsonify({"ok":False, "erro":"Não autorizado"}), 401
    u = usuarios[sessoes[sessao_id]]
    return jsonify({"ok":True, "dados": u})

# === SALVAR DADOS DO AQUÁRIO ===
@app.route("/salvar-volume", methods=["POST"])
def sv():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    usuarios[sessoes[sessao_id]]["volume"] = request.json["volume"]
    return jsonify({"ok":True})

@app.route("/adicionar-peixe", methods=["POST"])
def ap():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    p = request.json
    p["data"] = datetime.now().strftime("%d/%m/%Y")
    del p["sessao"]
    usuarios[sessoes[sessao_id]]["meus_peixes"].append(p)
    return jsonify({"ok":True})

@app.route("/apagar-peixe/<int:i>", methods=["DELETE"])
def dp(i):
    sessao_id = request.args.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    lista = usuarios[sessoes[sessao_id]]["meus_peixes"]
    if 0<=i<len(lista): lista.pop(i)
    return jsonify({"ok":True})

@app.route("/adicionar-medicao", methods=["POST"])
def am():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    m = request.json
    m["data"] = datetime.now().strftime("%d/%m %H:%M")
    del m["sessao"]
    usuarios[sessoes[sessao_id]]["historico"].append(m)
    return jsonify({"ok":True})

@app.route("/adicionar-tarefa", methods=["POST"])
def at():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    t = request.json
    t["concluida"] = False
    del t["sessao"]
    usuarios[sessoes[sessao_id]]["tarefas"].append(t)
    return jsonify({"ok":True})

@app.route("/concluir-tarefa/<int:i>", methods=["PUT"])
def ct(i):
    sessao_id = request.args.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    lista = usuarios[sessoes[sessao_id]]["tarefas"]
    if 0<=i<len(lista): lista[i]["concluida"] = not lista[i]["concluida"]
    return jsonify({"ok":True})

@app.route("/apagar-tarefa/<int:i>", methods=["DELETE"])
def dt(i):
    sessao_id = request.args.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    lista = usuarios[sessoes[sessao_id]]["tarefas"]
    if 0<=i<len(lista): lista.pop(i)
    return jsonify({"ok":True})

@app.route("/adicionar-gasto", methods=["POST"])
def ag():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    g = request.json
    g["data"] = datetime.now().strftime("%d/%m/%Y")
    del g["sessao"]
    usuarios[sessoes[sessao_id]]["gastos"].append(g)
    return jsonify({"ok":True})

@app.route("/adicionar-desejo", methods=["POST"])
def ad():
    sessao_id = request.json.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    d = request.json
    del d["sessao"]
    usuarios[sessoes[sessao_id]]["desejos"].append(d)
    return jsonify({"ok":True})

@app.route("/apagar-desejo/<int:i>", methods=["DELETE"])
def adeld(i):
    sessao_id = request.args.get("sessao")
    if sessao_id not in sessoes: return jsonify({"ok":False}), 401
    lista = usuarios[sessoes[sessao_id]]["desejos"]
    if 0<=i<len(lista): lista.pop(i)
    return jsonify({"ok":True})

@app.route("/sair", methods=["POST"])
def sair():
    sessao_id = request.json.get("sessao")
    if sessao_id in sessoes: del sessoes[sessao_id]
    return jsonify({"ok":True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))
