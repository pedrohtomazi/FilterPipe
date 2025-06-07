import os

PASTA_RESUMOS = "resumos"
ARQUIVO_SAIDA = "resumo_final.txt"

arquivos = sorted([f for f in os.listdir(PASTA_RESUMOS) if f.startswith("resumo_") and f.endswith(".txt")])

with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
    for arq in arquivos:
        caminho = os.path.join(PASTA_RESUMOS, arq)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
            saida.write(f"🔹 {arq.replace('.txt', '').replace('_', ' ').title()}\n\n")
            saida.write(conteudo + "\n\n")
