import streamlit as st
from PIL import Image
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="Personal Chef AI",
    page_icon="👨‍🍳",
    layout="centered", # 'centered' foca a atenção no meio da tela (mais minimalista)
    initial_sidebar_state="collapsed"
)

# --- CSS Customizado para Estilo Minimalista ---
st.markdown("""
<style>
    /* Remove o padding padrão exagerado do topo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Estiliza o título principal */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        color: #333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    /* Estiliza o botão de upload para ficar mais discreto */
    .stFileUploader {
        max-width: 500px;
        margin: 0 auto;
    }
    /* Card de receita (exemplo de formatação) */
    .recipe-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Funções Auxiliares (Mockup da IA) ---
def mock_analyze_image(image):
    """Simula a análise da imagem (substitua pela sua lógica do LangChain)"""
    time.sleep(2) # Simula delay de processamento
    return ["Ovos", "Tomate", "Queijo Parmesão", "Manjericão"]

def mock_generate_recipe(ingredients):
    """Simula a geração da receita"""
    time.sleep(2)
    return f"""
    ### 🍳 Omelete Caprese Rústica
    
    Com base nos ingredientes **{', '.join(ingredients)}**, aqui está uma sugestão rápida e deliciosa.
    
    **Tempo:** 15 min | **Dificuldade:** Fácil
    
    **Ingredientes:**
    * 3 Ovos
    * 1 Tomate picado
    * 50g Queijo Parmesão
    * Folhas de Manjericão fresco
    
    **Modo de Preparo:**
    1. Bata os ovos com uma pitada de sal.
    2. Aqueça a frigideira e despeje os ovos.
    3. Quando a borda firmar, adicione o tomate e o queijo.
    4. Dobre ao meio e finalize com manjericão.
    """

# --- Inicialização do Estado (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ingredients" not in st.session_state:
    st.session_state.ingredients = None

# --- Cabeçalho ---
st.title("👨‍🍳 Personal Chef AI")
st.markdown('<p class="subtitle">O que tem na sua geladeira hoje? Tire uma foto e deixe-me criar a receita.</p>', unsafe_allow_html=True)

# --- Área de Upload ---
# Container para centralizar visualmente
upload_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Arraste sua foto ou clique para buscar", 
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed" # Esconde o label para ficar mais limpo
    )

# --- Lógica Principal ---
if uploaded_file is not None:
    # 1. Exibir a Imagem (Preview compacto)
    image = Image.open(uploaded_file)
    
    # Criamos colunas para centralizar a imagem pequena e não ocupar a tela toda
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Sua despensa/geladeira", use_column_width=True)
    
    # Botão de Ação (Só aparece se tiver imagem)
    # Centralizado via colunas
    b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
    with b_col2:
        analyze_btn = st.button("🔍 Analisar e Cozinhar", type="primary", use_container_width=True)

    if analyze_btn:
        # AQUI VOCÊ CONECTARÁ SEU AGENTE LANGCHAIN
        
        with st.spinner("O Chef está analisando seus ingredientes..."):
            # Passo 1: Visão
            detected_ingredients = mock_analyze_image(uploaded_file)
            st.session_state.ingredients = detected_ingredients
            
            # Adiciona mensagem do sistema ao chat
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Identifiquei os seguintes ingredientes: **{', '.join(detected_ingredients)}**. Procurando a melhor receita..."
            })

        with st.spinner("Buscando receitas na web e criando o passo a passo..."):
            # Passo 2: Agente / Busca
            recipe = mock_generate_recipe(detected_ingredients)
            st.session_state.messages.append({"role": "assistant", "content": recipe})

# --- Interface de Chat (Abaixo do Upload) ---
st.divider()

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input para conversa contínua (Follow-up questions)
if prompt := st.chat_input("Pergunte algo sobre a receita (ex: 'Posso trocar tomate por cebola?')"):
    # Adiciona msg do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Agente (Simulação)
    with st.chat_message("assistant"):
        with st.spinner("Consultando o Chef..."):
            time.sleep(1)
            response = "Sim! Cebola caramelizada ficaria ótimo nessa combinação."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- Sidebar para Configurações (Opcional, mantém a tela limpa) ---
with st.sidebar:
    st.header("⚙️ Preferências")
    diet = st.selectbox("Restrição Alimentar", ["Nenhuma", "Vegano", "Vegetariano", "Sem Glúten", "Low Carb"])
    cuisine = st.selectbox("Estilo de Cozinha", ["Qualquer", "Italiana", "Brasileira", "Asiática", "Francesa"])
    
    st.divider()
    if st.button("Limpar Histórico"):
        st.session_state.messages = []
        st.session_state.ingredients = None
        st.rerun()