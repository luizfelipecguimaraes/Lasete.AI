import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Lasete AI",
    page_icon="icon.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "Lasete AI", um assistente de IA especialista em cibersegurança e tecnologias emergentes. Sua missão é ajudar os ligantes da Liga Acadêmica de Segurança e Tecnologias Emergentes (Lasete) da UNDB com dúvidas sobre os temas principais da liga de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco**: Responda apenas a perguntas relacionadas a cibersegurança, pilares da segurança da informação, meios de ataques online, criptografias, visão computacional, inteligência artificial, Iot, Blockchain, e demais assuntos que estejam corelacionados a liga acadêmica. Se o usuário perguntar sobre outros assuntos, responda educadamente que seu foco é exclusivamente em auxiliar com assuntos relacionados à Lasete.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de prática**: Forneça um ou mais exemplos de aplicação do assunto questionado, sendo bem comentado para explicar as partes importantes.
    * **Detalhes**: Após os exemplos, descreva em detalhes o conteúdo questionado, explicando a lógica e as funções.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""


with st.sidebar:

    st.image("icon.jpg", width=140)
    st.title("Lasete AI")
    st.markdown("Liga Acadêmica de Segurança e Tecnologias Emergentes - UNDB.")

    
    # Campo da chave de API da Groq
    groq_api_key = os.getenv("QROQ_API_KEY")

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Assistente focado em cibersegurança e tecnologias emergentes.")

    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")

    st.markdown("---")
    st.markdown("Conheça mais sobre a Lasete:")

    # Link para o site da DSA
    st.markdown("🔗 [Site oficial](https://lasete.vercel.app)")
    st.markdown("🔗 [Instagram](https://www.instagram.com/lasete.undb)")
    
    # Botão de link para enviar e-mail ao suporte da DSA
    st.link_button("✉️ E-mail Para o Suporte no Caso de Dúvidas", "mailto:lasete.undb@gmail.com")

# Título principal do app
st.title("Lasete AI")
st.markdown("---")

# Texto auxiliar abaixo do título
st.caption("Faça sua pergunta sobre conteúdos abordados pela liga.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se existe a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(dsa_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Lasete AI - Parte Integrante da Liga Acadêmica de Segurança e Tecnologias Emergentes da UNDB.    </p>
    </div>
    """,
    unsafe_allow_html=True
)
