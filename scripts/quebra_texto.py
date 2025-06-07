# scripts/quebra_texto.py (versão corrigida e mais simples)
import os
from pathlib import Path

# Você pode ajustar este valor se quiser blocos maiores ou menores.
TAMANHO_BLOCO = 5000

def fatiar_texto(input_filepath, output_dir):
    """
    Lê um arquivo de texto grande e o fatia em múltiplos arquivos menores (blocos)
    de tamanho fixo.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            texto_completo = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo de entrada: {e}")
        return

    if not texto_completo.strip():
        print("Aviso: O arquivo de texto de entrada está vazio ou contém apenas espaços.")
        return

    contador_blocos = 0
    for i in range(0, len(texto_completo), TAMANHO_BLOCO):
        contador_blocos += 1
        bloco_conteudo = texto_completo[i : i + TAMANHO_BLOCO]
        nome_bloco = f"bloco_{contador_blocos:03d}.txt" # Ex: bloco_001.txt
        caminho_bloco = Path(output_dir) / nome_bloco

        with open(caminho_bloco, 'w', encoding='utf-8') as f_bloco:
            f_bloco.write(bloco_conteudo)

    print(f"Texto fatiado em {contador_blocos} blocos no diretório '{output_dir}'.")


if __name__ == '__main__':
    # Bloco para permitir a execução do script diretamente pelo terminal para testes
    import sys
    if len(sys.argv) == 3:
        fatiar_texto(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python scripts/quebra_texto.py <arquivo_de_entrada> <diretorio_de_saida>")