# scripts/class_resm.py (Versão aprimorada para extração técnica)
import os
import requests
from pathlib import Path

MODELO_OLLAMA = "llama3"

# Em scripts/class_resm.py

def extrair_resumo_tecnico(conteudo_bloco):
    """
    Pede à IA para extrair e resumir o conteúdo técnico de um bloco de forma DETALHADA.
    """
    # >>> PROMPT MODIFICADO <<<
    prompt_extracao = f"""
Sua tarefa é atuar como um transcritor técnico. Analise o bloco de texto de uma aula, que mistura conteúdo técnico com conversas informais.

REGRAS ESTRITAS:
1.  **EXTRAIA E DETALHE O CONTEÚDO TÉCNICO:** Identifique todas as explicações técnicas, conceitos, definições e exemplos. Em vez de um resumo curto, crie um **resumo detalhado** em formato de TÓPICOS (bullet points). Preserve exemplos numéricos e o raciocínio do professor. O objetivo é criar um material de estudo útil e completo a partir deste bloco.
2.  **IGNORE O RUÍDO:** Ignore completamente as conversas pessoais, anedotas e opiniões.
3.  **SE NADA FOR ÚTIL:** Se o bloco de texto contiver **APENAS** ruído e absolutamente nenhuma informação técnica, sua resposta deve ser a palavra-chave exata: `SEM_INFO_UTIL`.
4.  **SAÍDA DIRETA:** Sua resposta deve ser ou o resumo técnico detalhado ou a palavra-chave. Não inclua saudações ou explicações.

Texto para análise:
\"\"\"
{conteudo_bloco}
\"\"\"
"""
    payload = {
        "model": MODELO_OLLAMA,
        "messages": [{"role": "user", "content": prompt_extracao}],
        "stream": False,
        # Aumentar a temperatura incentiva respostas um pouco mais criativas e detalhadas.
        "options": {"temperature": 0.2}
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"\nErro na requisição ao Ollama: {e}")
        return "SEM_INFO_UTIL"

def resumir_blocos(input_dir, output_dir):
    """
    Processa todos os arquivos de bloco, extrai os resumos técnicos e salva o resultado.
    """
    os.makedirs(output_dir, exist_ok=True)
    arquivos_blocos = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])

    for arquivo in arquivos_blocos:
        caminho_bloco = Path(input_dir) / arquivo
        with open(caminho_bloco, "r", encoding="utf-8") as f:
            conteudo = f.read()

        print(f"  🔎 Extraindo conteúdo técnico de {arquivo}...")
        resumo = extrair_resumo_tecnico(conteudo)

        if resumo:
            nome_saida = arquivo.replace("bloco", "resumo")
            with open(Path(output_dir) / nome_saida, "w", encoding="utf-8") as f_out:
                f_out.write(resumo)
        else:
            print(f"  ❌ Falha ao processar {arquivo}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        resumir_blocos(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python scripts/class_resm.py <diretorio_entrada_blocos> <diretorio_saida_resumos>")