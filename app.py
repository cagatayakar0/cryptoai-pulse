import streamlit as st
import requests
from google import genai

# 1. System & Page Configuration
st.set_page_config(page_title="CryptoAI-Pulse | Market Intelligence", page_icon="📊", layout="centered")

# 2. AI Client Initialization
GEMINI_API_KEY = "AIzaSyCEo-VlCyNEoEnN2vpCdOBqZkD10F2oWik"
client = genai.Client(api_key=GEMINI_API_KEY)

# Web Interface Header Section
st.title("📊 CryptoAI-Pulse")
st.subheader("Real-Time Data Analytics & AI Market Intelligence")
st.write("This intelligence platform integrates live market endpoints with generative AI to deliver institutional-grade market analysis.")
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
        with st.spinner("Gemini is generating a comprehensive market report, please wait... 🤖"):
            
            # Formulating the prompt to strictly generate institutional-grade English analysis
            prompt = f"""
            You are a Senior Crypto Quantitative Analyst and Macro Strategist. 
            Analyze the following real-time financial metrics provided by the system:
            - Bitcoin Spot Price: ${btc_price:,} USD
            - 24-Hour Price Delta: {btc_change:.2f}%

            Based on this data, deliver an institutional-grade, formal financial market analysis report.
            The report must cover the following critical areas:
            1. Current Price Action Assessment
            2. Market Psychology & Volume Dynamics Analysis (e.g., healthy consolidation, whale activity, or market momentum)
            3. Short-term Strategic Outlook & Risk Mitigation Steps for Asset Allocators (clearly state that this is not financial advice)
            
            Maintain a strictly professional, technical, and academic tone. Do NOT use emojis, social media hashtags (#), or refer to this as a social media 'post'. Output the report completely in professional English.
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