# scripts/resumo_e_classificacao.py
import os
import requests
import json
from pathlib import Path

# --- Configurações (poderiam vir de config.py) ---
MODELO_OLLAMA = "mistral" # ou outro modelo que você preferir
PALAVRAS_TECNICAS = ["tabela verdade", "porta lógica", "and", "or", "xor", "circuito", "sensor", "binário", "arduino", "processador", "memória", "barramento"]
PALAVRAS_RUIDO = ["moza", "trânsito", "conversas", "boneco", "pet", "telefone", "Curitiba", "motorista", "Uber", "dirigir"] # Adicionadas mais palavras-chave de ruído

def resumir_e_classificar_bloco(conteudo_bloco, model="llama3"):
    """
    Pede à IA para retornar OU um resumo técnico OU uma palavra-chave de descarte.
    """
    prompt_instrucao = f"""Sua tarefa é analisar o texto de uma transcrição de aula e retornar uma de duas coisas. Siga as regras com precisão.

REGRAS:
1. Se o texto contiver conteúdo técnico útil (lógica, hardware, programação, matemática), resuma estes pontos em português. Sua resposta deve ser APENAS o resumo.
2. Se o texto for primariamente uma conversa pessoal, anedota, ou ruído irrelevante, sua resposta deve ser APENAS a palavra-chave exata: RUÍDO_DESCARTAR

Não inclua nenhuma outra palavra, explicação ou formatação na sua resposta.

Texto para análise:
\"\"\"
{conteudo_bloco}
\"\"\"
"""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt_instrucao}],
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=300)
        response.raise_for_status()
        resumo_gerado = response.json()["message"]["content"].strip()

        # Lógica de classificação mais estrita
        if resumo_gerado == "RUÍDO_DESCARTAR":
            classificacao = "❌ Ruído"
            resumo = "Bloco classificado como ruído e descartado." 
        else:
            classificacao = "✅ Útil técnico"
            resumo = resumo_gerado

        return resumo, classificacao

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição ao Ollama: {e}")
        return None, "❌ Erro"
def resumir_blocos(input_dir, output_dir):
    """
    Processa todos os arquivos de bloco em um diretório,
    gera seus resumos e os classifica, salvando-os.
    """
    os.makedirs(output_dir, exist_ok=True)
    arquivos_blocos = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])

    for arquivo in arquivos_blocos:
        caminho_bloco = Path(input_dir) / arquivo
        with open(caminho_bloco, "r", encoding="utf-8") as f:
            conteudo = f.read()

        print(f"  📝 Resumindo e classificando {arquivo}...", end='')
        resumo, classificacao = resumir_e_classificar_bloco(conteudo)

        if resumo:
            nome_saida = arquivo.replace("bloco", "resumo")
            with open(Path(output_dir) / nome_saida, "w", encoding="utf-8") as f_out:
                f_out.write(f"🔹 {nome_saida.replace('.txt','').replace('_', ' ').title()} - {classificacao}\n\n")
                f_out.write(resumo + "\n")
            print(f" {classificacao} - Salvo: {nome_saida}")
        else:
            print(f" Falha ao processar {arquivo}")

if __name__ == "__main__":
    # Exemplo de uso direto: python scripts/resumo_e_classificacao.py blocos/ resumos/
    import sys
    if len(sys.argv) == 3:
        resumir_blocos(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python scripts/resumo_e_classificacao.py <diretorio_entrada_blocos> <diretorio_saida_resumos>")
        
def limpar_bloco_com_ia(texto_bloco, model="llama3"):
    """Usa um modelo de IA para remover ruídos de fala de um bloco de texto."""
    prompt_instrucao = """Sua única tarefa é pegar o texto a seguir, que é parte de uma transcrição de aula, e remover apenas as interjeições, hesitações, palavras de preenchimento (como 'né', 'tipo', 'então', 'aham') e repetições. NÃO altere o conteúdo técnico nem reformule frases. Retorne APENAS o texto limpo."""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": f"{prompt_instrucao}\n\n---TEXTO---\n{texto_bloco}"}],
        "stream": False
    }
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"\nAviso: Falha na limpeza com IA do bloco. Usando texto original. Erro: {e}")
        return texto_bloco