# ==========================================
# PORTFOLIO RISK ANALYSIS
# Real Market Data
# ==========================================

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# ==========================================
# 1. DATA COLLECTION
# ==========================================

stock_a = yf.download(
    "HDFCBANK.NS",
    period="1y",
    auto_adjust=True,
    progress=False
)

stock_b = yf.download(
    "RELIANCE.NS",
    period="1y",
    auto_adjust=True,
    progress=False
)


# Extract adjusted closing prices

prices_a = stock_a["Close"].squeeze()
prices_b = stock_b["Close"].squeeze()


# ==========================================
# 2. RETURN ANALYSIS
# ==========================================

def calculate_returns(prices):
    """Calculate daily percentage returns."""

    returns = prices.pct_change().dropna()

    return returns


returns_a = calculate_returns(prices_a)
returns_b = calculate_returns(prices_b)


# ==========================================
# 3. ALIGN RETURNS BY TRADING DATE
# ==========================================

returns_data = returns_a.to_frame(name="HDFC_Bank")
returns_data["Reliance"] = returns_b

returns_data = returns_data.dropna()

returns_a = returns_data["HDFC_Bank"]
returns_b = returns_data["Reliance"]


# ==========================================
# 4. AVERAGE RETURN
# ==========================================

def calculate_average_return(returns):
    """Calculate the average daily return."""

    average_return = returns.mean()

    return average_return


average_return_a = calculate_average_return(returns_a)
average_return_b = calculate_average_return(returns_b)


# ==========================================
# 5. SAMPLE VARIANCE
# ==========================================

def calculate_variance(returns, average_return):
    """Calculate sample variance of returns."""

    squared_deviations = []

    for r in returns:

        deviation = r - average_return

        squared_deviation = deviation ** 2

        squared_deviations.append(squared_deviation)

    variance = sum(squared_deviations) / (len(returns) - 1)

    return variance


variance_a = calculate_variance(
    returns_a,
    average_return_a
)

variance_b = calculate_variance(
    returns_b,
    average_return_b
)


# ==========================================
# 6. VOLATILITY
# ==========================================

def calculate_volatility(variance):
    """Calculate volatility as the square root of variance."""

    volatility = variance ** 0.5

    return volatility


volatility_a = calculate_volatility(variance_a)
volatility_b = calculate_volatility(variance_b)


# ==========================================
# 7. SAMPLE COVARIANCE
# ==========================================

def calculate_covariance(
    returns_a,
    returns_b,
    average_return_a,
    average_return_b
):
    """Calculate sample covariance between two assets."""

    covariance_products = []

    for i in range(len(returns_a)):

        deviation_a = returns_a.iloc[i] - average_return_a
        deviation_b = returns_b.iloc[i] - average_return_b

        product = deviation_a * deviation_b

        covariance_products.append(product)

    covariance = sum(covariance_products) / (len(returns_a) - 1)

    return covariance


covariance = calculate_covariance(
    returns_a,
    returns_b,
    average_return_a,
    average_return_b
)


# ==========================================
# 8. CORRELATION
# ==========================================

def calculate_correlation(
    covariance,
    volatility_a,
    volatility_b
):
    """Calculate correlation between two assets."""

    correlation = covariance / (
        volatility_a * volatility_b
    )

    return correlation


correlation = calculate_correlation(
    covariance,
    volatility_a,
    volatility_b
)


# ==========================================
# 9. PORTFOLIO WEIGHTS
# ==========================================

weight_a = 0.60
weight_b = 0.40


# ==========================================
# 10. PORTFOLIO RETURN
# ==========================================

def calculate_portfolio_return(
    weight_a,
    weight_b,
    average_return_a,
    average_return_b
):
    """Calculate weighted portfolio return."""

    portfolio_return = (
        weight_a * average_return_a
        + weight_b * average_return_b
    )

    return portfolio_return


portfolio_return = calculate_portfolio_return(
    weight_a,
    weight_b,
    average_return_a,
    average_return_b
)


# ==========================================
# 11. PORTFOLIO VARIANCE
# ==========================================

def calculate_portfolio_variance(
    weight_a,
    weight_b,
    variance_a,
    variance_b,
    covariance
):
    """Calculate portfolio variance."""

    term_a = (weight_a ** 2) * variance_a

    term_b = (weight_b ** 2) * variance_b

    term_c = 2 * weight_a * weight_b * covariance

    portfolio_variance = (
        term_a
        + term_b
        + term_c
    )

    return portfolio_variance


portfolio_variance = calculate_portfolio_variance(
    weight_a,
    weight_b,
    variance_a,
    variance_b,
    covariance
)


# ==========================================
# 12. PORTFOLIO VOLATILITY
# ==========================================

def calculate_portfolio_volatility(portfolio_variance):
    """Calculate portfolio volatility."""

    portfolio_volatility = portfolio_variance ** 0.5

    return portfolio_volatility


portfolio_volatility = calculate_portfolio_volatility(
    portfolio_variance
)


# ==========================================
# 13. PORTFOLIO VaR
# ==========================================

portfolio_value = 100000


def calculate_var(
    portfolio_value,
    z_score,
    portfolio_volatility
):
    """Calculate one-day parametric VaR."""

    var = (
        portfolio_value
        * z_score
        * portfolio_volatility
    )

    return var


z_score_95 = 1.645
z_score_99 = 2.326


var_95 = calculate_var(
    portfolio_value,
    z_score_95,
    portfolio_volatility
)

var_99 = calculate_var(
    portfolio_value,
    z_score_99,
    portfolio_volatility
)
# ==========================================
# 14. DRAWDOWN ANALYSIS
# ==========================================

