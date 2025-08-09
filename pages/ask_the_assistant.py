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
    "Answer only using the provided customs knowledge base (shown as {context}). "
    "Be factual, concise, professional, and warm in tone. "
    "For simple greetings or acknowledgments (e.g., 'thanks', 'ok', 'bye'), "
    "reply politely without repeating regulations unless asked. "
    "Do not pretend to be an officer or give advice outside official customs rules. "
    "If unsure, politely say you don't know."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Knowledge Base:\n{context}\n\nQuestion: {question}")
])

# ---- LLM & Chain ----
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=512
)
conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False,
    combine_docs_chain_kwargs={"prompt": prompt}
)

# ---- UI ----
st.caption("Type your question about customs. Press Enter to send!")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_bubble = """
<div style="width:100%; display:flex; justify-content:flex-end;">
    <div style="background-color:#e0f7fa; padding:10px 18px; border-radius:18px; margin-bottom:8px; max-width:72%;">
        {msg}
    </div>
</div>
"""

assistant_bubble = """
<div style="width:100%; display:flex; justify-content:flex-start;">
    <div style="background-color:#fff3e0; padding:10px 18px; border-radius:18px; margin-bottom:8px; max-width:72%;">
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
    user_input = st.session_state["user_input"].strip()
    st.session_state.chat_messages.append(("user", user_input))

    # Keyword-based soft close detection
    closing_keywords = [
        "ok", "okay", "okey", "oklah", "ok la", "thanks", "thank you", "terima kasih",
        "alright", "bye", "noted", "great", "appreciate"
    ]
    if any(kw in user_input.lower() for kw in closing_keywords):
        closing_reply = "You're welcome! Let me know if you have any other questions about Singapore Customs."
        st.session_state.chat_messages.append(("assistant", closing_reply))
    else:
        result = conversational_chain({
            "question": user_input,
            "chat_history": st.session_state.chat_history
        })
        answer = result["answer"]
        st.session_state.chat_messages.append(("assistant", answer))
        st.session_state.chat_history.append((user_input, answer))

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
