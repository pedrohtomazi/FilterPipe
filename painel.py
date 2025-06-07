# painel.py
import streamlit as st
import os
import sys
import shutil
from pathlib import Path
import time

# --- Adiciona o diretório raiz ao path para encontrar a pasta 'scripts' ---
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# --- Importação das suas funções do pipeline ---
from scripts.filtro_inicial import limpar_transcricao
from scripts.quebra_texto import fatiar_texto
from scripts.class_resm import resumir_blocos
from scripts.md_gen import gerar_markdown_final, refinar_markdown_com_ollama

# --- Função para criar e limpar os diretórios de trabalho ---
def setup_directories(dirs_to_create):
    """Cria e limpa uma lista de diretórios."""
    for d in dirs_to_create:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

# --- 1. Título da Página ---
st.set_page_config(layout="wide")
st.title("FilterPipe: Gerador de Resumos de Aulas 📘")

# --- 2. Elementos da Interface ---

st.subheader("1. Carregue a transcrição da aula")
uploaded_file = st.file_uploader(
    "Selecione um arquivo de texto (.txt)",
    type="txt"
)

st.subheader("2. Forneça o contexto")
tema_central = st.text_input(
    "Qual o tema central da aula?",
    placeholder="Ex: Introdução ao Git e Versionamento de Código"
)

palavras_chave_str = st.text_area(
    "Informe as palavras-chave técnicas (separadas por vírgula)",
    placeholder="Ex: git, commit, branch, merge, repositório, clone"
)

# --- 3. Botão para iniciar o processo ---
st.divider() # Adiciona uma linha divisória
processar_btn = st.button("Gerar Resumo", type="primary", use_container_width=True)


# --- 4. Lógica de integração do pipeline ---
if processar_btn:
    # Validação inicial dos inputs
    if not (uploaded_file and tema_central and palavras_chave_str):
        st.error("Por favor, preencha todos os campos e carregue o arquivo antes de continuar.")
        st.stop() # Para a execução se algo estiver faltando

    # --- PREPARAÇÃO E LIMPEZA PROFUNDA DO ARQUIVO ---
    try:
        # Nomes dos diretórios de trabalho
        BLOCO_DIR = "blocos"
        RESUMO_DIR = "resumos"
        MDS_DIR = "mds"
        DOCS_DIR = "docs_temp"
        
        # Cria e limpa os diretórios de trabalho
        st.info("Preparando diretórios de trabalho...")
        setup_directories([BLOCO_DIR, RESUMO_DIR, MDS_DIR, DOCS_DIR])
        
        # Lê os bytes brutos do arquivo carregado
        raw_bytes = uploaded_file.getvalue()
        
        # Tenta decodificar como UTF-8. Se não for, tenta como Latin-1.
        try:
            texto_bruto = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            st.warning("Arquivo não é UTF-8. Tentando decodificação como Latin-1 (pode resolver problemas de acentuação).")
            texto_bruto = raw_bytes.decode('latin-1', errors='replace')

        # ETAPA CRÍTICA: Procura e remove caracteres nulos ('\x00')
        if '\x00' in texto_bruto:
            st.warning("Caracteres nulos ('null') foram detectados e removidos do arquivo de entrada.")
            texto_bruto_limpo = texto_bruto.replace('\x00', '')
        else:
            texto_bruto_limpo = texto_bruto
        
        # Salva o conteúdo 100% limpo para o pipeline usar
        bruto_path = Path(DOCS_DIR) / "transcricao_bruta_temp.txt"
        with open(bruto_path, "w", encoding="utf-8") as f:
            f.write(texto_bruto_limpo)
        st.success("Arquivo de entrada lido e normalizado com sucesso.")

    except Exception as e:
        st.error(f"Ocorreu um erro crítico ao ler ou preparar o arquivo: {e}")
        st.stop() # Para a execução se o arquivo não puder ser processado

    # --- EXECUÇÃO DO PIPELINE ---
    with st.spinner("Etapa 1/4: Realizando limpeza inicial da transcrição..."):
        limpa_path = Path(DOCS_DIR) / "transcricao_limpa_temp.txt"
        limpar_transcricao(str(bruto_path), str(limpa_path))
        st.success("Limpeza inicial concluída!")

    with st.spinner("Etapa 2/4: Fatiando o texto em blocos..."):
        fatiar_texto(str(limpa_path), BLOCO_DIR)
        st.success("Texto fatiado com sucesso!")

    with st.spinner("Etapa 3/4: Gerando e classificando resumos dos blocos (pode levar alguns minutos)..."):
        resumir_blocos(BLOCO_DIR, RESUMO_DIR)
        st.success("Resumos dos blocos gerados!")
        
    with st.spinner("Etapa 4/4: Montando e refinando o Markdown final..."):
        final_md_bruto_path = Path(MDS_DIR) / "resumo_final_bruto.md"
        final_md_revisado_path = Path(MDS_DIR) / "resumo_final_revisado.md"
        
        # NOTA: Idealmente, as funções 'gerar_markdown_final' e 'classificar_texto'
        # seriam refatoradas para aceitar as palavras-chave e temas da interface diretamente.
        # Por enquanto, elas usarão os valores fixos definidos dentro dos próprios scripts.
        gerar_markdown_final(RESUMO_DIR, MDS_DIR, final_md_bruto_path.name)
        refinar_markdown_com_ollama(str(final_md_bruto_path), str(final_md_revisado_path))
        st.success("Resumo final gerado e refinado com sucesso!")

    # --- EXIBIÇÃO DO RESULTADO ---
    st.balloons()
    st.header("🎉 Resumo Final Gerado!")
    
    # Lê o conteúdo do arquivo markdown final e exibe na tela
    with open(final_md_revisado_path, "r", encoding="utf-8") as f:
        conteudo_final_md = f.read()
    
    st.markdown(conteudo_final_md)