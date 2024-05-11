import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
import json

st.title("Imersão IA ALURA")
st.subheader("Projeto localizador de respostas em vídeos do YouTube.")

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
        #transcript_text = '\n'.join([entry['text'] for entry in transcript])
        #return transcript_text

        # Format the transcript into a readable format
        formatted_transcript = '\n'.join([f"{x['start']}: {x['text']}; \n" for x in transcript])
        return formatted_transcript        
        
    except Exception as e:
        return str(e)

#trunca o texto para um número máximo de caracteres
def truncate_text(text, max_length=100):
    """ Trunca o texto para um número máximo de caracteres. """
    return text if len(text) <= max_length else text[:max_length] + '...'

# def link_time_youtube(video_id, start):
#     start_time = int(float(start))  
#     hours, remainder = divmod(start_time, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     time_stamp = f"{hours:02}:{minutes:02}:{seconds:02}"
#     video_link = f"https://www.youtube.com/watch?v={video_id}&t={start_time}s"
#     return f"<a href='{video_link}' target='_blank'>{time_stamp}</a>"

def create_video_url(video_id, start_time):
    # Conversão de start_time para int após converter para float para lidar com valores como '13.639'
    start_time_seconds = int(float(start_time))
    # Criação de uma URL que inclui o parâmetro de tempo
    return f"https://www.youtube.com/watch?v={video_id}&t={start_time_seconds}s"

#set o modelo de generative AI
GOOGLE_API_KEY = st.sidebar.text_input("Digite sua chave do Gemini:", type="password")
btn_set_model = st.sidebar.button("Set chave Gemini")

if btn_set_model:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name = 'gemini-1.0-pro')
    
    #set o modelo de chat
    st.session_state.chat = model.start_chat(history=[])    
    st.sidebar.success("Modelo configurado com sucesso.")


#carrega o link do video do youtube
url_youtube = st.text_input("Digite a URL do vídeo do youtube:")
st.caption("Exemplo de URL: https://www.youtube.com/watch?v=ZBcvHmuyDKI&list=PLqyYnji54FQZOjJjTO0fzhiKdaEzVmItb&index=4&t=359s")
btn_youtube = st.button("Recupera transcrição")

if 'url_youtube' in st.session_state:
    vd_principal = st.video(st.session_state.url_youtube)

if 'transcript' in st.session_state:
    txt_transcricao = st.write(truncate_text(st.session_state.transcript, 250))

if btn_youtube:
    if url_youtube:
        st.session_state.url_youtube = url_youtube
        vd_principal = st.video(st.session_state.url_youtube)

        # Replace 'your_video_id' with the actual YouTube video ID
        video_id = get_youtube_video_id(url_youtube)
        st.session_state.video_id = video_id
        
        with st.spinner('Carregando dados...'):        
            # Armazenando a transcrição no session state
            st.session_state.transcript = get_transcript(video_id)
        
        txt_transcricao = st.write(truncate_text(st.session_state.transcript, 250))

prompt = st.text_input("Digite sua pergunta sobre o vídeo:")
st.caption("Exemplo de pergunta: Quando fala sobre o princípio da coerência?")
btn_gemini = st.button("Enviar pergunta")

if btn_gemini:
    if 'transcript' in st.session_state:

        prompt_text = "responda a seguinte pergunta baseada na transcrição do vídeo."

        json_instruction = ("Responda utilizando o formato JSON, onde 'time' é o tempo de início "
                            "do trecho relevante do vídeo, e 'texto' é sua resposta. Exemplo de resposta: "
                            '{"time": "120", "texto": "Aqui vai a resposta detalhada."}')

        # Construir o prompt final incluindo a transcrição
        prompt_final = f"{prompt_text} {prompt} Considere a transcrição do vídeo após a marcação $$$. " \
                    f"A transcrição segue o padrão: 'tempo de início: texto; '. {json_instruction} $$$ " \
                    f"{st.session_state.transcript}"

        # prompt_final = ('Considere a transcrição do vídeo após a marcação $$$. '
        #     'A transcrição segue o padrão: "tempo de início: texto; ". '
        #     'Responde a pergunta e traga o "tempo de início" '
        #     f'em formato json: "time": "tempo de início", "texto": "resposta". '
        #     f'do principal texto que se baseou a resposta:' + prompt + '$$$ ' + st.session_state.transcript)
        
        response = st.session_state.chat.send_message(prompt_final)   
        st.write(response.text)
        
        try:
            response_data = json.loads(response.text)
            start_time = response_data["time"]
            resposta_texto = response_data["texto"]
            
            video_url = create_video_url(st.session_state.video_id, start_time)
            st.markdown(video_url, unsafe_allow_html=True)                     
            vd_auxiliar = st.video(video_url, start_time=int(float(start_time))) 

            # Criando a tabela em Streamlit
            # st.write("Resposta Transcrita com Links para o Vídeo:")
            # st.table({
            #     "Link": [video_link_html],
            #     "Texto": [resposta_texto]
            # })
        except json.JSONDecodeError:
            st.error("Falha ao decodificar a resposta JSON.")
    else:
        st.error("Nenhuma transcrição disponível. Por favor, recupere a transcrição primeiro.")