import os
from typing import Generator

import dotenv
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


dotenv.load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

CHROMA_PATH = "chroma"

template = ChatPromptTemplate([
    ("system", "You are a helpful AI bot. You answer the questions based on previous messages and on context but if the context doesn't help, use your previous knowledge."),
    ("human", "{user_input}")
])

llm = ChatGroq(model='llama3-8b-8192')
config = {"configurable": {"thread_id": "abc123"}}

# Define embedding model
model_name = "hkunlp/instructor-large"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    # model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

db = Chroma(
    embedding_function=hf,
    persist_directory=CHROMA_PATH
)

memory = MemorySaver()
retriever = db.as_retriever()

# Build retriever tool
tool = create_retriever_tool(
    retriever,
    "chroma_docs_retriever",
    "Searches and returns excerpts from the Shrek chunks.",
)
tools = [tool]

agent_executor = create_react_agent(llm, tools, checkpointer=memory)

st.set_page_config(page_icon="💬", layout="wide", page_title="ChatBot")
st.subheader("Groq Chatbot", divider="rainbow", anchor=False)


# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👨‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


if user_input := st.chat_input("Type your input here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_input)
    
    # Compose prompt
    prompt = template.invoke(user_input)

    # Fetch response from Groq API
    try:
        with st.chat_message("assistant", avatar="🤖"):
            agent_stream = agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="values"
            )

            # Stream and display the response
            for idx, event in enumerate(agent_stream):
                response = event["messages"][-1]

                print(f'evento {idx} ---------------------')
                print(event["messages"][-1])
                print(response.response_metadata)

                if response.response_metadata:
                    if response.response_metadata['finish_reason'] == "stop":
                        final_resp = response.content            


            # Save assistant response to session history
            # Append the full response to session_state.messages
            if isinstance(final_resp, str):
                st.session_state.messages.append(
                    {"role": "assistant", "content": final_resp}
                )
                st.write(final_resp)
            else:
                # Handle the case where full_response is not a string
                combined_response = "\n".join(str(item) for item in final_resp)
                st.session_state.messages.append(
                    {"role": "assistant", "content": combined_response}
                )
                st.write_stream(final_resp)

    except Exception as e:
        st.error(e, icon="🚨")
        import traceback
        traceback.print_exc()
