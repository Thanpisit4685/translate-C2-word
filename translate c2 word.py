import streamlit as st
import openai
import pandas as pd
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
import newspaper 




def read_news_from_url(url):
    try:
        # ดึง HTML จาก URL
        response = requests.get(url)
        response.raise_for_status()

        # สร้างออบเจ็กต์ Article จาก URL โดยใช้ newspaper
        article = newspaper.Article(url)
        article.download()
        article.parse()

        # รับข้อมูลข่าวเป็นข้อความ
        news_text = article.text

        return news_text

        

    except Exception as e:
        print(f"Error reading news from URL: {e}")
        return None


def get_text(url):
    try:
        respone = requests.get(url)
        respone.raise_for_status()
        soup = BeautifulSoup(respone.content, 'html.parser')
        text = soup.get_text()
        return text
    except requests.exceptions.HTTPError as e:
        st.error(f"Error fetching text from URL: {e}")
        return None

#ใช้ openai แปลงเป็นภาษาไทย
def find_C2_vocab(text):
    prompt = f"Act as an English teacher and find C2 level vocabulary in the following text:\n\n{text}"
    respones = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    C2_vocab = respones.choices[0].text.strip().split("\n")
    return C2_vocab

def translate_to_thai(words):
    translator = Translator()
    thai_text = [translator.translate(word, src='en', dest='th').text for word in words]
    return thai_text.text

def main():
    st.title("English Teacher Assistant")
    st.subheader("👋🏻 Welcome to English Teacher Assistant 👋🏻")
    st.write("This app will help you to translate English text to Thai language and find the words in C2 level vocabulary.")
    
    openai_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

    # ตรวจสอบว่า API key ถูกป้อนหรือไม่
    if not openai_key:
        st.warning("Please enter your OpenAI API Key.")
        st.stop()

    # กำหนด API key ใน OpenAI
    openai.api_key = openai_key
    url = st.text_input("Enter url link here")

    if st.button("Submit"):
        
        if url:
            text = read_news_from_url(url)
            if text:
                C2_vocab = find_C2_vocab(text)
                
                thai_text = translate_to_thai(C2_vocab)

                df = pd.DataFrame({
                    "English": C2_vocab,
                    "Thai": thai_text
                })
                st.table(df)
            else:
                st.warning("Failed to fetch text from the provided URL.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()