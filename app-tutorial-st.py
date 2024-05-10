import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.title("Imersão IA ALURA")
st.subheader("Projeto criação automatizada de tutorial")

#recupera a ID do video do youtube
def get_youtube_video_id(url):
    # This pattern covers various forms of YouTube URLs
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return "Invalid URL or video ID not found."

#recuperar a transcrição de um vídeo do youtube dado um ID
def get_transcript(video_id):
    try:
        # Fetching the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        # Converting the transcript into a readable format
        transcript_text = '\n'.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        return str(e)

#trunca o texto para um número máximo de caracteres
def truncate_text(text, max_length=100):
    """ Trunca o texto para um número máximo de caracteres. """
    return text if len(text) <= max_length else text[:max_length] + '...'

#set o modelo de generative AI
GOOGLE_API_KEY = st.sidebar.text_input("Digite sua chave de API do Google:")
btn_set_model = st.sidebar.button("Setar modelo")

if btn_set_model:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name = 'gemini-1.0-pro')
    
    #set o modelo de chat
    st.session_state.chat = model.start_chat(history=[])    


#carrega o link do video do youtube
url_youtube = st.text_input("Digite a URL do vídeo do youtube:")
btn_youtube = st.button("Recupera transcrição")

if 'url_youtube' in st.session_state:
    st.video(st.session_state.url_youtube)

if 'transcript' in st.session_state:
    st.write(truncate_text(st.session_state.transcript, 250))

if btn_youtube:
    if url_youtube:
        st.session_state.url_youtube = url_youtube
        st.video(st.session_state.url_youtube)

        # Replace 'your_video_id' with the actual YouTube video ID
        video_id = get_youtube_video_id(url_youtube)
        
        with st.spinner('Carregando dados...'):        
            # Armazenando a transcrição no session state
            st.session_state.transcript = get_transcript(video_id)
        
        st.write(truncate_text(st.session_state.transcript, 250))

prompt = st.text_input("Digite sua pergunta sobre o vídeo:")
btn_gemini = st.button("Enviar pergunta")

if btn_gemini:
    if 'transcript' in st.session_state:
        prompt_final = '''Considere a transcrição do vídeo após a marcação $$$ e responde a pergunta:''' + prompt + '$$$ ' + st.session_state.transcript
        response = st.session_state.chat.send_message(prompt_final)
        st.write(response.text)
    else:
        st.error("Nenhuma transcrição disponível. Por favor, recupere a transcrição primeiro.")


