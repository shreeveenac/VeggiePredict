
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="VeggiePredict",
    page_icon="🥦"
)

languages = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi"
}

if "language" not in st.session_state:
    st.session_state.language = "English"

if "page" not in st.session_state:
    st.session_state.page = 1

@st.cache_data
def translate_text(text, language):
    if language == "English":
        return text
    try:
        return GoogleTranslator(
            source="en",
            target=languages[language]
        ).translate(text)
    except Exception:
        return text

def tr(text):
    return translate_text(text, st.session_state.language)

markets = [
    "Bangalore", "Mangalore", "Shivamogga",
    "Mysore", "Kolar"
]

vegetables = [
    "Onion", "Chilli", "Tomato", "Potato"
]

prices = {
    "Onion": 30,
    "Chilli": 50,
    "Tomato": 25,
    "Potato": 35
}

# PAGE 1
if st.session_state.page == 1:

    st.title(tr("🥦 VeggiePredict"))
    st.subheader(tr("Vegetable Price Prediction"))

    language = st.selectbox(
        tr("Select Language"),
        ["English", "Kannada", "Hindi"]
    )

    st.session_state.language = language

    st.subheader(tr("Welcome to VeggiePredict"))

    market = st.selectbox(
        tr("Select Market"),
        markets,
        format_func=tr
    )

    vegetable = st.selectbox(
        tr("Select Vegetable"),
        vegetables,
        format_func=tr
    )

    if st.button(tr("Continue")):
        st.session_state.market = market
        st.session_state.vegetable = vegetable
        st.session_state.page = 2
        st.rerun()

# PAGE 2
else:

    st.title(tr("🥦 VeggiePredict"))
    st.subheader(tr("Price Dashboard"))

    market = st.session_state.market
    vegetable = st.session_state.vegetable

    st.write(tr("Market") + ": " + tr(market))
    st.write(tr("Vegetable") + ": " + tr(vegetable))

    today_price = prices[vegetable]
    predicted_price = today_price + 5

    st.metric(
        tr("Today's Price"),
        f"₹{today_price}/kg"
    )

    st.metric(
        tr("Predicted Price"),
        f"₹{predicted_price}/kg"
    )

    st.subheader(tr("7-Day Price Prediction"))

    data = pd.DataFrame({
        "Day": [
            "Today", "Day 2", "Day 3", "Day 4",
            "Day 5", "Day 6", "Day 7"
        ],
        "Price": [
            today_price,
            today_price + 1,
            today_price + 2,
            today_price + 3,
            today_price + 4,
            today_price + 5,
            today_price + 5
        ]
    })

    data["Day"] = data["Day"].apply(tr)

    st.line_chart(data.set_index("Day"))

    st.table(data.rename(columns={
        "Day": tr("Day"),
        "Price": tr("Price")
    }))

    st.info(tr(
        "Note: These are sample prices, not live market prices."
    ))

    if st.button(tr("Back")):
        st.session_state.page = 1
        st.rerun()
