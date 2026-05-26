import streamlit as st
import requests
from google import genai
import os

# 1. System & Page Configuration
st.set_page_config(
    page_title="CryptoAI-Pulse | Market Intelligence", 
    page_icon="📊", 
    layout="centered"
)

# 2. AI Client Initialization (Secured with Streamlit Secrets)
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
client = genai.Client()

# Web Interface Header Section
st.title("📊 CryptoAI-Pulse")
st.subheader("Real-Time Data Analytics & AI Market Intelligence")
st.write("This intelligence platform integrates live market endpoints with generative AI to deliver clear and actionable market insights.")
st.write("---")

# 3. Live Data Fetching Function (CoinGecko API)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url)
    return response.json()

# Refresh Trigger Button
if st.button("🔄 Refresh Live Metrics"):
    st.rerun()

try:
    data = get_crypto_data()
    btc_price = data["bitcoin"]["usd"]
    btc_change = data["bitcoin"]["usd_24h_change"]

    # 4. Financial Metric Cards Displays
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Bitcoin (BTC) Spot Price", value=f"${btc_price:,} USD")
    with col2:
        st.metric(label="24h Price Performance", value=f"{btc_change:.2f}%", delta=f"{btc_change:.2f}%")

    st.write("---")
    st.write("### 🧠 Generative AI Market Intelligence")

    # 5. Professional Analysis Execution Button
    if st.button("📈 Execute AI Market Analysis"):
        with st.spinner("Gemini is generating a sharp market report, please wait... 🤖"):
            
            # Formulating the prompt for a clean, simplified, bullet-point English overview
            prompt = f"""
            You are an elite digital asset strategist and financial analyst. Your task is to analyze the provided real-time Bitcoin data and deliver a sharp, high-impact market overview suitable for a professional network like LinkedIn.

            Rules:
            1. Strictly avoid dense banking jargon (e.g., 'idiosyncratic risk', 'abatement'). Keep it clean, direct, and understandable for everyone.
            2. Structure the analysis using clear bullet points and bold headers. No long text walls.
            3. Tone must be sharp, modern, professional, and insightful. Completely in English.

            Market Data:
            - Bitcoin Price: ${btc_price} USD
            - 24h Change: {btc_change:.2f}%

            Output Template Format (Follow this exactly, do not add extra text outside this format):
            📊 **Bitcoin (BTC) Real-Time Market Assessment**

            * **Price Action Momentum:** [Briefly interpret the price and 24h delta. Is it cooling off, breaking out, or consolidating?]
            * **Market Psychology:** [Analyze the current sentiment based on the movement. Is this a healthy correction, minor profit-taking, or a strong risk signal?]
            * **Short-Term Outlook:** [Provide a direct, 1-2 sentence tactical takeaway for asset allocators.]
            
            Disclaimer: Not financial advice.
            """
            
            response_ai = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            # Rendering the response elegantly inside a modern Markdown block
            st.success("Market Intelligence Report Generated Successfully!")
            st.markdown(response_ai.text)

except Exception as e:
    st.error(f"Data ingestion pipeline failed: {e}")