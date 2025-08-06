import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from lang_core.messages import SystemMessage

import os

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize ChatOpenAI and ConversationChain
# llm = ChatOpenAI(model_name="gpt-4o-mini")
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
# llm = ChatOpenAI(model = "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
#                      openai_api_key = st.secrets["TOGETHER_API_KEY"] , ## use your key
#                      openai_api_base = "https://api.together.xyz/v1"
#
#)

system_message = """You are a BearBot, a helpful AI assistant created by Build Fast with AI.
You answer questions in a funny and engaging way with unusual analogies.
You don't answer any questions not related to AI. Please respond with 'I cannot answer the question' for non-AI questions.
 """
conversation.memory.chat_memory.add_message(SystemMessage(content=system_message))
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Simple Chat Interface for LLMs by Build Fast with AI")


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
