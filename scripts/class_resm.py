# scripts/resumo_e_classificacao.py
import os
import requests
import json
from pathlib import Path

# --- Configurações (poderiam vir de config.py) ---
MODELO_OLLAMA = "mistral" # ou outro modelo que você preferir
PALAVRAS_TECNICAS = ["tabela verdade", "porta lógica", "and", "or", "xor", "circuito", "sensor", "binário", "arduino", "processador", "memória", "barramento"]
PALAVRAS_RUIDO = ["moza", "trânsito", "conversas", "boneco", "pet", "telefone", "Curitiba", "motorista", "Uber", "dirigir"] # Adicionadas mais palavras-chave de ruído

def classificar_texto(texto):
    """Classifica um texto como útil técnico, ruído ou parcial baseado em palavras-chave."""
    texto_lower = texto.lower()

    score_tecnico = sum(texto_lower.count(p) for p in PALAVRAS_TECNICAS)
    score_ruido = sum(texto_lower.count(p) for p in PALAVRAS_RUIDO)

    if score_tecnico > score_ruido * 1.5: # Prioriza técnico se houver uma clara vantagem
        return "✅ Útil técnico"
    elif score_ruido > score_tecnico * 1.5: # Prioriza ruído se houver uma clara vantagem
        return "❌ Ruído"
    elif score_tecnico > 0: # Se houver algum termo técnico e não for predominantemente ruído
        return "✅ Útil técnico"
    elif score_ruido > 0: # Se houver algum termo de ruído e não for predominantemente técnico
        return "❌ Ruído"
    else:
        return "⚠️ Parcial" # Para casos ambíguos ou sem palavras-chave claras

def resumir_e_classificar_bloco(conteudo_bloco, model=MODELO_OLLAMA):
    """
    Chama o Ollama para resumir um bloco e classifica o resumo.
    Retorna o resumo gerado e sua classificação.
    """
    prompt_instrucao = """
    Você é um assistente especialista em transcrever e organizar aulas técnicas.
    O texto a seguir veio de uma transcrição de aula com erros de fala.
    Reescreva o conteúdo com clareza, mantendo APENAS os pontos técnicos e eliminando completamente repetições, pausas, interjeições e CONTEÚDO NÃO TÉCNICO (conversas paralelas, anedotas, discussões não relacionadas ao assunto principal).
    Retorne um resumo estruturado e didático, focado na explicação técnica.
    """

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Você é um assistente especialista em transcrever e organizar aulas técnicas."},
            {"role": "user", "content": prompt_instrucao + "\n\n" + conteudo_bloco}
        ],
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=300) # Aumentar timeout
        response.raise_for_status() # Lança exceção para erros HTTP
        resumo_gerado = response.json()["message"]["content"]
        classificacao = classificar_texto(resumo_gerado)
        return resumo_gerado, classificacao
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão com o Ollama: {e}. Certifique-se de que o Ollama está rodando e o modelo '{model}' está baixado.")
        return None, "❌ Erro"
    except requests.exceptions.Timeout:
        print(f"Timeout ao conectar ou receber resposta do Ollama para o modelo '{model}'.")
        return None, "❌ Erro"
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