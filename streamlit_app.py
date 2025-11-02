import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot (Gemini 2.5 Pro)")
st.write(
    "このチャットボットはGoogle Gemini 2.5 Proを使って会話します。"
    "利用するには、Google Gemini APIキーが必要です。APIキーは [Google AI Studio](https://aistudio.google.com/) から取得できます。"
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Google Gemini APIキー", type="password")
if not gemini_api_key:
    st.info("続行するにはGoogle Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Configure Gemini API key
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("何か話しかけてみてください"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Geminiのチャットモデルを呼び出し
        model = genai.GenerativeModel("gemini-2.5-pro")
        chat = model.start_chat(history=[
            genai.types.Content(role=m["role"], parts=[m["content"]])
            for m in st.session_state.messages if m["role"] != "system"
        ])
        response = chat.send_message(prompt)
        # Geminiの応答を表示
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
