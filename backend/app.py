from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analysis import analyze_data, get_category_tips
from database import init_db, save_analysis, get_history, save_goal, get_goals, delete_goal, update_goal_amount
from prediction import simulate_savings, predict_financial_health
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
init_db()

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = analyze_data(data)
    return jsonify(result)

@app.route("/save_analysis", methods=["POST"])
def save_analysis_route():
    """Save analysis to history"""
    data = request.json
    try:
        save_analysis(data)
        return jsonify({"success": True, "message": "Analysis saved to history"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/history", methods=["GET"])
def history():
    """Get analysis history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        data = get_history(limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/simulate", methods=["POST"])
def simulate():
    """Simulate expense reduction scenarios"""
    data = request.json
    reduction_percent = data.get("reduction_percent", 10)
    
    try:
        # Use prediction.py functions
        yearly_savings = simulate_savings(data.get("current_data", {}), reduction_percent)
        financial_health = predict_financial_health(data.get("savings_rate", 0))
        
        return jsonify({
            "yearly_savings": yearly_savings,
            "financial_health": financial_health,
            "reduction_percent": reduction_percent
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/category_tips", methods=["POST"])
def category_tips():
    """Get category-specific tips"""
    data = request.json
    try:
        tips = get_category_tips(data)
        return jsonify(tips)
    except Exception as e:
        return jsonify({"error": str(e)})

# --- AI Chat Advisor ---

@app.route("/chat_advisor", methods=["POST"])
def chat_advisor():
    """Interactive financial chat advisor (Simplified Logic)"""
    data = request.json
    query = data.get("query", "").lower()
    expenses = data.get("expenses", {})
    health_score = data.get("health_score", 0)
    
    response = ""
    
    if "save" in query or "saving" in query:
        response = "To save more, I recommend focusing on your largest variable expenses. For most users, reducing 'Food Delivery' or 'Shopping' by 20% can increase monthly savings significantly!"
    elif "budget" in query:
        response = "A common rule is the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Looking at your data, we can see how close you are to this target."
    elif "hello" in query or "hi" in query:
        response = "Hello! I am your AI Financial Advisor. How can I help you improve your money management today?"
    elif "invest" in query:
        response = "Before investing, ensure you have an emergency fund covering 3-6 months of expenses. Once that's ready, consider low-cost index funds."
    else:
        response = "That's a great question! Based on your current financial health score of " + str(health_score) + "/100, I suggest reviewing your 'Other' expenses to find hidden leaks."
    
    return jsonify({"response": response})

# --- Goal Management Routes ---

@app.route("/save_goal", methods=["POST"])
def add_goal():
    """Add a new financial goal"""
    data = request.json
    try:
        save_goal(data.get("name"), data.get("target_amount"), data.get("current_amount", 0))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_goals", methods=["GET"])
def list_goals():
    """Link all goals"""
    try:
        goals = get_goals()
        return jsonify(goals)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/update_goal", methods=["POST"])
def edit_goal():
    """Update goal progress"""
    data = request.json
    try:
        update_goal_amount(data.get("id"), data.get("amount"))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/delete_goal/<int:goal_id>", methods=["DELETE"])
def remove_goal(goal_id):
    """Delete a goal"""
    try:
        delete_goal(goal_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
