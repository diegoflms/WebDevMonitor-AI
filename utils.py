from openai import OpenAI
import streamlit as st
import uuid
from sheets import add_rows_to_sheet, build_list_to_sheet, init_google_sheets

def save_feedback(index, tab):
    """Salva o feedback do usuário para uma mensagem específica, atualizando o estado da mensagem e registrando a avaliação no Google Sheets."""
    st.session_state.messages[index]["feedback"] = st.session_state[f"feedback_{index}"]
    feedback_list = build_list_to_sheet(
        st.session_state.messages[index]["message_id"],
        "feedback",
        "feedback",
        st.session_state[f"feedback_{index}"],
        0, # Token usage não é atualizado aqui
    )
    add_rows_to_sheet(tab, [feedback_list])

def click_question(question):
    """Função utilitária para lidar com o clique em uma pergunta pré-definida na sidebar, atualizando o estado para que a pergunta seja processada como input do usuário."""
    st.session_state.clicked_question = question

@st.cache_resource # Garante que a conexão com OpenAI e Sheets só aconteça UMA vez
def load_connections():
    """Inicializa as conexões com OpenAI e Google Sheets, retornando os objetos de cliente e aba."""
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )
    tab = init_google_sheets()
    
    return client, tab

def init_session_state():
    """Inicializa as variáveis de estado necessárias para a aplicação, garantindo que existam antes de qualquer interação do usuário."""
    if 'uuid' not in st.session_state:
        st.session_state['uuid'] = str(uuid.uuid4())
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if "model" not in st.session_state:
        st.session_state["model"] = st.secrets["GROQ_MODEL"]
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "clicked_question" not in st.session_state:
        st.session_state.clicked_question = None

def get_ai_response(client, model, messages, usage_dict):
    """Obtém a resposta da IA, atualizando o dicionário de uso de tokens."""
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
    )

    for chunk in stream:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            content = chunk.choices[0].delta.content
            if content:
                yield content
        
        # Captura metadados de uso (tokens) quando o stream termina
        if hasattr(chunk, 'usage') and chunk.usage is not None:
            usage_dict["prompt"] = chunk.usage.prompt_tokens
            usage_dict["completion"] = chunk.usage.completion_tokens
            if hasattr(chunk.usage, 'prompt_tokens_details') and chunk.usage.prompt_tokens_details:
                usage_dict["cached"] = chunk.usage.prompt_tokens_details.cached_tokens