# painel.py (Versão corrigida para orquestrar o pipeline de blocos)
import streamlit as st
import os
import sys
import shutil
from pathlib import Path

# --- Adiciona o diretório raiz ao path para encontrar a pasta 'scripts' ---
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# --- Importação de todas as funções necessárias do pipeline ---
from scripts.filtro_inicial import limpar_transcricao
from scripts.quebra_texto import fatiar_texto
from scripts.extrair_info_ppxt import extrair_texto_de_pptx
# Importa o script de alinhamento por palavras-chave (a versão corrigida)
# from scripts.alinhar_conteudo import alinhar_blocos_com_slides # Removido para simplificar, se necessário
# Importa o script de resumo por extração (a versão corrigida)
from scripts.class_resm import resumir_blocos
# Importa o gerador de markdown (a versão corrigida)
from scripts.md_gen import gerar_markdown_final, refinar_markdown_com_ollama

# --- Função para criar e limpar os diretórios de trabalho ---
def setup_directories(dirs_to_create):
    """Cria e/ou limpa uma lista de diretórios."""
    for d in dirs_to_create:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

# --- 1. Título e Configuração da Página ---
st.set_page_config(layout="wide")
st.title("FilterPipe: Gerador de Resumos de Aulas 📘")

# --- 2. Elementos da Interface ---
st.subheader("1. Carregue os arquivos da aula")

col1, col2 = st.columns(2)
with col1:
    uploaded_pptx = st.file_uploader(
        "Selecione os Slides (.pptx)",
        type="pptx"
    )
with col2:
    uploaded_txt = st.file_uploader(
        "Selecione a Transcrição (.txt)",
        type="txt"
    )

st.divider()
processar_btn = st.button("Gerar Resumo via Pipeline de Blocos", type="primary", use_container_width=True)

# --- 4. Lógica de integração do pipeline ---
if processar_btn:
    if not (uploaded_pptx and uploaded_txt):
        st.error("Por favor, carregue o arquivo de slides (.pptx) e o de transcrição (.txt).")
        st.stop()

    # --- PREPARAÇÃO E LIMPEZA ---
    # Nomes dos diretórios
    DOCS_DIR = "docs_temp"
    BLOCO_DIR = "blocos"
    RESUMO_DIR = "resumos"
    MDS_DIR = "mds"
    
    st.info("Preparando diretórios de trabalho...")
    setup_directories([DOCS_DIR, BLOCO_DIR, RESUMO_DIR, MDS_DIR])
    
    # Salva e normaliza os arquivos carregados
    texto_bruto = uploaded_txt.getvalue().decode('utf-8', errors='replace').replace('\x00', '')
    bruto_path = Path(DOCS_DIR) / "transcricao_bruta_temp.txt"
    with open(bruto_path, "w", encoding="utf-8") as f:
        f.write(texto_bruto)

    pptx_path = Path(DOCS_DIR) / "slides_temp.pptx"
    with open(pptx_path, "wb") as f:
        f.write(uploaded_pptx.getbuffer())
    st.success("Arquivos de entrada salvos.")

    # --- EXECUÇÃO DO PIPELINE DE BLOCOS ---
    with st.spinner("Etapa 1/5: Extraindo texto dos slides..."):
        slides_texto_path = Path(DOCS_DIR) / "slides_extraidos.txt"
        extrair_texto_de_pptx(str(pptx_path), str(slides_texto_path))
        st.success("Texto dos slides extraído!")

    with st.spinner("Etapa 2/5: Realizando limpeza inicial da transcrição..."):
        limpa_path = Path(DOCS_DIR) / "transcricao_limpa_temp.txt"
        limpar_transcricao(str(bruto_path), str(limpa_path))
        st.success("Limpeza inicial concluída!")

    with st.spinner("Etapa 3/5: Fatiando a transcrição em blocos..."):
        fatiar_texto(str(limpa_path), BLOCO_DIR)
        st.success("Transcrição fatiada em blocos!")

    with st.spinner("Etapa 4/5: Extraindo conteúdo técnico de cada bloco (pode levar minutos)..."):
        # A função resumir_blocos agora extrai o conteúdo técnico de cada bloco no BLOCO_DIR
        resumir_blocos(BLOCO_DIR, RESUMO_DIR)
        st.success("Extração de conteúdo dos blocos concluída!")
        
    with st.spinner("Etapa 5/5: Montando e refinando o Markdown final..."):
        final_md_bruto_path = Path(MDS_DIR) / "resumo_final_bruto.md"
        final_md_revisado_path = Path(MDS_DIR) / "resumo_final_revisado.md"
        
        # A função gerar_markdown_final agora filtra os resumos vazios ("SEM_INFO_UTIL")
        gerar_markdown_final(RESUMO_DIR, MDS_DIR, final_md_bruto_path.name)
        refinar_markdown_com_ollama(str(final_md_bruto_path), str(final_md_revisado_path))
        st.success("Resumo final gerado e refinado!")

    # --- EXIBIÇÃO DO RESULTADO ---
    st.balloons()
    st.header("🎉 Resumo Final Gerado!")
    
    with open(final_md_revisado_path, "r", encoding="utf-8") as f:
        conteudo_final_md = f.read()
    
    st.markdown(conteudo_final_md)