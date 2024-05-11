# Localizador de Respostas em Vídeos do YouTube

## Descrição

Este projeto utiliza o Google Gemini para localizar respostas específicas em vídeos do YouTube. Dado um link de vídeo do YouTube, o sistema:

1. **Recupera a transcrição do vídeo.**
2. **Permite que o usuário faça perguntas sobre o conteúdo do vídeo.**
3. **Utiliza o Gemini para analisar a transcrição e identificar o momento exato no vídeo onde a resposta à pergunta é dada.**
4. **Retorna o timestamp (tempo) e o trecho da transcrição que contém a resposta.**
5. **Fornece um link para o momento exato no vídeo do YouTube.**

## Motivação

A localização de informações específicas em vídeos pode ser uma tarefa tediosa e demorada. Este projeto visa a facilitar esse processo, permitindo que os usuários encontrem rapidamente as respostas que procuram sem precisar assistir ao vídeo inteiro.

## Como Usar

1. **Acesse a aplicação:** [[link para a aplicação Streamlit](https://gemini-youtube-alura.streamlit.app/)]
2. **Insira sua chave de API do Gemini:** Obtenha sua chave de API do Google Gemini e insira-a no campo indicado.
3. **Cole o link do vídeo do YouTube no campo "Digite a URL do vídeo do YouTube".**
4. **Clique em "Recuperar transcrição".**
5. **Digite sua pergunta sobre o vídeo no campo "Digite sua pergunta sobre o vídeo".**
6. **Clique em "Enviar pergunta".**
7. **O sistema retornará o timestamp, o trecho da transcrição e um link para o momento exato no vídeo onde a resposta é dada.**

## Tecnologias utilizadas

1. **Google Gemini**
2. **Streamlit**
3. **Python**

## Observações

1. **O sistema foi testado apenas com vídeos pequenos. Em vídeos de maior duração, foram detectadas alucinações.**
2. **O sistema é capaz de recuperar transcrições apenas em português.**

## Autor
Thiago Medeiros Barros
<thiago.medeiros@ifrn.edu.br>

## Exemplo

[[link para vídeo executando a aplicação](https://www.youtube.com/watch?v=_vyid4fVL5w)]