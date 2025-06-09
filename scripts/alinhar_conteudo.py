# scripts/alinhar_conteudo.py (Versão Corrigida com Alinhamento por Palavras-Chave)
import os
import shutil
import re
from pathlib import Path

# NOVO THRESHOLD: Um bloco será mantido se contiver pelo menos 3% (0.03) das
# palavras-chave únicas extraídas de TODOS os slides. Este valor pode ser ajustado.
KEYWORD_OVERLAP_THRESHOLD = 0.03

# Lista de palavras comuns em português a serem ignoradas na extração de keywords.
# Isso ajuda a focar nos termos técnicos.
STOP_WORDS = set([
    'a', 'o', 'e', 'ou', 'de', 'do', 'da', 'em', 'no', 'na', 'um', 'uma', 'com',
    'que', 'se', 'por', 'para', 'os', 'as', 'dos', 'das', 'ao', 'aos', 'à', 'às',
    'pelo', 'pela', 'ser', 'são', 'está', 'é', 'foi', 'mas', 'mais', 'como', 'aqui',
    'também', 'até', 'isso', 'isto', 'este', 'esta', 'ele', 'ela', 'nós', 'você',
    'tem', 'então', 'assim', 'muito', 'só', 'quando', 'pra', 'coisa', 'coisas'
])

def _extrair_keywords(texto):
    """Extrai palavras únicas e em minúsculas de um texto, removendo stop words e números."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    # Retorna um conjunto de palavras que não são stop words e não são apenas dígitos.
    return set(p for p in palavras if p not in STOP_WORDS and not p.isdigit())

def alinhar_blocos_com_slides(slides_texto_path, blocos_input_dir, blocos_output_dir):
    """
    Filtra blocos de transcrição com base na sobreposição de palavras-chave
    com o conteúdo dos slides.
    """
    os.makedirs(blocos_output_dir, exist_ok=True)
    try:
        with open(slides_texto_path, 'r', encoding='utf-8') as f:
            conteudo_slides = f.read()
    except FileNotFoundError:
        print(f"🚨 ERRO: Arquivo de slides não encontrado em '{slides_texto_path}'")
        return 0, 0

    # 1. Cria um vocabulário único de palavras-chave a partir de todos os slides.
    keywords_dos_slides = _extrair_keywords(conteudo_slides)
    
    if not keywords_dos_slides:
        print("🚨 AVISO: Nenhuma palavra-chave encontrada nos slides. O alinhamento pode falhar.")
        # Como fallback, se não houver keywords, copie todos os blocos para não gerar um resultado vazio.
        for nome_arquivo in sorted(os.listdir(blocos_input_dir)):
            shutil.copy(Path(blocos_input_dir) / nome_arquivo, Path(blocos_output_dir) / nome_arquivo)
        return len(os.listdir(blocos_input_dir)), 0

    total_keywords_slides = len(keywords_dos_slides)
    print(f"🔑 Encontradas {total_keywords_slides} palavras-chave únicas nos slides para o alinhamento.")
    
    # 2. Itera sobre cada bloco e calcula a sobreposição de palavras-chave.
    mantidos = 0
    descartados = 0
    print("\n🧩 Alinhando blocos de transcrição com keywords dos slides (método aprimorado)...")

    for nome_arquivo in sorted(os.listdir(blocos_input_dir)):
        caminho_bloco = Path(blocos_input_dir) / nome_arquivo
        with open(caminho_bloco, 'r', encoding='utf-8') as f:
            conteudo_bloco = f.read()

        keywords_do_bloco = _extrair_keywords(conteudo_bloco)
        
        # Calcula a interseção (palavras em comum)
        keywords_em_comum = keywords_dos_slides.intersection(keywords_do_bloco)
        
        score_sobreposicao = len(keywords_em_comum) / total_keywords_slides if total_keywords_slides > 0 else 0

        # 3. Filtra com base no novo threshold de sobreposição.
        if score_sobreposicao >= KEYWORD_OVERLAP_THRESHOLD:
            shutil.copy(caminho_bloco, Path(blocos_output_dir) / nome_arquivo)
            print(f"  -> ✅ Mantido: {nome_arquivo} (Sobreposição: {score_sobreposicao:.2%}, Palavras em comum: {len(keywords_em_comum)})")
            mantidos += 1
        else:
            print(f"  -> ❌ Descartado: {nome_arquivo} (Sobreposição: {score_sobreposicao:.2%})")
            descartados += 1

    if mantidos == 0:
        print("\n🚨 AVISO: Nenhum bloco atingiu o threshold. O resumo final pode ficar vazio.")
        print("💡 SUGESTÃO: Tente diminuir o valor de 'KEYWORD_OVERLAP_THRESHOLD' no script 'alinhar_conteudo.py'.")


    return mantidos, descartados