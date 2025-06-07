# scripts/filtro_inicial.py (Versão Corrigida e Segura)
import re

def limpar_transcricao(input_filepath, output_filepath):
    """
    Remove ruídos (repetições de letras/palavras, interjeições comuns com regex),
    normaliza espaços e salva o texto limpo.
    Mantém os marcadores de fonte.
    """
    with open(input_filepath, "r", encoding="utf-8") as f:
        texto = f.read()

    # Remove repetições de letras (ex: "ééééé", "aaaaa")
    texto = re.sub(r'(.)\1{2,}', r'\1', texto)

    # Lista de interjeições e palavras de preenchimento a serem removidas
    # Esta lista pode ser aumentada se você notar outras palavras comuns
    interjeicoes = [
        r'\b(né|tá|aham|então|beleza|tipo|mano|daí|é…)\b',
        r'\b(uh|um|ah|eh|hm)\b',
        r'\b(certo|ok)\b'
    ]
    for i in interjeicoes:
        texto = re.sub(i, '', texto, flags=re.IGNORECASE)

    # Remove repetições de palavras idênticas seguidas (ex: "é é é")
    texto = re.sub(r'\b(\w+)( \1\b)+', r'\1', texto, flags=re.IGNORECASE)

    # Corrige múltiplos espaços e limpa linhas
    texto = re.sub(r'\s+', ' ', texto).strip()
    texto = re.sub(r'(\[\s*source:\s*\d+\s*\])\s*', r'\1 ', texto) # Garante espaço após source
    texto = re.sub(r'\]\s*(\S)', r'] \1', texto) # Garante espaço após colchete de source

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(texto)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        limpar_transcricao(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python scripts/filtro_inicial.py <arquivo_entrada_bruta> <arquivo_saida_limpa>")