def calculate_drawdown(prices):
    """Calculate drawdown series, current drawdown and maximum drawdown."""

    peaks = []
    current_peak = prices.iloc[0]

    for price in prices:

        if price > current_peak:
            current_peak = price

        peaks.append(current_peak)

    drawdowns = []

    for i in range(len(prices)):

        drawdown = (
            (prices.iloc[i] - peaks[i])
            / peaks[i]
        )

        drawdowns.append(drawdown)

    current_drawdown = drawdowns[-1]
    maximum_drawdown = min(drawdowns)

    return drawdowns, current_drawdown, maximum_drawdown

drawdowns_a, current_drawdown_a, maximum_drawdown_a = calculate_drawdown(
    prices_a
)

drawdowns_b, current_drawdown_b, maximum_drawdown_b = calculate_drawdown(
    prices_b
)

 # ==========================================
# 15.1 VISUALISATION - PRICE MOVEMENT
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    prices_a.index,
    prices_a,
    label="HDFC Bank"
)

plt.plot(
    prices_b.index,
    prices_b,
    label="Reliance"
)

plt.title("HDFC Bank vs Reliance - Historical Price Movement")
plt.xlabel("Date")
plt.ylabel("Price (₹)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("visualisations/price_movement.png", dpi=300)

plt.show()

# ==========================================
# 15.2 VISUALISATION - NORMALIZED PERFORMANCE
# ==========================================

normalized_a = (prices_a / prices_a.iloc[0]) * 100
normalized_b = (prices_b / prices_b.iloc[0]) * 100

plt.figure(figsize=(12, 6))

plt.plot(
    normalized_a.index,
    normalized_a,
    label="HDFC Bank"
)

plt.plot(
    normalized_b.index,
    normalized_b,
    label="Reliance"
)

plt.title("HDFC Bank vs Reliance - Normalized Performance")

plt.xlabel("Date")
plt.ylabel("Normalized Price (Base = 100)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("visualisations/normalized_performance.png", dpi=300)

plt.show()

# ------------------------------------------
# 15.3 DRAWDOWN VISUALISATION
# ------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    prices_a.index,
    drawdowns_a,
    label="HDFC Bank"
)

plt.plot(
    prices_b.index,
    drawdowns_b,
    label="Reliance"
)

plt.title("HDFC Bank vs Reliance - Drawdown Over Time")

plt.xlabel("Date")
plt.ylabel("Drawdown")

plt.gca().yaxis.set_major_formatter(
    mtick.PercentFormatter(1.0)
)

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("visualisations/drawdown.png", dpi=300)

plt.show()

# ==========================================
# 15.4 VISUALISATION - CORRELATION
# ==========================================

plt.figure(figsize=(8, 6))

plt.scatter(
    returns_a,
    returns_b,
    alpha=0.5
)

plt.title("HDFC Bank vs Reliance - Daily Returns")
plt.xlabel("HDFC Bank Daily Return")
plt.ylabel("Reliance Daily Return")

plt.grid(True)
plt.tight_layout()

plt.savefig("visualisations/correlation.png", dpi=300)

plt.show()

# ==========================================
# 15.5 VISUALISATION - VOLATILITY COMPARISON
# ==========================================

stocks = ["HDFC Bank", "Reliance"]
volatilities = [volatility_a, volatility_b]

plt.figure(figsize=(8, 6))

plt.bar(stocks, volatilities)

plt.title("HDFC Bank vs Reliance - Daily Volatility")
plt.xlabel("Stock")
plt.ylabel("Daily Volatility")

plt.gca().yaxis.set_major_formatter(
    mtick.PercentFormatter(1.0)
)

plt.grid(axis="y")
plt.tight_layout()

plt.savefig("visualisations/volatility.png", dpi=300)

plt.show()

# ==========================================
# 16. FINAL RESULTS
# ==========================================

print("\n==========================================")
print("       PORTFOLIO RISK ANALYSIS")
print("==========================================")

print("\n--- INDIVIDUAL STOCK METRICS ---")

print("\nHDFC BANK")
print("------------------------------------------")
print(f"Average Daily Return : {average_return_a:.4%}")
print(f"Sample Variance      : {variance_a:.10f}")
print(f"Daily Volatility     : {volatility_a:.2%}")
print(f"Current Drawdown     : {current_drawdown_a:.2%}")
print(f"Maximum Drawdown     : {maximum_drawdown_a:.2%}")

print("\nRELIANCE")
print("------------------------------------------")
print(f"Average Daily Return : {average_return_b:.4%}")
print(f"Sample Variance      : {variance_b:.10f}")
print(f"Daily Volatility     : {volatility_b:.2%}")
print(f"Current Drawdown     : {current_drawdown_b:.2%}")
print(f"Maximum Drawdown     : {maximum_drawdown_b:.2%}")

print("\n--- RELATIONSHIP BETWEEN ASSETS ---")
print("------------------------------------------")
print(f"Sample Covariance    : {covariance:.10f}")
print(f"Correlation          : {correlation:.4f}")

print("\n--- PORTFOLIO ---")
print("------------------------------------------")
print(f"HDFC Bank Weight     : {weight_a:.0%}")
print(f"Reliance Weight      : {weight_b:.0%}")
print(f"Portfolio Return     : {portfolio_return:.4%}")
print(f"Portfolio Variance   : {portfolio_variance:.10f}")
print(f"Portfolio Volatility : {portfolio_volatility:.2%}")

print("\n--- VALUE AT RISK ---")
print("------------------------------------------")
print(f"Portfolio Value      : ₹{portfolio_value:,.2f}")
print(f"1-Day 95% VaR        : ₹{var_95:,.2f}")
print(f"1-Day 99% VaR        : ₹{var_99:,.2f}")

