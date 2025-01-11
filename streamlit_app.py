__import__('pysqlite3')
import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import streamlit as st
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import requests
#import sqlite3
#import chromadb


def load_chroma_db():
    # Load the Chroma database
    embeddings = HuggingFaceEmbeddings()
    vectorstore = Chroma(embedding_function=embeddings)
    return vectorstore


def similarity_search(query, vectorstore):
    # Perform a similarity search
    results = vectorstore.similarity_search(query)
    return results


# Sidebar Navigation
with st.sidebar:
    st.title("🏭")
    st.title("**AI Advisory for Factory Legal**")
    if "page" not in st.session_state:
        st.session_state.page = "Home"
   
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("Legal Guidance"):
        st.session_state.page = "Legal Guidance"
    if st.button("Q&A Chatbot"):
        st.session_state.page = "Q&A Chatbot"
       
# Page Functions
def home_page_view():
    st.title("🏭")
    st.title("AI Advisory for Food Factory Setup")
    st.write("ระบบแนะนำข้อกำหนดทางกฎหมายและขั้นตอนการขออนุญาตจัดตั้งโรงงานอาหารในประเทศไทย")
    st.image(
        "https://img.freepik.com/free-vector/food-manufacturing-illustration_23-2149513856.jpg?semt=ais_hybrid",  # Replace with the URL of an industrial park image in Thailand
        #use_container_width=True
    )
    st.info("""
        Welcome to the AI Advisory system for Thailand's food factory legal guidance.
        This platform leverages Retrieval-Augmented Generation (RAG) technology and Generative AI to:
       
        - Provide clear and accurate legal guidance for food factory licenses.
        - Simplify regulatory processes.
        - Empower users with real-time legal assistance through an intelligent chatbot.
    """)


