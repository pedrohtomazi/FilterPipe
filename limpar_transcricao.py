import re
import sys

def limpar(texto):
    # Remove repetições de letras (tipo "ééééé", "aaaaa")
    texto = re.sub(r'(.)\1{2,}', r'\1', texto)

    # Remove interjeições comuns
    interjeicoes = [
        r'\bné\b', r'\btá\b', r'\baham\b', r'\bentão\b', r'\bbeleza\b',
        r'\bé+\b', r'\bsei lá\b', r'\bau\b', r'\bhum\b', r'\btipo\b', r'\bmano\b'
    ]
    for i in interjeicoes:
        texto = re.sub(i, '', texto, flags=re.IGNORECASE)

    # Remove repetições de palavras idênticas seguidas (ex: "é é é")
    texto = re.sub(r'\b(\w+)( \1\b)+', r'\1', texto)

    # Corrige múltiplos espaços
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python limpar_transcricao.py entrada.txt > limpa.txt")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        conteudo = f.read()

    resultado = limpar(conteudo)
    print(resultado)
