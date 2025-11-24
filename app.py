import streamlit as st
import requests
import os

# لینک backend FastAPI (بعداً پر می‌کنیم)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Persian Chatbot", layout="centered")
st.title("🤖 چت‌بات هوشمند فارسی")

# ذخیره مکالمات در session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"system","content":"You are a helpful Persian AI assistant."}
    ]

def send(text):
    st.session_state.messages.append({"role":"user","content":text})
    payload = {"messages": st.session_state.messages}

    try:
        r = requests.post(f"{BACKEND_URL}/chat", json=payload)
        reply = r.json().get("reply","")
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.messages.append({"role":"assistant","content":reply})

# فرم ورود پیام
with st.form("msg_form", clear_on_submit=True):
    text = st.text_input("پیام شما:")
    send_btn = st.form_submit_button("ارسال")
    if send_btn and text:
        send(text)

# نمایش مکالمات
for m in st.session_state.messages:
    if m["role"]=="user":
        st.markdown(f"**شما:** {m['content']}")
    elif m["role"]=="assistant":
        st.markdown(f"**ربات:** {m['content']}")
