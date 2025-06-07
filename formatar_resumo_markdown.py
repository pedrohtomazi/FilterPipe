import re

ENTRADA = "resumo_final_util.txt"
SAIDA = "resumo_final.md"

# Temas e palavras-chave
TEMAS = {
    "Portas Lógicas": [2, 3],
    "Sensores e Sinalização": [5, 6, 7, 10],
    "Hardware e Prova": [13, 14],
}

import re

def extrair_blocos_util(texto):
    blocos = re.findall(r"(🔹 Resumo_(\d+).*?)(?=🔹 Resumo_\d+|\Z)", texto, re.DOTALL)
    blocos_util = {tema: [] for tema in TEMAS}

    for bloco, idx in blocos:
        idx = int(idx)
        for tema, indices in TEMAS.items():
            if idx in indices:
                blocos_util[tema].append(bloco.strip())
    return blocos_util

def formatar_markdown(blocos_por_tema):
    linhas = ["# 📘 Resumo Final – Aula Xiscatti\n"]
    for tema, blocos in blocos_por_tema.items():
        linhas.append(f"\n## 🧠 {tema}\n")
        for bloco in blocos:
            # Separar título e conteúdo
            partes = bloco.split("\n", 1)
            titulo = partes[0].replace("🔹", "### 📌").strip()
            conteudo = partes[1].strip() if len(partes) > 1 else ""
            linhas.append(f"\n{titulo}\n\n{conteudo}\n")
    return "\n".join(linhas)

# Execução
with open(ENTRADA, "r", encoding="utf-8") as f:
    conteudo = f.read()

blocos_util = extrair_blocos_util(conteudo)
markdown_formatado = formatar_markdown(blocos_util)

with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(markdown_formatado)

print(f"✅ Resumo formatado salvo como: {SAIDA}")