def legal_guidance_page():
    st.title("Legal Guidance for Food Factory")
    st.write("Provide details about your factory to receive tailored guidance.")


    # Load Vector Database
    chroma_db = load_chroma_db()


    # Input form for user details
    with st.form("factory_form"):
        factory_type = st.text_input("Enter Food Factory Type:")
        machine_power = st.number_input("Machine Power (HP):", min_value=0, step=1)
        employee = st.number_input("Number of Employees:", min_value=0, step=1)
        submit_button = st.form_submit_button("Get Guidance")

  with st.write("### Legal Guidance:")
        st.write("""
1. ประเภทอาหารและการจำแนกตาม TSIC ที่เกี่ยวข้อง:
   - ประเภทอาหาร: ผลิตภัณฑ์เนื้อสัตว์แปรรูป
   - การจำแนกตาม TSIC: หมวด 1013 - การผลิตผลิตภัณฑ์เนื้อสัตว์แปรรูป เช่น ไส้กรอก

2. ประกาศกระทรวงสาธารณสุขและเลขที่ประกาศที่เกี่ยวข้อง:
   - ประกาศกระทรวงสาธารณสุข ฉบับที่ 234 (พ.ศ. 2544) เรื่อง กำหนดคุณภาพหรือมาตรฐานของอาหาร
   - ประกาศกระทรวงสาธารณสุข ฉบับที่ 159 (พ.ศ. 2536) เรื่อง การควบคุมการผลิตอาหารประเภทเนื้อสัตว์แปรรูป

3. ระบุว่ากิจการโรงงานนี้ต้องยื่นขอใบอนุญาตประเภทใด:
   - จากข้อมูลที่ให้มา:
     - แรงม้าของเครื่องจักร: 44 แรงม้า
     - จำนวนพนักงาน: 7 คน
   - ประเภทโรงงานที่ต้องยื่นขอ: แบบ อ.1 (ใบอนุญาตประกอบกิจการจากกองอาหารและยา)

4. รายการเอกสารเบื้องต้นที่ต้องใช้สำหรับการยื่นขอใบอนุญาต:
   - แบบฟอร์มคำขออนุญาตประกอบกิจการโรงงาน (อ.1)
   - สำเนาทะเบียนบ้านหรือเอกสารแสดงกรรมสิทธิ์ในที่ตั้งโรงงาน
   - แผนผังโรงงานและตำแหน่งติดตั้งเครื่องจักร
   - รายการเครื่องจักรพร้อมรายละเอียดกำลังแรงม้า
   - แผนการจัดการด้านสุขลักษณะและความปลอดภัยของพนักงาน
   - ผลการตรวจวิเคราะห์คุณภาพผลิตภัณฑ์เบื้องต้น (ถ้ามี)
   - สำเนาบัตรประจำตัวประชาชนหรือเอกสารยืนยันตัวตนของผู้ยื่นคำขอ
        """)
    if submit_button:
        st.write("### Your Factory Details:")
        st.write(f"**Factory Type:** {factory_type}")
        st.write(f"**Machine Power:** {machine_power} HP")
        st.write(f"**Number of Employees:** {employee}")


        # Similarity Search
        tsic_results = similarity_search(factory_type, chroma_db)
        food_law_results = similarity_search(factory_type, chroma_db)


        # Use Google Gemini to Generate Display Results
        #with st.spinner("Generating insights with Generative AI..."):
        #    api_key = st.secrets.get("gemini_api_key", "AIzaSyBnlQoQBbgfUgJwkTyHZ7l1ZMXDx7L3hAg")  # Replace with actual API key or config
        #    headers = {"Authorization": f"Bearer {api_key}"}


        try:
            gemini_api_key = st.secrets.get("gemini_api_key", "AIzaSyBnlQoQBbgfUgJwkTyHZ7l1ZMXDx7L3hAg")  # Replace with your actual key
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel("gemini-pro")  # Use your specific Gemini model
            generation_config = { 
                "temperature" : 0.9 , 
                "top_p" : 1 , 
                "top_k" : 1 , 
                "max_output_tokens" : 2048 , 
} 
            st.success("Gemini API Key successfully configured.")


            prompt = f"""
จากข้อมูลต่อไปนี้:
- ผลลัพธ์จาก TSIC: {[result['content'] for result in tsic_results]}
- ผลลัพธ์จากกฎหมายอาหาร (Food Law): {[result['content'] for result in food_law_results]}
- แรงม้าของเครื่องจักร: {machine_power} แรงม้า
- จำนวนพนักงาน: {employee} คน


กรุณาให้ข้อมูลดังต่อไปนี้:
1. ประเภทอาหารและการจำแนกตาม TSIC ที่เกี่ยวข้อง
2. ประกาศกระทรวงสาธารณสุขและเลขที่ประกาศที่เกี่ยวข้อง
3. ระบุว่ากิจการโรงงานนี้ต้องยื่นขอใบอนุญาตประเภทใด (รง.4 หรือ อ.1) โดยพิจารณาจากแรงม้าและจำนวนพนักงาน
4. รายการเอกสารเบื้องต้นที่ต้องใช้สำหรับการยื่นขอใบอนุญาตดังกล่าว
"""
             # Generate Response
             
            #response = genai.generate_context(model="gemini-pro", prompt=prompt, max_tokens=300)
            response = model.generate_context(prompt)
            st.write("### Legal Guidance:")
            st.write(response.result)


        except Exception as e:
            st.error(f"An error occurred while setting up the Gemini model: {e}")


def qa_chatbot_page():
    st.title("Q&A Chatbot")
    st.write("Ask questions about food factory regulations. The chatbot retrieves information from a vector database and uses GenAI (Gemini) for intelligent responses.")


    # Chatbot interface
    with st.form("chat_form"):
        user_query = st.text_input("Ask your legal question:")
        submit_chat = st.form_submit_button("Get Answer")


    if submit_chat:
        if user_query:
            # Simulated retrieval and AI response
            with st.spinner("Retrieving and generating answer..."):
                api_key = st.secrets.get("gemini_api_key", "AIzaSyBnlQoQBbgfUgJwkTyHZ7l1ZMXDx7L3hAg")  # Replace with actual API key or config
                headers = {"Authorization": f"Bearer {api_key}"}
                payload = {
                    "prompt": f"""
                    Retrieve information and provide an answer to the following question:
                    {user_query}
                    """,
                    "max_tokens": 200,
                }
                # Example API call (replace with real endpoint)
                try:
                    response = requests.post("https://api.example.com/generate", headers=headers, json=payload)
                    if response.status_code == 200:
                        st.write("### Answer:")
                        st.write(response.json().get("output", "No data found."))
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question.")


# Main Function
def main():


    if st.session_state.page == "Home":
        home_page_view()
    elif st.session_state.page == "Legal Guidance":
        legal_guidance_page()
    elif st.session_state.page == "Q&A Chatbot":
        qa_chatbot_page()


if __name__ == '__main__':
    main()
