💎 AntiGravity Finance — AI Personal Money Advisor
Take control of your finances with AI-powered insights, smart budgeting, and personalized savings advice.

✨ Features

📊 Dashboard — Get a real-time snapshot of your financial health, savings rate, and spending breakdown
⚡ Quick Entry — Log income and expenses across categories (Rent/EMI, Groceries, Travel, Dining, Shopping, Subscriptions, Miscellaneous) in seconds
📈 Analytics — Visual breakdown of where your money goes each month
🎯 Savings Goals — Set, track, and hit your savings targets
🤖 AI Advisor — Chat with a virtual financial assistant for personalized tips and answers to questions like "How can I save more?" or "What's the 50/30/20 rule?"
🕐 Recent History — Review past transactions and spending patterns
💱 INR / USD Toggle — Switch between Indian Rupee and US Dollar display
📤 Export Report — Download your financial summary

🛠️ Tech Stack
LayerTechnologyFrontendHTML5, CSS3, JavaScript (Vanilla)BackendPython, FlaskDatabaseSQLite (database.db)AI / MLCustom prediction & analysis models (prediction.py, analysis.py)ORM / Datadatabase.py, models.py

📁 Project Structure
AI-Personal-Money-Advisor/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── database.py         # DB connection & setup
│   ├── models.py           # Data models
│   ├── analysis.py         # Spending analysis logic
│   ├── prediction.py       # AI-based financial predictions
│   ├── database.db         # SQLite database
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main app UI
│   ├── script.js           # Frontend logic & API calls
│   └── style.css           # Styling & layout
└── README.md

🚀 Getting Started
Prerequisites

Python 3.10+
pip

1. Clone the Repository
bashgit clone https://github.com/SrushtiSurwase-14/AI-Personal-Money-Advisor.git
cd AI-Personal-Money-Advisor
2. Set Up the Backend
bashcd backend
python -m venv .venv

# Windows
.venv\Scripts\activate


pip install -r requirements.txt
3. Run the Backend Server
bashpython app.py
The backend will start at http://127.0.0.1:5000
4. Open the Frontend
Just open frontend/index.html in your browser — no build step needed!
Or visit:
http://127.0.0.1:5000
if Flask is configured to serve the frontend directly.

💡 Usage

Enter your monthly income in the Quick Entry panel
Fill in your expenses across all categories
Check your Financial Health score and Savings Rate
Visit the Analytics page for spending charts
Set targets under Savings Goals
Ask the AI Advisor anything about your finances
Use Export Report to save a summary


🤖 AI Advisor Examples

"How can I save more money this month?"
"What is the 50/30/20 budgeting rule?"
"Am I spending too much on dining out?"
"How long will it take to reach my savings goal?"


🗺️ Roadmap

 User authentication & multi-user support
 Monthly comparison charts
 Email/SMS spending alerts
 Mobile-responsive redesign
 Integration with UPI / bank statement import
 Dark mode

https://github.com/SrushtiSurwase-14/AI-Personal-Money-Advisor.git

👩‍💻 Author
Srushti Surwase

GitHub: @SrushtiSurwase-14



