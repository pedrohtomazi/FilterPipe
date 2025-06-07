import os
import requests
import json

PASTA_BLOCOS = "blocos"
PASTA_RESUMOS = "resumos"
MODELO = "mistral"  # já instalado no Ollama

# Prompt básico ajustado pra transcrição suja
PROMPT_INSTRUCAO = """
Esse texto veio de uma transcrição de aula com erros de fala. Reescreva o conteúdo com clareza, mantendo os pontos técnicos e eliminando repetições, pausas e interjeições. Retorne um resumo estruturado e didático.
"""

os.makedirs(PASTA_RESUMOS, exist_ok=True)

arquivos_blocos = sorted([f for f in os.listdir(PASTA_BLOCOS) if f.endswith(".txt")])

for arquivo in arquivos_blocos:
    caminho_bloco = os.path.join(PASTA_BLOCOS, arquivo)
    with open(caminho_bloco, "r", encoding="utf-8") as f:
        conteudo = f.read()

    print(f"📄 Resumindo {arquivo}...")

    payload = {
        "model": MODELO,
        "messages": [
            {"role": "system", "content": "Você é um assistente especialista em transcrever e organizar aulas técnicas."},
            {"role": "user", "content": PROMPT_INSTRUCAO + "\n\n" + conteudo}
        ],
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/chat", json=payload)
    resposta = response.json()["message"]["content"]

    nome_saida = arquivo.replace("bloco", "resumo")
    with open(os.path.join(PASTA_RESUMOS, nome_saida), "w", encoding="utf-8") as f:
        f.write(resposta)

    print(f"✅ Salvo: {nome_saida}")