def analyze_data(data):
    income = float(data["income"])

    expenses = {
        "Rent": float(data["rent"]),
        "Groceries": float(data["groceries"]),
        "Travel": float(data["travel"]),
        "Food Delivery": float(data["food_delivery"]),
        "Shopping": float(data["shopping"]),
        "Subscriptions": float(data["subscriptions"]),
        "Other": float(data["other"])
    }

    total_expense = sum(expenses.values())
    savings = income - total_expense
    
    # Prevent division by zero
    if income <= 0:
        return {"error": "Income must be greater than 0"}
    
    savings_rate = (savings / income) * 100
    advice = []
    behavior = "Balanced Spender"
    health_score = 100

    # Behavioral analysis
    if expenses["Shopping"] + expenses["Food Delivery"] > 0.30 * income:
        behavior = "Impulse Spender"
        advice.append("⚠️ Reduce lifestyle spending (Shopping & Food Delivery).")
        health_score -= 20

    if expenses["Subscriptions"] > 0.05 * income:
        advice.append("💡 Review subscriptions - you may have unused services.")
        health_score -= 10

    if expenses["Rent"] > 0.40 * income:
        advice.append("🏠 Rent is high. Consider finding affordable housing.")
        health_score -= 15

    if savings_rate < 10:
        advice.append("📊 You're spending too much. Target at least 20% savings rate.")
        health_score -= 25
    elif savings_rate >= 30:
        behavior = "Smart Saver"
        advice.append("✅ Great job! You're saving 30% or more - keep it up!")
        health_score = 100
    elif savings_rate >= 20:
        behavior = "Good Saver"
        advice.append("👍 Good savings rate! Try to push it to 30%.")
        health_score = 85

    # If negative savings
    if savings < 0:
        advice.append("❌ You're spending more than you earn. Cut expenses immediately!")
        health_score = 20

    yearly_projection = savings * 12
    
    # Overspending categories
    overspent_categories = {k: v for k, v in expenses.items() if v > 0.25 * income}

    return {
        "income": round(income, 2),
        "total_expense": round(total_expense, 2),
        "savings": round(savings, 2),
        "savings_rate": round(savings_rate, 2),
        "behavior": behavior,
        "health_score": max(0, min(100, health_score)),
        "yearly_projection": round(yearly_projection, 2),
        "expenses": expenses,
        "advice": advice,
        "overspent_categories": overspent_categories
    }

def get_category_tips(data):
    """Get detailed tips for each expense category based on spending patterns"""
    income = float(data.get("income", 0))
    expenses = {
        "Rent": float(data.get("rent", 0)),
        "Groceries": float(data.get("groceries", 0)),
        "Travel": float(data.get("travel", 0)),
        "Food Delivery": float(data.get("food_delivery", 0)),
        "Shopping": float(data.get("shopping", 0)),
        "Subscriptions": float(data.get("subscriptions", 0)),
        "Other": float(data.get("other", 0))
    }
    
    tips = {}
    
    # Rent tips
    if expenses["Rent"] > 0.40 * income:
        tips["Rent"] = {
            "status": "warning",
            "message": "Your rent exceeds 40% of income. Consider roommate options or moving to a cheaper area.",
            "potential_savings": round(expenses["Rent"] * 0.20, 2)
        }
    elif expenses["Rent"] > 0.30 * income:
        tips["Rent"] = {
            "status": "moderate",
            "message": "Rent is manageable but could be optimized. Look for deals in your area.",
            "potential_savings": round(expenses["Rent"] * 0.10, 2)
        }
    else:
        tips["Rent"] = {
            "status": "good",
            "message": "Great! Your rent is within the recommended 30% threshold.",
            "potential_savings": 0
        }
    
    # Groceries tips
    if expenses["Groceries"] > 0.15 * income:
        tips["Groceries"] = {
            "status": "warning",
            "message": "Groceries are high. Try meal planning, using coupons, or buying store brands.",
            "potential_savings": round(expenses["Groceries"] * 0.25, 2)
        }
    else:
        tips["Groceries"] = {
            "status": "good",
            "message": "Your grocery spending is well balanced.",
            "potential_savings": 0
        }
    
    # Travel tips
    if expenses["Travel"] > 0.15 * income:
        tips["Travel"] = {
            "status": "warning",
            "message": "Consider carpooling, public transit, or working from home to reduce travel costs.",
            "potential_savings": round(expenses["Travel"] * 0.30, 2)
        }
    else:
        tips["Travel"] = {
            "status": "good",
            "message": "Your travel expenses are reasonable.",
            "potential_savings": 0
        }
    
    # Food Delivery tips
    if expenses["Food Delivery"] > 0.10 * income:
        tips["Food Delivery"] = {
            "status": "warning",
            "message": "Cooking at home can save you significantly. Try meal prep on weekends!",
            "potential_savings": round(expenses["Food Delivery"] * 0.50, 2)
        }
    elif expenses["Food Delivery"] > 0.05 * income:
        tips["Food Delivery"] = {
            "status": "moderate",
            "message": "Limit food delivery to once a week to reduce costs.",
            "potential_savings": round(expenses["Food Delivery"] * 0.30, 2)
        }
    else:
        tips["Food Delivery"] = {
            "status": "good",
            "message": "Great job keeping food delivery expenses low!",
            "potential_savings": 0
        }
    
    # Shopping tips
    if expenses["Shopping"] > 0.15 * income:
        tips["Shopping"] = {
            "status": "warning",
            "message": "Try the 24-hour rule: wait a day before non-essential purchases.",
            "potential_savings": round(expenses["Shopping"] * 0.40, 2)
        }
    elif expenses["Shopping"] > 0.08 * income:
        tips["Shopping"] = {
            "status": "moderate",
            "message": "Look for sales and use cashback apps when shopping.",
            "potential_savings": round(expenses["Shopping"] * 0.20, 2)
        }
    else:
        tips["Shopping"] = {
            "status": "good",
            "message": "Your shopping habits are controlled.",
            "potential_savings": 0
        }
    
    # Subscriptions tips
    if expenses["Subscriptions"] > 0.05 * income:
        tips["Subscriptions"] = {
            "status": "warning",
            "message": "Review all subscriptions - you might have forgotten about some!",
            "potential_savings": round(expenses["Subscriptions"] * 0.50, 2)
        }
    else:
        tips["Subscriptions"] = {
            "status": "good",
            "message": "Your subscription costs are well managed.",
            "potential_savings": 0
        }
    
    # Other tips
    if expenses["Other"] > 0.10 * income:
        tips["Other"] = {
            "status": "warning",
            "message": "Track your 'Other' expenses more carefully to identify hidden costs.",
            "potential_savings": round(expenses["Other"] * 0.30, 2)
        }
    else:
        tips["Other"] = {
            "status": "good",
            "message": "Your miscellaneous expenses are reasonable.",
            "potential_savings": 0
        }
    
    return tips
