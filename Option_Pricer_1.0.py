import streamlit as st
import numpy as np
from scipy.stats import norm

# This sets the browser tab title and icon
st.set_page_config(page_title="My Option Pricer", page_icon="📈")


tab1, tab2, tab3 = st.tabs(["Homepage", "Option Pricer", "Formulas & Variables"])

with tab1:
    st.title("Option Pricer by Dominik Wicik")

    st.write("""Welcome to my Option Pricer. The goal of this project is to
        showcase my ability to handle Python programming.
        The interface is supported by the streamlit library. The calculations
        are based on the Black-Scholes-Merton model.""")

with tab2:
    st.title("Option Pricer")

    col1, col2, col3 = st.columns(3)

    with col1:
        s = st.number_input("Asset Price ($S$)", min_value=0.01, value=100.0, step=1.0)
        #q = st.number_input("Dividend yield ($q$)", value=0.05, step=0.005)
        q = st.number_input("Dividend Yield (q)", 
                    value=0.00, 
                    step=0.01, 
                    format="%.4f")

    with col2:
        k = st.number_input("Strike Price ($K$)", min_value=0.01, value=100.0, step=1.0)
        sigma = st.number_input("Volatility ($\sigma$)", min_value=0.01, value=0.2, step=0.01)
        
        
    with col3:
        #r = st.number_input("Risk-Free Rate ($r$)", min_value=0.0001, value=0.05, step=0.005)
        r = st.number_input("Risk-Free Rate (r)",
                    value=0.0575, 
                    step=0.01, 
                    format="%.4f")
        t = float(st.number_input("Time to expiration ($T$)", min_value=0.0001, value=0.5, step=0.5))

    def calculate_bsm(s, k, r, q, sigma, t):

        d1 = (np.log(s/k) + (r - q + sigma**2/2)*t)/(sigma*np.sqrt(t))
        
        d2 = d1 - sigma*np.sqrt(t)

        c = s * np.exp(-q*t) * norm.cdf(d1) - k * np.exp(-r*t) * norm.cdf(d2)

        p = k * np.exp(-r*t) * norm.cdf(-d2) - s * np.exp(-q*t) * norm.cdf(-d1)

        return d1, d2, c, p
    
    d1, d2, c, p = calculate_bsm(s, k, r, q, sigma, t)

    st.subheader("Final Option Prices")
    col1, col2 = st.columns(2)
    col1.metric("Call Value", f"${c:.2f}")
    col2.metric("Put Value", f"${p:.2f}")



with tab3:
    st.title("Formulas & Variables")
    st.write("""Here you can find all of the formulas and variables used in the
                Black-Scholes-Merton model, as well as brief descriptions.""")
    
    st.markdown("---")
    st.subheader(r"$d_1$ parameter")
    st.write(r"""$d_1$ parameter is necessary to calculate call premium (C)
                and put premium (P) later on.""")
    st.latex(r'''
    d_1 = \frac{\ln\left(\frac{S}{K}\right)+\left(r-q+\frac{\sigma^2}{2}\right)T}{\sigma\sqrt{T}}
    ''')

    st.markdown("---")
    st.subheader(r"$d_2$ parameter")
    st.write(r"""$d_2$ parameter is also required to later calculate call premium (C)
                and put premium (P).""")
    st.latex(r'''
    d_2 = d_1 - \sigma\sqrt{T}
    ''')

    st.markdown("---")
    st.subheader(r"Call premium ($C$)")
    st.write("Call premium is the price of a call option.")
    st.latex(r'''
    C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)
    ''')

    st.markdown("---")
    st.subheader(r"Put premium ($P$)")
    st.write("Put premium is the price of a call option.")
    st.latex(r'''
    P = K e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)
    ''')

    st.markdown("---")
    st.header("Variables")
    st.write(r"$S$ - spot price of the option's underlying asset.")
    st.write(r"""$K$ - strike price/exercise price. It is the price at which the
                underlying asset of the option can be bought (call option) or
                sold (put option).""")
    st.write(r"""$r$ - risk-free rate. It is a theoretical rate of return on an investment
                with no risk of financial loss. Obviously, in the real world every investment
                comes with risk in some amount, but generally government treasury bonds
                are considered to have "risk-free" interest rates, and thus, are used
                in the Black-Scholes-Merton model.""")
    st.write(r"""$q$ - continuously compounded dividend yield.""")
    st.write(r"""$\sigma$ - standard deviation of the underlying asset's returns.""")
    st.write(r"""$T$ - time until expiration of the option (expressed in years). After this time
                passes, the option holder must decide whether to exercise the option or not.""")
    st.write(r"""$N(x)$ - value of the cumulative distribution function of the standard
                normal distribution.""")
    