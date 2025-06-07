# scripts/filtro_inicial.py
import re

def limpar_transcricao(input_filepath, output_filepath):
    """
    Remove ruídos (repetições de letras/palavras, interjeições),
    normaliza espaços e salva o texto limpo.
    Mantém os marcadores de fonte .
    """
    with open(input_filepath, "r", encoding="utf-8") as f:
        texto = f.read()

    # Remove repetições de letras (tipo "ééééé", "aaaaa")
    texto = re.sub(r'(.)\1{2,}', r'\1', texto)

    # Remove interjeições comuns (melhoradas para serem mais robustas)
    interjeicoes = [
        r'\bné\b', r'\btá\b', r'\baham\b', r'\bentão\b', r'\bbeleza\b',
        r'\bé+\b', r'\bsei lá\b', r'\bau\b', r'\bhum\b', r'\btipo\b', r'\bmano\b',
        r'\bai\b', r'\boh\b', r'\bpessoal\b', r'\bcerto\b', r'\bok\b', r'\bopa\b',
        r'\bpode falar\b', r'\bnão é\b', r'\bné não\b'
    ]
    for i in interjeicoes:
        # Use uma função de substituição para preservar maiúsculas/minúsculas da primeira letra,
        # ou simplesmente remover. Para interjeições, a remoção simples é geralmente melhor.
        texto = re.sub(i, '', texto, flags=re.IGNORECASE)

    # Remove repetições de palavras idênticas seguidas (ex: "é é é")
    texto = re.sub(r'\b(\w+)( \1\b)+', r'\1', texto)

    # Corrige múltiplos espaços e limpa linhas
    texto = re.sub(r'\s+', ' ', texto).strip() # Multiplos espaços para um só
    texto = re.sub(r'(\[\s*source:\s*\d+\s*\])\s*', r'\1 ', texto) # Garante espaço após source
    texto = re.sub(r'\]\s*(\S)', r'] \1', texto) # Garante espaço após colchete de source

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(texto)

if __name__ == "__main__":
    # Este bloco só será executado se o script for chamado diretamente
    # Para o pipeline, main.py o chamará como uma função.
    # Exemplo de uso direto: python scripts/filtro_inicial.py docs/transcricao_aula_bruta.txt docs/transcricao_aula_limpa.txt
    import sys
    if len(sys.argv) == 3:
        limpar_transcricao(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python scripts/filtro_inicial.py <arquivo_entrada_bruta> <arquivo_saida_limpa>")