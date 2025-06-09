# scripts/md_gen.py
import re
import os
import subprocess
import time
import shutil
from pathlib import Path

# --- Configurações (poderiam vir de config.py) ---
MODELO_OLLAMA_REFINAMENTO = "llama3" # Modelo para refinamento final (pode ser diferente do de resumo)

# Temas e palavras-chave (para agrupamento e filtragem)
TEMAS = {
    "Portas Lógicas": ["porta lógica", "and", "or", "xor", "xnor", "equações booleanas", "tabela verdade"],
    "Sensores e Sinalização": ["sensor", "arduino", "carrinho", "sumôbots", "luzes", "sinalização", "estacionamento", "cancela"],
    "Sistemas Numéricos e Operações": ["binário", "decimal", "hexadecimal", "conversão", "soma", "subtração", "sistema posicional", "expoente"],
    "Hardware e Arquitetura de Computadores": ["processador", "memória", "interface", "periférico", "fonte", "gabinete", "monitor", "bios", "pci express", "barramento", "microcódigos"],
}

# Dentro de scripts/md_gen.py
def filtrar_e_agrupar_resumos(resumo_dir):
    """
    Lê os resumos extraídos, filtra os úteis (ignorando os marcados como sem informação)
    e os agrupa por tema.
    """
    blocos_por_tema = {tema: [] for tema in TEMAS}
    arquivos_resumos = sorted([f for f in os.listdir(resumo_dir) if f.startswith("resumo_") and f.endswith(".txt")])

    for arq_nome in arquivos_resumos:
        caminho_resumo = Path(resumo_dir) / arq_nome
        with open(caminho_resumo, "r", encoding="utf-8") as f:
            conteudo_resumo = f.read().strip()

        # >>> INÍCIO DA ALTERAÇÃO <<<
        # Nova lógica de filtragem: ignora se for a palavra-chave ou se estiver vazio.
        if "SEM_INFO_UTIL" in conteudo_resumo or not conteudo_resumo:
            print(f"  -> Ignorando {arq_nome}: Sem conteúdo técnico.")
            continue
        # >>> FIM DA ALTERAÇÃO <<<

        titulo_bloco_original = arq_nome.replace('.txt', '').replace('_', ' ').title()

        encontrou_tema = False
        for tema, palavras_chave in TEMAS.items():
            if any(pc.lower() in conteudo_resumo.lower() for pc in palavras_chave):
                blocos_por_tema[tema].append(f"### 📌 {titulo_bloco_original}\n\n{conteudo_resumo}")
                encontrou_tema = True
                print(f"  -> Agrupando {arq_nome} no tema '{tema}'.")
                break
        
        if not encontrou_tema:
            if "Outros Tópicos Técnicos" not in blocos_por_tema:
                blocos_por_tema["Outros Tópicos Técnicos"] = []
            blocos_por_tema["Outros Tópicos Técnicos"].append(f"### 📌 {titulo_bloco_original}\n\n{conteudo_resumo}")
            print(f"  -> Agrupando {arq_nome} em 'Outros Tópicos'.")

    return blocos_por_tema


def gerar_markdown_final(resumo_dir, output_dir, output_filename):
    """
    Gera o arquivo Markdown final a partir dos resumos filtrados e agrupados.
    """
    blocos_por_tema = filtrar_e_agrupar_resumos(resumo_dir)
    markdown_path = Path(output_dir) / output_filename

    with open(markdown_path, "w", encoding="utf-8") as f_md:
        f_md.write("# 📘 Resumo Final – Aula Xiscatti\n")

        for tema, blocos in blocos_por_tema.items():
            if blocos: # Escreve o tema apenas se houver blocos associados
                f_md.write(f"\n## 🧠 {tema}\n")
                for bloco_conteudo in blocos:
                    f_md.write(f"\n{bloco_conteudo}\n")
                    f_md.write("——————————————————————————————————————————————————\n") # Separador entre resumos

    print(f"Resumo bruto em Markdown gerado em: {markdown_path}")

# Em scripts/md_gen.py

def refinar_markdown_com_ollama(input_md_path, output_md_path):
    """
    Chama o modelo Ollama para atuar como um REVISOR TÉCNICO, corrigindo o
    conteúdo sem alterar a estrutura.
    """
    with open(input_md_path, "r", encoding="utf-8") as f:
        conteudo_md = f.read()

    # >>> PROMPT DE REFINAMENTO ALTAMENTE RESTRITIVO <<<
    prompt_refinamento = f"""
Sua tarefa é atuar como um **revisor técnico (proofreader)**. Sua única função é corrigir e polir o documento Markdown abaixo. Você **NÃO DEVE** alterar a estrutura, o formato ou o nível de detalhe do texto.

**REGRAS ABSOLUTAS E INQUEBRÁVEIS:**
1.  **CORREÇÃO DE CONTEÚDO TÉCNICO:** Corrija **apenas** erros factuais ou técnicos no texto. Por exemplo, se um cálculo estiver errado (ex: `1+1=0`), corrija-o para a resposta correta no contexto binário (ex: `1+1=10(2)`). Se um conceito estiver mal explicado (ex: `a porta XNOR dá 0 para entradas iguais`), corrija-o.
2.  **CORREÇÃO DE TEXTO BÁSICO:** Corrija erros de digitação, gramática e pontuação. Melhore a clareza das frases, mas sem alterar seu significado ou comprimento.
3.  **MANTER A ESTRUTURA 100%:** A estrutura de cabeçalhos (`##`, `###`) e de TÓPICOS (bullet points como `*` ou `-`) deve ser **PRESERVADA IDENTICAMENTE**. É PROIBIDO transformar listas de tópicos em parágrafos.
4.  **NÃO RESUMIR:** O nível de detalhe de cada tópico deve ser mantido. Não remova informações, exemplos ou bullet points para encurtar o texto.
5.  **SAÍDA DIRETA:** Retorne APENAS o documento Markdown corrigido, mantendo o formato original.

DOCUMENTO BRUTO PARA CORREÇÃO:
\"\"\"
{conteudo_md}
\"\"\"
"""

    print(f"  🛠️  Aplicando revisão técnica com {MODELO_OLLAMA_REFINAMENTO} (isso pode levar um tempo)...", end='', flush=True)

    processo = subprocess.Popen(
        ["ollama", "run", MODELO_OLLAMA_REFINAMENTO],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    processo.stdin.write(prompt_refinamento.encode('utf-8'))
    processo.stdin.close()

    saida_bruta = []
    erros_brutos = []

    while True:
        stdout_line = processo.stdout.readline()
        stderr_line = processo.stderr.readline()

        if stdout_line:
            saida_bruta.append(stdout_line)
        if stderr_line:
            erros_brutos.append(stderr_line)

        if not stdout_line and not stderr_line and processo.poll() is not None:
            break
        time.sleep(0.05)

    saida_completa = b"".join(saida_bruta).decode('utf-8').strip()
    erros_completo = b"".join(erros_brutos).decode('utf-8').strip()

    returncode = processo.wait()

    if returncode != 0:
        print(f"\n❌ ERRO do Ollama (código {returncode}):")
        print(f"Detalhes do erro: {erros_completo}")
        print("Continuando sem o refinamento. O arquivo gerado será o 'bruto'.")
        shutil.copyfile(input_md_path, output_md_path)
    else:
        # Garante que o ollama não adicionou texto extra
        if "```" in saida_completa:
             saida_completa = re.search(r'```markdown\n(.*?)\n```', saida_completa, re.DOTALL).group(1)

        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(saida_completa)
        print(" ✅ Revisão concluída!")

# (A parte if __name__ == "__main__" continua a mesma)