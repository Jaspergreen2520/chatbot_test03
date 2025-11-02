import streamlit as st
import google.generativeai as genai

st.title("💬 教えてGemini！")
st.write(
    "このチャットボットはGoogle Gemini 2.5 Proを使って会話します。"
    "利用するには、Google Gemini APIキーが必要です。APIキーは [Google AI Studio](https://aistudio.google.com/) から取得できます。"
)

gemini_api_key = st.text_input("Google Gemini APIキー", type="password")
if not gemini_api_key:
    st.info("続行するにはGoogle Gemini APIキーを入力してください。", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("何か話しかけてみてください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini用のhistory形式
        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            elif m["role"] == "assistant":
                history.append({"role": "model", "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-2.5-pro")
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
