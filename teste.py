import streamlit as st
import subprocess
import os
import shutil

st.title('transcription.app')

extensions = ['json', 'srt', 'txt', 'vtt', 'tsv']

# Upload do arquivo de áudio
audio_file = st.file_uploader('Carregar Audio', type=['wav', 'mp3', 'mp4a'])

# Botão para iniciar a transcrição
if st.button('Transcrever Áudio') and audio_file:
    for ext in extensions:
        filename = f"arquivos/audioteste.{ext}"  # Caminho para a pasta "arquivos"
        if os.path.exists(filename):
            os.remove(filename)

    # Salvar o arquivo carregado no disco com o nome desejado
    audio_path = "arquivos/audioteste.mp3"
    with open(audio_path, "wb") as f:  # Caminho para a pasta "arquivos"
        f.write(audio_file.getbuffer())

    # Comando a ser executado
    command = ["whisper", audio_path, "--model", "medium", "--language", "pt"]  # Caminho para a pasta "arquivos"

    # Executando o comando
    subprocess.run(command)

    # Mover os arquivos transcritos para a pasta "arquivos"
    for ext in extensions:
        filename = f"audioteste.{ext}"
        if os.path.exists(filename):
            shutil.move(filename, f"arquivos/{filename}")

    # Apresenta links de download e visualização para cada arquivo gerado
    for ext in extensions:
        filename = f"arquivos/audioteste.{ext}"  # Caminho para a pasta "arquivos"
        if os.path.exists(filename):
            st.markdown(f"### Arquivo {ext.upper()}:")
            st.markdown(f"**Baixar {ext.upper()}:**")
            st.download_button(label=f"Download {ext.upper()}", data=open(filename, 'rb'), file_name=filename, mime=None, key=None, help=None, on_click=None)
            st.markdown(f"**Visualizar {ext.upper()}:**")
            with open(filename, 'r', encoding='utf-8') as file:
                st.text_area(f"Conteúdo do arquivo {ext.upper()}:", value=file.read(), height=200)
