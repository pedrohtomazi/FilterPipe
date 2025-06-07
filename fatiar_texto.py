import os
import sys

def fatiar_texto(texto, palavras_por_bloco=800):
    palavras = texto.split()
    blocos = [palavras[i:i + palavras_por_bloco] for i in range(0, len(palavras), palavras_por_bloco)]
    return [' '.join(bloco) for bloco in blocos]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fatiar_texto.py limpa.txt")
        sys.exit(1)

    caminho_entrada = sys.argv[1]

    with open(caminho_entrada, "r", encoding="utf-16") as f:
        texto = f.read()

    blocos = fatiar_texto(texto, palavras_por_bloco=800)

    pasta_saida = "blocos"
    os.makedirs(pasta_saida, exist_ok=True)

    for i, bloco in enumerate(blocos):
        with open(os.path.join(pasta_saida, f"bloco_{i+1:02}.txt"), "w", encoding="utf-8") as f:
            f.write(bloco)

    print(f"{len(blocos)} blocos salvos na pasta '{pasta_saida}'")