import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            rent REAL,
            groceries REAL,
            travel REAL,
            food_delivery REAL,
            shopping REAL,
            subscriptions REAL,
            other REAL
        )
    """)
    
    # Create history table for tracking analyses over time
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            income REAL,
            total_expense REAL,
            savings REAL,
            savings_rate REAL,
            health_score REAL,
            behavior TEXT,
            rent REAL,
            groceries REAL,
            travel REAL,
            food_delivery REAL,
            shopping REAL,
            subscriptions REAL,
            other REAL
        )
    """)

    # Create goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            target_amount REAL,
            current_amount REAL,
            date_created TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def save_analysis(data):
    """Save analysis to history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO analysis_history (
            date, income, total_expense, savings, savings_rate, 
            health_score, behavior, rent, groceries, travel,
            food_delivery, shopping, subscriptions, other
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("income"),
        data.get("total_expense"),
        data.get("savings"),
        data.get("savings_rate"),
        data.get("health_score"),
        data.get("behavior"),
        data.get("expenses", {}).get("Rent", 0),
        data.get("expenses", {}).get("Groceries", 0),
        data.get("expenses", {}).get("Travel", 0),
        data.get("expenses", {}).get("Food Delivery", 0),
        data.get("expenses", {}).get("Shopping", 0),
        data.get("expenses", {}).get("Subscriptions", 0),
        data.get("expenses", {}).get("Other", 0)
    ))
    
    conn.commit()
    conn.close()
    return True

def get_history(limit=10):
    """Get analysis history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, income, total_expense, savings, savings_rate, 
               health_score, behavior, rent, groceries, travel,
               food_delivery, shopping, subscriptions, other
        FROM analysis_history 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "date": row[0],
            "income": row[1],
            "total_expense": row[2],
            "savings": row[3],
            "savings_rate": row[4],
            "health_score": row[5],
            "behavior": row[6],
            "expenses": {
                "Rent": row[7],
                "Groceries": row[8],
                "Travel": row[9],
                "Food Delivery": row[10],
                "Shopping": row[11],
                "Subscriptions": row[12],
                "Other": row[13]
            }
        })
    
    return history

def clear_history():
    """Clear all history (optional feature)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history")
    conn.commit()
    conn.close()

# --- Goal Management Functions ---

def save_goal(name, target_amount, current_amount=0):
    """Save a new financial goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (name, target_amount, current_amount, date_created)
        VALUES (?, ?, ?, ?)
    """, (name, target_amount, current_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return True

def get_goals():
    """Retrieve all financial goals"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, target_amount, current_amount, date_created FROM goals")
    rows = cursor.fetchall()
    conn.close()
    
    goals = []
    for row in rows:
        goals.append({
            "id": row[0],
            "name": row[1],
            "target_amount": row[2],
            "current_amount": row[3],
            "date_created": row[4]
        })
    return goals

def update_goal_amount(goal_id, amount):
    """Update current saved amount for a goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE goals SET current_amount = ? WHERE id = ?", (amount, goal_id))
    conn.commit()
    conn.close()
    return True

def delete_goal(goal_id):
    """Remove a financial goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
    return True
