# main.py
import os
import shutil
from pathlib import Path

# Importar funções dos outros módulos
from scripts.filtro_inicial import limpar_transcricao
from scripts.quebra_texto import fatiar_texto
from scripts.class_resm import resumir_blocos, classificar_resumos
from scripts.md_gen import gerar_markdown_final, refinar_markdown_com_ollama

# --- Configurações Iniciais (poderiam vir de um config.py) ---
INPUT_BRUTO_FILE = "transcricao_aula_bruta.txt"
LIMPA_FILE = "transcricao_aula_limpa.txt"
BLOCO_DIR = "blocos"
RESUMO_DIR = "resumos"
MDS_DIR = "mds"
FINAL_MD_BRUTO = "resumo_final_bruto.md"
FINAL_MD_REVISADO = "resumo_final_revisado.md"

def setup_directories():
    """Cria e limpa diretórios de saída."""
    for d in [BLOCO_DIR, RESUMO_DIR, MDS_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d) # Limpa diretórios de execução anterior
        os.makedirs(d, exist_ok=True)
    os.makedirs("docs", exist_ok=True) # Garante que a pasta docs existe

def main():
    print("🚀 Iniciando o pipeline de geração de resumos de aula!")
    setup_directories()

    # Assumindo que a transcrição bruta está em docs/
    bruto_path = Path("docs") / INPUT_BRUTO_FILE
    if not bruto_path.exists():
        print(f"Erro: Arquivo de entrada '{bruto_path}' não encontrado. Por favor, coloque a transcrição bruta na pasta 'docs/'.")
        return

    # Etapa 1: Filtro Inicial (Limpeza)
    print("\n[1/4] Realizando limpeza inicial da transcrição...")
    limpa_path = Path("docs") / LIMPA_FILE
    limpar_transcricao(str(bruto_path), str(limpa_path))
    print(f"Limpeza concluída. Saída salva em: {limpa_path}")

    # Etapa 2: Quebra de Texto (Fatiar em blocos)
    print("\n[2/4] Fatiando o texto limpo em blocos menores...")
    fatiar_texto(str(limpa_path), BLOCO_DIR)
    print(f"Texto fatiado em blocos. Blocos salvos em: {BLOCO_DIR}")

    # Etapa 3: Resumir e Classificar Blocos
    print("\n[3/4] Gerando e classificando resumos dos blocos...")
    resumir_blocos(BLOCO_DIR, RESUMO_DIR) # Isso vai gerar resumos e classificá-los internamente
    print(f"Resumos gerados e classificados. Resumos salvos em: {RESUMO_DIR}")

    # Etapa 4: Geração e Refinamento do Markdown Final
    print("\n[4/4] Gerando o resumo final em Markdown e aplicando refinamento...")
    gerar_markdown_final(RESUMO_DIR, MDS_DIR, FINAL_MD_BRUTO)
    print(f"Resumo bruto em Markdown gerado: {Path(MDS_DIR) / FINAL_MD_BRUTO}")

    refinar_markdown_com_ollama(str(Path(MDS_DIR) / FINAL_MD_BRUTO), str(Path(MDS_DIR) / FINAL_MD_REVISADO))
    print(f"Refinamento concluído. Resumo final salvo em: {Path(MDS_DIR) / FINAL_MD_REVISADO}")

    print("\n✅ Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()