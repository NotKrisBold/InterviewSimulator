import ollama
import streamlit as st

# Init ollama client
client = ollama.Client()

st.title("Job interview simulator")

# Define model
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = "interviewer"

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]


userInput = st.chat_input("What is up?")

st.session_state["messages"].append({"role": "user", "content": userInput})

with st.chat_message("user"):
    st.markdown(userInput)

with st.chat_message("assistant"):
    message = st.write_stream(model_res_generator())
    st.session_state["messages"].append({"role": "assistant", "content": message, "toDisplay": message})
