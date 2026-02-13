# Cores base para o tema
BLUE = "#72839d"    # Azul do LabES
ORANGE = "#F9A940"  # Laranja do LabES
BLACK = "#000000"   # Preto

def get_main_styles():
    """Retorna o CSS principal para estilização da aplicação, incluindo ajustes globais, sidebar, botões, expander e avatares do chat."""
    return f"""
<style>
    /* 1. Elementos Globais e Limpeza */
    .stDeployButton, [data-testid="stMainMenu"], [data-testid="stStatusWidget"], 
    footer, [data-testid="stDecoration"],  {{
        visibility: hidden;
        display: none;
    }}
    .block-container {{ padding-top: 2rem !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    #GithubIcon {{ visibility: hidden; }}

    /* 2. Sidebar */
    [data-testid="stSidebar"] {{ background-color: {BLUE} !important; }}
    [data-testid="stSidebar"] * {{ color: {BLACK} !important; }}

    /* 3. Botões da Sidebar */
    [data-testid="stSidebar"] .stButton button {{
        width: 100%;
        border-radius: 8px;
        transition: all 0.3s;
        background-color: {ORANGE} !important;
        border: 1px solid {ORANGE} !important;
        color: {BLACK} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stButton button:hover {{
        background-color: #d68233 !important;
        border-color: {ORANGE} !important;
    }}

    /* 4. Expander */
    [data-testid="stSidebar"] [data-testid="stExpander"] {{
        border: none !important;
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] [data-testid="stExpander"] details summary {{
        background-color: {ORANGE} !important;
        border-radius: 8px !important;
        color: {BLACK} !important;
    }}

    /* 5. Avatares do Chat */
    [data-testid="stChatMessageAvatarAssistant"] {{ background-color: {ORANGE} !important; }}
    [data-testid="stChatMessageAvatarUser"] {{ background-color: {BLUE} !important; }}

    /* 6. Snippet do Fórum */
    div[data-testid="stToolbar"] {{
        visibility: hidden;
        height: 0%;
        position: fixed;
    }}
    div[data-testid="stDecoration"] {{
    visibility: hidden;
    height: 0%;
    position: fixed;
    }}
    div[data-testid="stStatusWidget"] {{
    visibility: hidden;
    height: 0%;
    position: fixed;
    }}
    #MainMenu {{
    visibility: hidden;
    height: 0%;
    }}
    header {{
    visibility: hidden;
    height: 0%;
    }}
    footer {{
    visibility: hidden;
    height: 0%;
    }}
</style>
"""

def get_login_styles():
    """Retorna o CSS específico para a tela de login, incluindo cores, fontes e layout para criar uma experiência de boas-vindas alinhada com a identidade visual do LabES."""
    return f"""
<style>
    /* 1. Estilos para a tela de login */
    .stApp {{ background-color: {BLUE} !important; }}
    [data-testid="stForm"] {{ background-color: transparent !important; border: none !important; padding: 0px !important; }}
    .login-title {{ color: #FFFFFF; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0px; }}
    .login-subtitle {{ color: #E0E0E0; font-size: 1.1rem; font-style: italic; text-align: center; margin-bottom: 1rem; }}
    
    /* 2. Estilos para os campos de entrada */
    div.stFormSubmitButton > button {{
        background-color: {ORANGE} !important;
        color: {BLACK} !important;
        border-radius: 8px !important;
        border: 2px solid {ORANGE} !important;
        font-weight: bold !important;
    }}
    
    /* 3. Ajustes adicionais */
    [data-testid="InputInstructions"] {{ display: none !important; }}
    [data-testid="stImage"] {{ display: flex; justify-content: center; margin-bottom: -15px !important; }}
</style>
"""