import streamlit as st
import openai
import os
from dotenv import load_dotenv
from faqs import FAQS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Customer Support Chatbot")
st.title("🤖 Customer Support Chatbot")
st.write("Hi! I’m here to help you 24/7 😊")

if "chat" not in st.session_state:
    st.session_state.chat = []

if "order_id" not in st.session_state:
    st.session_state.order_id = None

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your question here...")

def get_faq_answer(text):
    text = text.lower()
    for key in FAQS:
        if key in text:
            return FAQS[key]
    return None

def get_ai_answer(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    if st.session_state.order_id is None:
        if user_input.isdigit():
            st.session_state.order_id = user_input
            bot_reply = f"✅ Your order with ID **{user_input}** is currently being processed and will be delivered soon."
        else:
            faq_reply = get_faq_answer(user_input)
            if faq_reply:
                bot_reply = faq_reply
            else:
                bot_reply = get_ai_answer(user_input)
    else:
        bot_reply = f"📦 Your order **{st.session_state.order_id}** is on the way. Expected delivery in 2 days."

    st.session_state.chat.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)
