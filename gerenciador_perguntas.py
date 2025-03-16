import json
import os

# Diretório para salvar perguntas não respondidas
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
SUGESTOES_FILE = os.path.join(LOG_DIR, "respostas_sugeridas.json")
NAO_RESPONDIDAS_FILE = os.path.join(LOG_DIR, "perguntas_nao_respondidas.json")

# Criar diretório de logs se não existir
os.makedirs(LOG_DIR, exist_ok=True)

# 🔹 Criar o arquivo perguntas_nao_respondidas.json se não existir
if not os.path.exists(NAO_RESPONDIDAS_FILE):
    with open(NAO_RESPONDIDAS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# 🔹 Criar o arquivo respostas_sugeridas.json se não existir
if not os.path.exists(SUGESTOES_FILE):
    with open(SUGESTOES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# 📌 Função para verificar respostas sugeridas
def buscar_resposta_sugerida(pergunta):
    """Verifica se há uma resposta sugerida salva no JSON."""
    with open(SUGESTOES_FILE, "r", encoding="utf-8") as f:
        base = json.load(f)

    for item in base:
        if item["pergunta"].lower() == pergunta.lower():
            return item["resposta"]

    return None

# 📌 Função para salvar perguntas sem resposta no JSON
def salvar_pergunta_nao_respondida(pergunta, resposta):
    """Salva perguntas sem resposta no JSON."""
    with open(NAO_RESPONDIDAS_FILE, "r", encoding="utf-8") as f:
        perguntas_nao_respondidas = json.load(f)

    perguntas_nao_respondidas.append({"pergunta": pergunta, "resposta": resposta})

    with open(NAO_RESPONDIDAS_FILE, "w", encoding="utf-8") as f:
        json.dump(perguntas_nao_respondidas, f, indent=4, ensure_ascii=False)

# 📌 Função para validar se a resposta gerada é útil
def resposta_valida(resposta, limite_palavras=5):
    """Valida se a resposta não é genérica ou vazia."""
    respostas_invalidas = [
        "não sei", "não consegui encontrar", "não há informação",
        "não consigo responder", "informação indisponível", "não encontrei",
        "desculpe, não entendi"
    ]

    resposta_lower = resposta.lower().strip()

    if any(neg in resposta_lower for neg in respostas_invalidas):
        return False

    if len(resposta.split()) <= limite_palavras and resposta_lower not in ["olá", "oi", "bom dia", "boa tarde", "boa noite"]:
        return False

    return True