# 📁 File: app.py

import streamlit as st
from agent import build_qa_chain
from utils.web_scraper import scrape_website
from tools.swot_tool import generate_swot
from tools.news_tool import fetch_news
from tools.summary_tool import summarize_docs
from tools.risk_tool import analyze_risks_with_severity
from tools.stock_tool import fetch_stock_data, plot_stock_chart
import plotly.graph_objects as go

st.set_page_config(page_title="AI Business Intelligence", layout="wide")
st.title("📊 AI Business Intelligence")

# --- Session State Initialization ---
if "stock" not in st.session_state:
    st.session_state.stock = {}

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "docs" not in st.session_state:
    st.session_state.docs = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "swot" not in st.session_state:
    st.session_state.swot = ""

if "news" not in st.session_state:
    st.session_state.news = []

if "risks" not in st.session_state:
    st.session_state.risks = {}

if "comp_summary" not in st.session_state:
    st.session_state.comp_summary = ""

if "comp_swot" not in st.session_state:
    st.session_state.comp_swot = ""


# --- Sidebar Input ---
st.sidebar.header("Company Info")
url = st.sidebar.text_input("🔗 Company Website URL", "https://python.langchain.com/")
company_name = st.sidebar.text_input("🏢 Company Name", "Langchain")

st.sidebar.markdown("---")
st.sidebar.header("Competitor Info")
comp_url = st.sidebar.text_input("🔗 Competitor Website URL", "https://www.crewai.com/")
comp_name = st.sidebar.text_input("🏢 Competitor Name", "Crewai")

if st.sidebar.button("🚀 Analyze"):
    with st.spinner("Scraping and analyzing both companies..."):
        # Primary Company
        docs = scrape_website(url)
        comp_docs = scrape_website(comp_url)

        if docs and comp_docs:
            # Main Company Chains
            qa_chain = build_qa_chain(docs)
            st.session_state.qa_chain = qa_chain
            st.session_state.docs = docs
            content = " ".join([d.page_content for d in docs])
            st.session_state.swot = generate_swot(company_name, content)
            st.session_state.news = fetch_news(company_name)
            st.session_state.stock = fetch_stock_data(company_name)
            st.session_state.summary = summarize_docs(docs)
            st.session_state.risks = analyze_risks_with_severity(company_name, content)

            # Competitor Chains
            st.session_state.comp_summary = summarize_docs(comp_docs)
            comp_content = " ".join([d.page_content for d in comp_docs])
            st.session_state.comp_swot = generate_swot(comp_name, comp_content)

# --- Tabs ---
if "qa_chain" in st.session_state:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "💬 Ask Questions", "📈 SWOT Analysis", "📰 News & Stock", "🧠 Key Takeaways",
        "⚔️ Compare Competitors", "⚠️ Risk Analysis", "📊 SWOT Radar",
        "📉 Risk Radar", "📈 Stock Trends"
    ])

    with tab1:
        question = st.text_input("Ask something about the company:")
        if question:
            answer = st.session_state.qa_chain.run(question)
            st.markdown(f"**Answer:** {answer}")

    with tab2:
        st.markdown("### SWOT Analysis")
        st.markdown(st.session_state.swot)

    with tab3:
        st.markdown("### 📰 Latest News")
        for item in st.session_state.news:
            st.write(f"- {item}")
    
        st.markdown("### 💹 Stock Data")
        stock = st.session_state.stock
        
        # Check if stock data exists and has required fields
        if stock and all(key in stock for key in ['symbol', 'price', 'change', 'market_cap']):
            st.write(f"**Symbol**: {stock['symbol']}")
            st.write(f"**Price**: {stock['price']}")
            st.write(f"**Change**: {stock['change']}")
            st.write(f"**Market Cap**: {stock['market_cap']}")
        else:
            st.warning("Stock data not available for this company. It may not be publicly traded or the data couldn't be retrieved.")

    with tab4:
        st.markdown("### 🧠 AI Summary of Website")
        st.markdown(st.session_state.summary)

    with tab5:
        st.markdown("### ⚔️ Competitor Comparison")
        st.subheader("Your Company Summary")
        st.markdown(st.session_state.summary)

        st.subheader("Competitor Summary")
        st.markdown(st.session_state.comp_summary)

        st.subheader("SWOT Comparison")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{company_name} SWOT**")
            st.markdown(st.session_state.swot)
        with col2:
            st.markdown(f"**{comp_name} SWOT**")
            st.markdown(st.session_state.comp_swot)

    with tab6:
        st.markdown("### ⚠️ Risk Analysis")
        risks = st.session_state.risks
        if isinstance(risks, dict) and 'error' not in risks:
            for category, data in risks.items():
                st.subheader(category)
                st.write(f"- **{data['summary']}** (Severity: {data['severity']})")
        else:
            st.warning("Risk parsing failed. Showing raw output:")
            st.text(risks.get("raw", "No data."))

    with tab7:
        st.markdown("### 📊 SWOT Radar Chart")

        swot_text = st.session_state.swot
        categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
        values = [
            swot_text.lower().count("strength"),
            swot_text.lower().count("weakness"),
            swot_text.lower().count("opportunit"),
            swot_text.lower().count("threat")
        ]

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='SWOT Intensity'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(values) + 2])
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab8:
        st.markdown("### 📉 Risk Radar Chart")
        risks = st.session_state.risks
        if isinstance(risks, dict) and 'error' not in risks:
            radar_categories = list(risks.keys())
            severity_scores = [risks[cat]['score'] for cat in radar_categories]

            fig = go.Figure(data=go.Scatterpolar(
                r=severity_scores,
                theta=radar_categories,
                fill='toself',
                name='Risk Severity'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(severity_scores) + 2])
                ),
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Radar chart not available due to parsing issue.")

    with tab9:
        st.markdown("### 📈 Stock Trend Chart")

        st.info("You can enter the stock ticker manually or use the company name if it's publicly traded.")
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, GOOG)", value="AAPL")
        period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=2)

        if ticker:
            fig = plot_stock_chart(ticker)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Could not retrieve stock data. Try another ticker.")

else:
    st.info("👈 Enter a company and competitor URL, then click 'Analyze'.")
