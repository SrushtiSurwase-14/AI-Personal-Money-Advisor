def simulate_savings(data, reduction_percent):
    """Simulate potential yearly savings if expenses are reduced"""
    income = float(data["income"])
    expenses = sum([
        float(data["rent"]),
        float(data["groceries"]),
        float(data["travel"]),
        float(data["food_delivery"]),
        float(data["shopping"]),
        float(data["subscriptions"]),
        float(data["other"])
    ])
    
    total_reduction = expenses * (reduction_percent / 100)
    new_savings = income - (expenses - total_reduction)
    yearly_savings = new_savings * 12
    
    return round(yearly_savings, 2)

def predict_financial_health(savings_rate):
    """Predict overall financial health based on savings rate"""
    if savings_rate >= 30:
        return "Excellent - You're building wealth faster than most"
    elif savings_rate >= 20:
        return "Good - On track for financial stability"
    elif savings_rate >= 10:
        return "Fair - Could improve significantly"
    else:
        return "Poor - Need immediate lifestyle changes"
