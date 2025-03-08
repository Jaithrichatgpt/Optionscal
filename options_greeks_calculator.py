import numpy as np
import pandas as pd
import streamlit as st

# Title of the app
st.title("Options Greeks Tracker")
st.subheader("Track Option Price Movements Based on Greeks")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

# Stock selection from memory
stocks = ["NVIDIA (NVDA)", "Super Micro Computer (SMCI)", "SoundHound AI (SOUN)"]
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

S = st.sidebar.number_input("Current Stock Price (S)", value=500.0)
K = st.sidebar.number_input("Strike Price (K)", value=480.0)
r = st.sidebar.number_input("Risk-Free Rate (r, %)", value=5.0) / 100
T = st.sidebar.number_input("Time to Expiration (Days)", value=30) / 365
sigma = st.sidebar.number_input("Implied Volatility (IV, %)", value=50.0) / 100
delta = st.sidebar.number_input("Delta", value=0.60)
gamma = st.sidebar.number_input("Gamma", value=0.03)
theta = st.sidebar.number_input("Theta", value=-0.02)
vega = st.sidebar.number_input("Vega", value=0.10)

# Function to calculate projected option prices
def option_price_projection(S, K, r, T, sigma, delta, gamma, theta, vega):
    """
    Calculate projected option price based on Greeks and market conditions.
    """
    price_change_up = delta * (S * 0.01) + 0.5 * gamma * (S * 0.01) ** 2
    price_change_down = -delta * (S * 0.01) + 0.5 * gamma * (S * 0.01) ** 2
    time_decay = theta * (1 / 365)  # One-day decay
    iv_change = vega * 0.01  # 1% IV change impact

    projected_price_up = max(0, S + price_change_up - time_decay)
    projected_price_down = max(0, S - price_change_down - time_decay)
    projected_price_higher_iv = max(0, projected_price_up + iv_change)
    projected_price_lower_iv = max(0, projected_price_down - iv_change)

    return {
        "Stock Up": projected_price_up,
        "Stock Down": projected_price_down,
        "IV Up": projected_price_higher_iv,
        "IV Down": projected_price_lower_iv,
        "Time Decay Impact": time_decay,
    }

# Calculate & Display Results
if st.sidebar.button("Calculate"):
    projections = option_price_projection(S, K, r, T, sigma, delta, gamma, theta, vega)
    st.subheader(f"Projected Option Prices for {selected_stock}")
    df = pd.DataFrame(list(projections.items()), columns=["Scenario", "Projected Price"])
    st.table(df)
