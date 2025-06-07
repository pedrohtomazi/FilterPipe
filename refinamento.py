import subprocess
import re
import sys
import io
import os
import time

# --- Configurações ---
ARQUIVO_ENTRADA = "resumo_final.md"
ARQUIVO_SAIDA = "resumo_final_revisado.md"
MODELO_OLLAMA = "mixtral" # Mude aqui se quiser usar outro modelo (ex: "llama3")

# Força a saída do terminal como UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verificar_ollama():
    """Verifica se o comando 'ollama' está disponível no sistema."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Ollama encontrado no sistema.")
        return True
    except FileNotFoundError:
        print("❌ ERRO: O comando 'ollama' não foi encontrado. Por favor, instale o Ollama e adicione-o ao seu PATH.", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao verificar o Ollama: {e.stderr.decode('utf-8').strip()}", file=sys.stderr)
        return False

def carregar_resumo():
    """Carrega o conteúdo do arquivo de resumo."""
    print(f"📄 Carregando conteúdo de '{ARQUIVO_ENTRADA}'...")
    try:
        with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo '{ARQUIVO_ENTRADA}' não foi encontrado. Certifique-se de que ele está no mesmo diretório do script.", file=sys.stderr)
        sys.exit(1) # Sai do script se o arquivo não for encontrado

def separar_blocos(texto):
    """Separa o texto principal em blocos baseados nos títulos de resumo."""
    print("✂️ Separando o conteúdo em blocos para análise...")
    # O re.split inclui o delimitador no resultado quando o delimitador está entre parênteses
    blocos = re.split(r"(### 📌 Resumo_\d+ - ✅ Útil técnico)", texto)
    
    blocos_processados = []
    # O primeiro elemento de blocos pode ser texto antes do primeiro título, ou vazio.
    # Queremos emparelhar o título com o conteúdo que o segue.
    # Iteramos de 1 em 2 para pegar o título e seu conteúdo.
    for i in range(1, len(blocos), 2):
        if i + 1 < len(blocos): # Garante que há conteúdo após o título
            titulo = blocos[i].strip()
            conteudo = blocos[i + 1].strip()
            blocos_processados.append((titulo, conteudo))
    
    if not blocos_processados:
        print("⚠️ Atenção: Nenhum bloco de resumo técnico encontrado no arquivo. Verifique o formato dos títulos '### 📌 Resumo_X - ✅ Útil técnico'.")
    else:
        print(f"👍 {len(blocos_processados)} blocos encontrados para análise.")
    return blocos_processados

def rodar_ollama(trecho):
    """
    Chama o modelo Ollama para revisar um trecho de texto,
    adicionando feedback visual durante o processo.
    """
    prompt = f"""Você é um assistente técnico. Revise o seguinte conteúdo e aponte **apenas os erros técnicos ou explicações confusas** (ex: erros sobre portas lógicas, sensores, circuitos), e reescreva a parte corrigida em **formato markdown**, mantendo clareza e concisão. Ignore erros gramaticais irrelevantes.

Texto a revisar:
\"\"\"
{trecho}
\"\"\"

Retorne somente:
1. Uma explicação sobre o erro, se houver.
2. O trecho reescrito corrigido, com marcação markdown.
"""
    
    print(f"⏳ Chamando {MODELO_OLLAMA} (isso pode levar alguns segundos)...", end='', flush=True)
    processo = subprocess.Popen(
        ["ollama", "run", MODELO_OLLAMA],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Escreve o prompt para a entrada padrão do processo ollama
    processo.stdin.write(prompt.encode('utf-8'))
    processo.stdin.close() # Fecha a entrada para sinalizar que terminamos de enviar dados

    saida_bruta = []
    erros_brutos = []

    # Lê a saída em tempo real e imprime pontos de progresso
    while True:
        stdout_line = processo.stdout.readline()
        stderr_line = processo.stderr.readline()

        if stdout_line:
            saida_bruta.append(stdout_line)
            # print(".", end='', flush=True) # Feedback de progresso
            # Remover o ponto em tempo real para não poluir o terminal,
            # o feedback "Rodando modelo..." já é suficiente.
        if stderr_line:
            erros_brutos.append(stderr_line)
            # print("e", end='', flush=True) # Feedback de erro, se houver

        if not stdout_line and not stderr_line and processo.poll() is not None:
            break
        # Pequena pausa para evitar consumo excessivo de CPU em loop apertado
        time.sleep(0.05)

    saida_completa = b"".join(saida_bruta).decode('utf-8').strip()
    erros_completo = b"".join(erros_brutos).decode('utf-8').strip()

    # Verifica o código de retorno final do processo
    returncode = processo.wait()

    if returncode != 0:
        print(f"\n❌ ERRO do Ollama (código {returncode}):")
        print(f"Detalhes do erro: {erros_completo}", file=sys.stderr)
        return f"🚨 ERRO: Não foi possível obter resposta do modelo {MODELO_OLLAMA}. Verifique os logs acima."
    
    print(" ✅ Concluído!")
    return saida_completa

def main():
    print("🚀 Iniciando o script de revisão técnica com Ollama!\n")
    
    if not verificar_ollama():
        sys.exit(1) # Sai se o Ollama não estiver disponível

    texto_original = carregar_resumo()
    blocos = separar_blocos(texto_original)

    if not blocos:
        print("Nenhum bloco válido para processar. Encerrando.")
        return

    conteudo_revisado = []

    # Adiciona qualquer texto antes do primeiro bloco processado
    # Isso é importante para manter o início do arquivo se ele não começar com um título de bloco
    primeiro_titulo = blocos[0][0] if blocos else None
    if primeiro_titulo:
        match = re.search(r"(### 📌 Resumo_\d+ - ✅ Útil técnico)", texto_original)
        if match:
            texto_antes_primeiro_bloco = texto_original[:match.start()]
            conteudo_revisado.append(texto_antes_primeiro_bloco.strip())


    for i, (titulo, conteudo) in enumerate(blocos, 1):
        print(f"\n--- Bloco {i}/{len(blocos)} ---")
        print(f"🔍 Analisando: {titulo}")
        
        # Adiciona o título e o conteúdo original ao arquivo revisado
        conteudo_revisado.append(f"\n{titulo}\n\n{conteudo}\n")

        resposta_ollama = rodar_ollama(conteudo)
        
        print(f"\n✅ Saída do modelo para '{titulo}':\n")
        print(f"{resposta_ollama}\n")
        
        # Adiciona a resposta do Ollama ao conteúdo revisado para o novo arquivo
        conteudo_revisado.append(f"\n\n### Sugestão de Revisão do Ollama para '{titulo}':\n{resposta_ollama}\n")
        conteudo_revisado.append("-" * 80 + "\n") # Separador para o arquivo de saída

    print("\n\n🎉 Processamento de todos os blocos concluído!")
    
    # Salva o conteúdo revisado em um novo arquivo
    try:
        with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(conteudo_revisado))
        print(f"💾 As revisões foram salvas em '{ARQUIVO_SAIDA}'")
    except IOError as e:
        print(f"❌ ERRO ao salvar o arquivo '{ARQUIVO_SAIDA}': {e}", file=sys.stderr)

    print("\n--- Fim do script ---")

if __name__ == "__main__":
    main()