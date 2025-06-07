ARQUIVO_ENTRADA = "resumos_classificados.txt"
ARQUIVO_SAIDA = "resumo_final_util.txt"

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as entrada:
    conteudo = entrada.read()

# Dividir pelos blocos de resumo
blocos = conteudo.split("--------------------------------------------------")

# Filtrar só os que têm a tag ✅
resumos_uteis = [bloco.strip() for bloco in blocos if "✅ Útil técnico" in bloco]

# Concatenar tudo num único texto
texto_final = "\n\n".join(resumos_uteis)

# Salvar em arquivo de saída
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
    saida.write(texto_final)

print(f"Resumo final salvo em: {ARQUIVO_SAIDA}")
