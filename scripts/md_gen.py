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

def filtrar_e_agrupar_resumos(resumo_dir):
    """
    Lê os resumos classificados, filtra os úteis e os agrupa por tema.
    Retorna um dicionário {tema: [resumo_texto_formatado]}.
    """
    blocos_por_tema = {tema: [] for tema in TEMAS}
    arquivos_resumos = sorted([f for f in os.listdir(resumo_dir) if f.startswith("resumo_") and f.endswith(".txt")])

    for arq_nome in arquivos_resumos:
        caminho_resumo = Path(resumo_dir) / arq_nome
        with open(caminho_resumo, "r", encoding="utf-8") as f:
            conteudo_completo = f.read().strip()

        # Extrai a classificação e o conteúdo do resumo
        match = re.match(r"🔹 (Resumo[_\s]\d+.*?) - (✅ Útil técnico|❌ Ruído|⚠️ Parcial)\n\n(.*)", conteudo_completo, re.DOTALL)
        if not match:
            print(f"Aviso: Formato inesperado para o arquivo {arq_nome}. Pulando.")
            continue

        titulo_bloco_original, classificacao, conteudo_resumo = match.groups()

        if classificacao == "✅ Útil técnico":
            # Tenta categorizar o resumo útil em um tema
            encontrou_tema = False
            for tema, palavras_chave in TEMAS.items():
                if any(pc.lower() in conteudo_resumo.lower() for pc in palavras_chave):
                    blocos_por_tema[tema].append(f"### 📌 {titulo_bloco_original.replace('Resumo_', 'Resumo ').title()}\n\n{conteudo_resumo}")
                    encontrou_tema = True
                    break
            if not encontrou_tema:
                # Se não encaixar em nenhum tema específico, adiciona a um tema genérico ou inicial
                if "Outros Tópicos Técnicos" not in blocos_por_tema:
                    blocos_por_tema["Outros Tópicos Técnicos"] = []
                blocos_por_tema["Outros Tópicos Técnicos"].append(f"### 📌 {titulo_bloco_original.replace('Resumo_', 'Resumo ').title()}\n\n{conteudo_resumo}")
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

def refinar_markdown_com_ollama(input_md_path, output_md_path):
    """
    Chama o modelo Ollama para revisar o arquivo Markdown gerado.
    """
    with open(input_md_path, "r", encoding="utf-8") as f:
        conteudo_md = f.read()

    prompt_refinamento = f"""
Sua tarefa é corrigir e reescrever um documento Markdown em Português do Brasil. O documento original contém erros técnicos, de digitação e seções irrelevantes.

REGRAS ESTRITAS:
1.  **CORRIJA O CONTEÚDO TÉCNICO:** Corrija todas as informações, lógicas e cálculos que estiverem errados. Substitua palavras sem sentido (ex: 'Zoukê', 'nárdo', 'schusnor') pela palavra técnica correta, se o contexto permitir.
2.  **MANTENHA A ESTRUTURA:** Preserve 100% da estrutura de cabeçalhos Markdown (`## 🧠 Tópico` e `### 📌 Resumo XXX`). Não junte ou mescle seções de resumo.
3.  **REESCREVA COM CLAREZA:** Melhore a clareza e a fluidez do texto, mas NÃO RESUMA. O objetivo é uma versão corrigida e melhorada, com um nível de detalhe similar ao original.
4.  **REMOVA RUÍDO:** Se uma seção inteira (`### 📌 Resumo XXX`) for apenas uma história pessoal ou anedota não-técnica (ex: sobre dirigir, animais de estimação, etc.), remova a seção inteira, incluindo seu cabeçalho.
5.  **IDIOMA:** A saída final deve ser inteiramente em Português do Brasil.

A seguir, um exemplo de como você deve transformar o texto:

---EXEMPLO DE ENTRADA---
### 📌 Resumo 013
Processador é responsável por executar microcódigos no LAN e pegar elemento no Zoukê. Não há questões ativas na prova.
---EXEMPLO DE SAÍDA CORRIGIDA---
### 📌 Resumo 013
O processador é responsável por executar microcódigos. Também é mencionado que não haverá questões discursivas ("ativas") na prova do Blackboard.
---FIM DO EXEMPLO---

Agora, processe o documento completo a seguir. Retorne APENAS o documento Markdown final e corrigido.

DOCUMENTO ORIGINAL:
\"\"\"
{conteudo_md}
\"\"\"
"""

    print(f"  ⏳ Aplicando refinamento com {MODELO_OLLAMA_REFINAMENTO} (isso pode levar um tempo)...", end='', flush=True)

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
        # Se o Ollama falhar, copia o arquivo bruto para o revisado
        shutil.copyfile(input_md_path, output_md_path)
    else:
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(saida_completa)
        print(" ✅ Refinamento concluído!")

if __name__ == "__main__":
    # Exemplo de uso direto para gerar Markdown:
    # python scripts/md_gen.py resumos/ mds/ resumo_final_bruto.md
    # Exemplo de uso direto para refinar (assumindo que o resumo_final_bruto.md já existe):
    # python scripts/md_gen.py --refine mds/resumo_final_bruto.md mds/resumo_final_revisado.md

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--refine":
        if len(sys.argv) == 4:
            refinar_markdown_com_ollama(sys.argv[2], sys.argv[3])
        else:
            print("Uso para refinamento: python scripts/md_gen.py --refine <arquivo_entrada_md> <arquivo_saida_md_revisado>")
    elif len(sys.argv) == 4:
        gerar_markdown_final(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Uso para geração de Markdown: python scripts/md_gen.py <diretorio_resumos> <diretorio_saida_md> <nome_arquivo_md>")