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

1. **O sistema foi testado apenas com vídeos pequenos. Em vídeos grandes foi detectado alucionações**
2. **O sistema recupera apenas transcrição em português**

## Autor
Thiago Medeiros Barros
<thiago.medeiros@ifrn.edu.br>

## Exemplo

**Pergunta:** Quando o vídeo fala sobre o princípio da coerência?

**Resposta:**
```json
{
  "time": "468.639",
  "texto": "O princípio da coerência é que toda informação irrelevante para o aprendizado para alcançar aquele objetivo de aprendizagem ele deve ser excluído menos é mais certo então uma música ao fundo alguma figura que não tá acrescentando para o objetivo daquela paisagem tem que ser removido"
}
https://www.youtube.com/watch?v=ZbcrHmyxDkI&t=468s