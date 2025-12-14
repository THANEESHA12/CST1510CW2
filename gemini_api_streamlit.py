import streamlit as st
from google import genai
from google.genai import types

def gemini_main():
    st.set_page_config(page_title="AI Assistant", layout="wide")

    st.session_state.show_register = False
    st.session_state.show_login = False

    #Allows user to move through other sections of the platform
    with st.sidebar:
        st.title("**Navigation**")
        st.divider()
        st.title("**Quick Access**")
        if st.button("Home", key="nav_home_ai"):
            st.session_state.current_page = "home"; st.rerun()
        if st.button("Cyber Security", key="nav_cy_ai"):
            st.session_state.current_page = "cybersecurity"; st.rerun()
        if st.button("Data Science", key="nav_ds_ai"):
            st.session_state.current_page = "data_science"; st.rerun()
        if st.button("IT Operations", key="nav_ops_ai"):
            st.session_state.current_page = "it_operations"; st.rerun()
        if st.button("AI Analyzer", key="gemini_nav_ai_analyzer"):
            st.session_state.current_page = "AI_analyzer"; st.rerun()

      

        st.divider()
        st.title("**Artificial Intelligence**") #
        st.button("AI Assistant", use_container_width=True, disabled=True, key="nav_ai_assistant_disabled")


        st.divider()
        #This us where the conversation is saved at and it can be deleted also
        st.title("Chat Controls")
        message_count = len(st.session_state.get("messages", []))
        st.metric("Messages", message_count)
        if st.button("Logout", use_container_width=True, key="ai_logout"):
            st.session_state.user_logged_in = False
            st.session_state.username = None
            st.session_state.user_role = None
            st.success("Logged out.")
            st.switch_page("streamlit_code/home.py")
        if st.button("Clear Chat", use_container_width=True, key="ai_clear_chat"):
            st.session_state.messages = []
            st.rerun()

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    st.subheader("Gemini API")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = "assistant" if message["role"] == "model" else message["role"]
        with st.chat_message(role): #This display a bot emoji
            st.markdown(message["parts"][0]["text"])

    prompt = st.chat_input("Say Something")

    if prompt:
        with st.chat_message("user"): #This displays and emoji that represents user
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction="You are assistant."),
            contents=st.session_state.messages,
        )

        with st.chat_message("assistant"):
            container = st.empty()
            full_reply = ""
            for chunk in response:
                full_reply += chunk.text
                container.markdown(full_reply)

        st.session_state.messages.append({"role": "model", "parts": [{"text": full_reply}]})
        st.rerun()

if __name__ == "__main__":
    gemini_main()
