import os

# Pasta com os resumos
PASTA = "resumos"
SAIDA = "resumos_classificados.txt"

# Palavras-chave pra tentativa de classificação
PALAVRAS_TECNICAS = ["tabela verdade", "porta lógica", "and", "or", "xor", "circuito", "sensor", "binário", "arduino"]
PALAVRAS_RUÍDO = ["moza", "trânsito", "conversas", "boneco", "pet", "telefone"]

def classificar(texto):
    texto_lower = texto.lower()

    if any(p in texto_lower for p in PALAVRAS_RUÍDO):
        return "❌ Ruído"
    elif any(p in texto_lower for p in PALAVRAS_TECNICAS):
        return "✅ Útil técnico"
    else:
        return "⚠️ Parcial"

arquivos = sorted([f for f in os.listdir(PASTA) if f.endswith(".txt")])

with open(SAIDA, "w", encoding="utf-8") as saida:
    for nome in arquivos:
        caminho = os.path.join(PASTA, nome)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            categoria = classificar(conteudo)
            saida.write(f"🔹 {nome.replace('.txt','').title()} - {categoria}\n\n")
            saida.write(conteudo + "\n\n")
            saida.write("—" * 50 + "\n\n")