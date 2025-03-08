import numpy as np
import streamlit as st

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
        "Projected Price (Stock Up)": projected_price_up,
        "Projected Price (Stock Down)": projected_price_down,
        "Projected Price (IV Up)": projected_price_higher_iv,
        "Projected Price (IV Down)": projected_price_lower_iv,
        "Time Decay Impact": time_decay,
    }

# Streamlit UI
st.title("Options Greeks Calculator")
st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Stock Price (S)", value=500.0)
K = st.sidebar.number_input("Strike Price (K)", value=480.0)
r = st.sidebar.number_input("Risk-Free Rate (r, %)", value=5.0) / 100
T = st.sidebar.number_input("Time to Expiration (Days)", value=30) / 365
sigma = st.sidebar.number_input("Implied Volatility (IV, %)", value=50.0) / 100
delta = st.sidebar.number_input("Delta", value=0.60)
gamma = st.sidebar.number_input("Gamma", value=0.03)
theta = st.sidebar.number_input("Theta", value=-0.02)
vega = st.sidebar.number_input("Vega", value=0.10)

if st.sidebar.button("Calculate"):
    projections = option_price_projection(S, K, r, T, sigma, delta, gamma, theta, vega)
    st.subheader("Projected Option Prices")
    
    # Improved Display with Table Format
    st.write("### Option Price Projections")
    st.table({
        "Scenario": ["Stock Up", "Stock Down", "IV Up", "IV Down", "Time Decay Impact"],
        "Projected Price": [
            f"{projections['Projected Price (Stock Up)']:.2f}",
            f"{projections['Projected Price (Stock Down)']:.2f}",
            f"{projections['Projected Price (IV Up)']:.2f}",
            f"{projections['Projected Price (IV Down)']:.2f}",
            f"{projections['Time Decay Impact']:.2f}"
        ]
    })
