# 👨‍🍳 Personal Chef Assistant

O **Personal Chef Assistant** é uma aplicação inteligente que transforma o conteúdo da sua geladeira em receitas deliciosas. Basta enviar uma foto dos seus ingredientes e o assistente, agindo como um Chef profissional, irá sugerir pratos personalizados.

## 🚀 Tecnologias Utilizadas

Este projeto demonstra o uso de tecnologias modernas de Engenharia de IA, com foco em interatividade e manutenção de contexto:

- **[Streamlit](https://streamlit.io/)**: Framework Python utilizado para construir toda a interface web de forma ágil e eficiente.
- **[LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)**: O "cérebro" da aplicação. Utilizamos LangGraph para orquestrar o fluxo do agente.
- **Memória de Sessão (Memory)**: Um dos diferenciais do projeto. Utilizando `InMemorySaver` do LangGraph, o agente mantém o **estado da conversa**. Isso permite que você refine a receita (ex: "Não gosto de cebola, troque por outro ingrediente") e o Chef entenda o contexto perfeitamente.
- **Python**: Linguagem base do projeto.
- **Modelos Multimodais**: Capacidade de "ver" e interpretar imagens dos ingredientes.
- **[Tavily](https://tavily.com/)**: Ferramenta de busca utilizada pelo agente para consultar informações atualizadas na web, caso necessário.

## 🧠 Como Funciona a Memória?

A implementação de **memória** é crucial para uma experiência natural. Ao invés de cada interação ser isolada (stateless), o sistema armazena o histórico do chat na sessão atual (`thread_id`). 

Isso possibilita uma conversa fluida onde o assistente lembra:
1. Da imagem que você enviou.
2. Da receita que ele acabou de sugerir.
3. Das suas preferências citadas anteriormente na conversa.

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.11+
- Gerenciador de dependências `uv` (recomendado) ou `pip`.
- Chaves de API configuradas no `.env` (OpenAI/Anthropic e Tavily).

### Instalação

1. **Clone o repositório** e entre na pasta:
   ```bash
   git clone <seu-repo>
   cd personal_chef_assistant
   ```

2. **Instale as dependências**:
   ```bash
   uv sync
   # ou, se preferir pip:
   pip install -r requirements.txt
   ```

3. **Inicie a aplicação**:
   ```bash
   streamlit run app.py
   ```
