# ==========================================
# PORTFOLIO RISK ANALYSIS
# ==========================================


# ==========================================
# 1. FUNCTION - CALCULATE RETURNS
# ==========================================

def calculate_returns(prices):

    returns = []

    for i in range(1, len(prices)):
        return_value = (prices[i] - prices[i - 1]) / prices[i - 1]
        returns.append(return_value)

    return returns


# ==========================================
# 2. FUNCTION - CALCULATE AVERAGE RETURN
# ==========================================

def calculate_average_return(returns):

    average_return = sum(returns) / len(returns)

    return average_return


# ==========================================
# 3. FUNCTION - CALCULATE VARIANCE
# ==========================================

def calculate_variance(returns, average_return):

    squared_deviations = []

    for r in returns:

        deviation = r - average_return

        squared_deviation = deviation ** 2

        squared_deviations.append(squared_deviation)

    variance = sum(squared_deviations) / len(returns)

    return variance


# ==========================================
# 4. FUNCTION - CALCULATE VOLATILITY
# ==========================================

def calculate_volatility(variance):

    volatility = variance ** 0.5

    return volatility


# ==========================================
# 5. STOCK A - PRICE DATA
# ==========================================

prices_a = [100, 102, 101, 105, 103]

returns_a = calculate_returns(prices_a)

average_return_a = calculate_average_return(returns_a)

variance_a = calculate_variance(
    returns_a,
    average_return_a)

volatility_a = calculate_volatility(variance_a)


# ==========================================
# 6. STOCK B - PRICE DATA
# ==========================================

prices_b = [200, 204, 202, 208, 206]

returns_b = calculate_returns(prices_b)

average_return_b = calculate_average_return(returns_b)

variance_b = calculate_variance(
    returns_b,
    average_return_b)

volatility_b = calculate_volatility(variance_b)


# ==========================================
# 7. COVARIANCE
# ==========================================

covariance_products = []

for i in range(len(returns_a)):

    deviation_a = returns_a[i] - average_return_a

    deviation_b = returns_b[i] - average_return_b

    product = deviation_a * deviation_b

    covariance_products.append(product)

covariance = sum(covariance_products) / len(covariance_products)


# ==========================================
# 8. CORRELATION
# ==========================================

correlation = covariance / (volatility_a * volatility_b)


# ==========================================
# 9. PORTFOLIO WEIGHTS
# ==========================================

weight_a = 0.60
weight_b = 0.40


# ==========================================
# 10. PORTFOLIO RETURN
# ==========================================

portfolio_return = (
    weight_a * average_return_a
    + weight_b * average_return_b)


# ==========================================
# 11. PORTFOLIO VARIANCE
# ==========================================

term_a = (weight_a ** 2) * variance_a

term_b = (weight_b ** 2) * variance_b

term_c = 2 * weight_a * weight_b * covariance

portfolio_variance = term_a + term_b + term_c


# ==========================================
# 12. PORTFOLIO VOLATILITY
# ==========================================

portfolio_volatility = portfolio_variance ** 0.5


# ==========================================
# 13. VALUE AT RISK (VaR)
# ==========================================

portfolio_value = 100000


# 95% VaR

z_score_95 = 1.645

var_95 = (
    portfolio_value
    * z_score_95
    * portfolio_volatility)


# 99% VaR

z_score_99 = 2.326

var_99 = (
    portfolio_value
    * z_score_99
    * portfolio_volatility)


# ==========================================
# 14. FUNCTION - CALCULATE DRAWDOWN
# ==========================================

def calculate_drawdown(prices):

    peaks = []

    current_peak = prices[0]

    for price in prices:

        if price > current_peak:
            current_peak = price

        peaks.append(current_peak)


    drawdowns = []

    for i in range(len(prices)):

        drawdown = (
            (prices[i] - peaks[i])
            / peaks[i]
        )

        drawdowns.append(drawdown)


    current_drawdown = drawdowns[-1]

    maximum_drawdown = min(drawdowns)


    return drawdowns, current_drawdown, maximum_drawdown


# ==========================================
# 15. STOCK A - DRAWDOWN
# ==========================================

drawdowns_a, current_drawdown_a, max_drawdown_a = calculate_drawdown(
    prices_a)


# ==========================================
# 16. STOCK B - DRAWDOWN
# ==========================================

drawdowns_b, current_drawdown_b, max_drawdown_b = calculate_drawdown(
    prices_b)



# ==========================================
# 17. FINAL OUTPUT
# ==========================================

print("\n==========================================")
print("       PORTFOLIO RISK ANALYSIS")
print("==========================================")


print("\nSTOCK A")
print("------------------------------------------")

print(
    "Average Return       :",
    round(average_return_a * 100, 2), "%")


print(
    "Volatility           :",
    round(volatility_a * 100, 2),"%")

print(
    "Current Drawdown     :",
    round(current_drawdown_a * 100, 2), "%")

print(
    "Maximum Drawdown     :",
    round(max_drawdown_a * 100, 2), "%")


print("\nSTOCK B")
print("------------------------------------------")

print(
    "Average Return       :",
    round(average_return_b * 100, 2), "%")

print(
    "Volatility           :",
    round(volatility_b * 100, 2), "%")

print(
    "Current Drawdown     :",
    round(current_drawdown_b * 100, 2), "%")

print("Maximum Drawdown     :"
      ,round(max_drawdown_b * 100, 2), "%")


print("\nPORTFOLIO")
print("------------------------------------------")

print(
    "Portfolio Return     :",
    round(portfolio_return * 100, 2),
    "%"
)

print(
    "Portfolio Volatility :",
    round(portfolio_volatility * 100, 2),
    "%"
)

print(
    "95% VaR              : ₹",
    round(var_95, 2)
)

print(
    "99% VaR              : ₹",
    round(var_99, 2)
)

print("==========================================")