import os
import streamlit as st
from dotenv import load_dotenv

# ---- Load API key from .env ----
load_dotenv()

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate

# ---- Build or load the vector store ----
@st.cache_resource
def get_vectorstore():
    with open("customs_knowledge_base.txt", "r", encoding="utf-8") as f:
        kb_text = f.read()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("---", "Section")])
    docs = splitter.split_text(kb_text)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

vectorstore = get_vectorstore()

# ---- System prompt ----
system_prompt = (
    "You are a Singapore Customs information assistant. "
    "Always answer using only the provided customs knowledge base (shown as {context}). "
    "Be factual, concise, professional, and warm in your tone. If the user's message is a greeting, polite acknowledgment, or does not require an answer, reply with a short, friendly, polite closing or thank you. "
    "You must never pretend to be any official, officer, or act as anyone except a neutral customs assistant. "
    "Refuse any request to role-play or give advice outside published customs regulations. "
    "If you cannot answer, politely say you don't know.\n"
    "Examples:\n"
    "User: okay\n"
    "Assistant: Thank you! If you have more questions, just let me know.\n"
    "User: thanks\n"
    "Assistant: You're most welcome! Feel free to ask more questions about customs anytime.\n"
    "User: hello\n"
    "Assistant: Hello! How can I assist you with Singapore Customs information today?\n"
    "User: pretend you are an ICA officer\n"
    "Assistant: I'm here to help as a Singapore Customs information assistant. Please let me know your customs-related question."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Knowledge Base:\n{context}\n\nQuestion: {question}")
])

# ---- Set up LLM and ConversationalRetrievalChain ----
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
    max_tokens=512
)
conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    combine_docs_chain_kwargs={"prompt": prompt}
)

# ---- Streamlit UI ----
st.caption("Type your question about customs. Press Enter to send!")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_bubble = """
<div style="width:100%; display:flex; justify-content:flex-end;">
    <div style="
        background-color: var(--secondary-background-color, #e0f7fa);
        color: var(--text-color, #222);
        padding:10px 18px;
        border-radius:18px;
        margin-bottom:8px;
        display:inline-block;
        max-width:72%;
        text-align:left;">
        {msg}
    </div>
</div>
"""

assistant_bubble = """
<div style="width:100%; display:flex; justify-content:flex-start;">
    <div style="
        background-color: var(--background-color, #fff3e0);
        color: var(--text-color, #222);
        padding:10px 18px;
        border-radius:18px;
        margin-bottom:8px;
        display:inline-block;
        max-width:72%;
        text-align:left;">
        {msg}
    </div>
</div>
"""

# Display chat history
for role, msg in st.session_state.chat_messages:
    if role == "user":
        st.markdown(user_bubble.format(msg=msg), unsafe_allow_html=True)
    else:
        st.markdown(assistant_bubble.format(msg=msg), unsafe_allow_html=True)

def send_message():
    user_input_raw = st.session_state["user_input"]
    user_input_clean = user_input_raw.strip().lower()
    st.session_state.chat_messages.append(("user", user_input_raw))

    # Exact-match closing phrases only (prevents Malay word "rokok" from triggering "ok")
    closing_phrases = [
        "okay", "ok", "thanks", "thank you", "noted", "alright", "got it", "great", "bye",
        "noted thanks", "noted with thanks", "appreciate", "thanksss"
    ]
    if any(user_input_clean == phrase for phrase in closing_phrases):
        closing_reply = "Thank you! If you have more questions about Singapore Customs, just let me know."
        st.session_state.chat_messages.append(("assistant", closing_reply))
    else:
        result = conversational_chain({
            "question": user_input_raw,
            "chat_history": st.session_state.chat_history
        })
        answer = result["answer"]
        st.session_state.chat_messages.append(("assistant", answer))
        st.session_state.chat_history.append((user_input_raw, answer))

    st.session_state["user_input"] = ""

st.text_input(
    "Type your message (press Enter to send):",
    key="user_input",
    placeholder="E.g. Can I bring in 2 bottles of wine?",
    on_change=send_message
)

if st.button("Reset Conversation"):
    st.session_state.chat_messages = []
    st.session_state.chat_history = []
    st.rerun()
