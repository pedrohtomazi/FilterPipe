import re

ENTRADA = "resumo_final_util.txt"
SAIDA = "resumo_final_formatado.txt"

with open(ENTRADA, "r", encoding="utf-8") as f:
    texto = f.read()

# Substituir marcadores por títulos limpos
texto = re.sub(r"🔹 Resumo_\d+ - ✅ Útil técnico", lambda m: f"\n\n📌 {m.group(0).split(' - ')[0].replace('_', ' ')}", texto)

# Remover repetições de "Resumo:" e deixar só uma estrutura padrão
texto = re.sub(r"\*\*Resumo:\*\*", "", texto)
texto = re.sub(r"Resumo estruturado da aula:", "", texto)
texto = re.sub(r"Resumo da Aula:", "", texto)
texto = re.sub(r"Resumo:", "", texto)

# Remover espaços e quebras múltiplas
texto = re.sub(r"\n{3,}", "\n\n", texto)
texto = re.sub(r"[ \t]+$", "", texto, flags=re.MULTILINE)

# Adiciona separador visual entre os blocos
texto = re.sub(r"(📌 Resumo_\d+)", r"\n\n—\1—\n", texto)

# Salvar saída
with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(texto)

print(f"✅ Resumo formatado salvo em: {SAIDA}")
