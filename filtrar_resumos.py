ARQUIVO_ENTRADA = "resumos_classificados.txt"
ARQUIVO_SAIDA = "resumo_final.txt"

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as entrada:
    conteudo = entrada.read()

# Divide o conteúdo em blocos por linha separadora
blocos = conteudo.split("——————————————————————————————————————————————————")

# Filtra só os blocos com "✅ Útil técnico"
blocos_uteis = [bloco.strip() for bloco in blocos if "✅ Útil técnico" in bloco]

# Junta todos os blocos em um único texto
resumo_final = "\n\n".join(blocos_uteis)

# Salva no arquivo de saída
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
    saida.write(resumo_final)

print(f"✅ Resumo final salvo em: {ARQUIVO_SAIDA}")