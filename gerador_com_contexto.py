# gerador_com_contexto.py
import subprocess
from pathlib import Path

# --- Arquivos de Entrada ---
ARQUIVO_SLIDES = "slides_extraidos.txt"
ARQUIVO_TRANSCRICAO = "docs_temp/transcricao_limpa_temp.txt"

# --- Arquivo de Saída ---
ARQUIVO_SAIDA = "resumo_final_de_alta_qualidade.md"

# --- Modelo Ollama ---
MODELO_OLLAMA = "llama3"

def gerar_resumo_contextualizado():
    """
    Gera um resumo de alta qualidade combinando o texto dos slides (contexto)
    com a transcrição da aula (detalhes).
    """
    try:
        with open(ARQUIVO_SLIDES, 'r', encoding='utf-8') as f:
            conteudo_slides = f.read()
        with open(ARQUIVO_TRANSCRICAO, 'r', encoding='utf-8') as f:
            conteudo_transcricao = f.read()
    except FileNotFoundError as e:
        print(f"🚨 ERRO: Arquivo não encontrado: {e.filename}")
        print("Certifique-se que os arquivos 'slides_extraidos.txt' e 'docs_temp/transcricao_limpa_temp.txt' existem.")
        return

    # O prompt final que usa as duas fontes de informação
    prompt_com_contexto = f"""
Você é um especialista em criar materiais de estudo claros e eficientes. Sua tarefa é criar um resumo de alta qualidade de uma aula sobre eletrônica digital, usando duas fontes:

1.  **TEXTO DOS SLIDES (A ESTRUTURA E OS TERMOS CORRETOS):** Este texto é sua fonte da verdade para os tópicos, a ordem e a grafia correta dos termos técnicos.
2.  **TRANSCRIÇÃO DA AULA (AS EXPLICAÇÕES DETALHADAS):** Este texto contém a fala do professor, com exemplos, detalhes e o raciocínio por trás dos conceitos. Está cheio de erros de transcrição e conversas informais.

**INSTRUÇÕES:**

1.  **USE OS SLIDES COMO GUIA:** Baseie a estrutura do seu resumo nos tópicos apresentados nos slides. Use os termos dos slides para corrigir os erros da transcrição (ex: se a transcrição diz 'porta a bosta' e os slides mencionam 'Portas Lógicas', use 'Portas Lógicas').
2.  **USE A TRANSCRIÇÃO PARA EXPLICAR:** Preencha cada tópico dos slides com as explicações, exemplos e detalhes que você encontrar na transcrição da fala do professor.
3.  **SINTETIZE, NÃO APENAS JUNTE:** Combine as informações das duas fontes para criar um texto coeso e didático.
4.  **IGNORE O RUÍDO:** Descarte todas as histórias pessoais, opiniões e conversas informais da transcrição.
5.  **FORMATAÇÃO DE ALTA QUALIDADE:**
    * Crie um título geral para o resumo (começando com 📘).
    * Crie seções para cada grande tema (começando com 🔹).
    * Use bullet points (`*`) para detalhar os conceitos e **negrito** para termos importantes.

---
**FONTE 1: TEXTO DOS SLIDES (GUIA ESTRUTURAL)**
---
{conteudo_slides}
---
**FONTE 2: TRANSCRIÇÃO DA AULA (EXPLICAÇÕES E DETALHES)**
---
{conteudo_transcricao}
---

Agora, com base nas duas fontes e seguindo todas as instruções, gere o resumo de estudo final.
"""

    print(f"✅ Arquivos lidos. Combinando slides e transcrição para o modelo {MODELO_OLLAMA}...")
    print("⏳ Gerando o resumo final... Isso pode levar alguns minutos.")

    try:
        processo = subprocess.run(
            ["ollama", "run", MODELO_OLLAMA],
            input=prompt_com_contexto,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        
        resultado_final = processo.stdout.strip()
        
        with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
            f.write(resultado_final)
            
        print(f"🎉 Resumo de alta qualidade gerado com sucesso!")
        print(f"Verifique o arquivo: {ARQUIVO_SAIDA}")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao executar o Ollama: {e}")


if __name__ == "__main__":
    gerar_resumo_contextualizado()