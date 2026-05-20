// --- State Management ---
let mainChart = null;
let trendChart = null;
let currentCurrency = '₹';
let currencyFactor = 1;
let currentExpenses = {};
let currentHealthScore = 0;

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboard();
    loadGoals(); // Initial Load
    initChat();
});

// --- Navigation Logic ---
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('data-section');

            // Update UI
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            sections.forEach(s => {
                s.classList.remove('active');
                if (s.id === target) s.classList.add('active');
            });

            // Trigger section-specific loads
            if (target === 'history') loadHistory();
            if (target === 'goals') loadGoals();
            if (target === 'analytics') loadAnalytics();
        });
    });
}

// --- Analysis Engine ---
async function analyze() {
    const form = document.getElementById('expenseForm');
    const btn = form.querySelector('.primary-btn');
    const scanner = document.getElementById('scanner');

    // Basic Validation
    const inputs = form.querySelectorAll('input');
    let valid = true;
    inputs.forEach(i => {
        if (!i.value) {
            i.style.borderColor = 'var(--accent)';
            valid = false;
        } else {
            i.style.borderColor = 'var(--border)';
        }
    });

    if (!valid) return;

    // Show Scanning Animation
    scanner.style.display = 'flex';
    btn.classList.add('loading');

    const data = {
        income: parseFloat(document.getElementById('income').value),
        rent: parseFloat(document.getElementById('rent').value),
        groceries: parseFloat(document.getElementById('groceries').value),
        travel: parseFloat(document.getElementById('travel').value),
        food_delivery: parseFloat(document.getElementById('food_delivery').value),
        shopping: parseFloat(document.getElementById('shopping').value),
        subscriptions: parseFloat(document.getElementById('subscriptions').value),
        other: parseFloat(document.getElementById('other').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        // Simulate "Thinking" time
        setTimeout(() => {
            scanner.style.display = 'none';
            btn.classList.remove('loading');
            
            displayDashboardResults(result);
            saveToHistory(result);
        }, 1500);

    } catch (error) {
        console.error("Analysis failed:", error);
        scanner.style.display = 'none';
        btn.classList.remove('loading');
        alert("Make sure the backend server is running!");
    }
}

function displayDashboardResults(data) {
    currentExpenses = data.expenses;
    currentHealthScore = data.health_score;

    // Update Stats
    document.getElementById('dash-health').innerText = `${data.health_score}/100`;
    document.getElementById('dash-savings-rate').innerText = `${data.savings_rate}%`;

    // Update mini-bars
    const bars = document.querySelectorAll('.mini-chart .bar');
    bars[0].style.width = `${data.health_score}%`;
    bars[1].style.width = `${data.savings_rate}%`;

    // Update Chart
    renderMainChart(data.expenses);

    // Populate Analytics Preview (hidden until switched)
    displayAdvice(data.advice, data.overspent_categories);
}

// --- Charting Logic ---
function renderMainChart(expenses) {
    const ctx = document.getElementById('main-chart').getContext('2d');
    if (mainChart) mainChart.destroy();

    mainChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(expenses),
            datasets: [{
                data: Object.values(expenses),
                backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#f43f5e', '#ec4899', '#8b5cf6', '#06b6d4'],
                borderWidth: 0,
                hoverOffset: 20
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#64748b', padding: 20, font: { size: 12 } } },
                title: { display: true, text: 'Expense Distribution', color: '#1e293b', font: { size: 16 } }
            },
            cutout: '70%',
            animation: { animateScale: true }
        }
    });
}

// --- Savings Goals Logic ---
async function loadGoals() {
    try {
        const res = await fetch('http://127.0.0.1:5000/get_goals');
        const goals = await res.json();
        const container = document.getElementById('goals-list-container');
        container.innerHTML = '';

        goals.forEach(goal => {
            const percent = Math.min(Math.round((goal.current_amount / goal.target_amount) * 100), 100);
            const card = document.createElement('div');
            card.className = 'glass-card goal-card';
            card.innerHTML = `
                <div class="goal-progress-circle" style="--percent: ${percent * 3.6}" data-percent="${percent}"></div>
                <div class="goal-info">
                    <h4>${goal.name}</h4>
                    <p>Target: ${currentCurrency}${formatNum(goal.target_amount)}</p>
                    <p>Saved: ${currentCurrency}${formatNum(goal.current_amount)}</p>
                </div>
                <div class="goal-actions">
                    <button class="export-btn" onclick="updateGoalProgress(${goal.id}, ${goal.current_amount})"><i class="fas fa-plus"></i></button>
                    <button class="export-btn" onclick="deleteGoal(${goal.id})"><i class="fas fa-trash"></i></button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (e) { console.error("Error loading goals:", e); }
}

async function addNewGoal() {
    const name = document.getElementById('goal-name').value;
    const target = document.getElementById('goal-target').value;

    if (!name || !target) return;

    await fetch('http://127.0.0.1:5000/save_goal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, target_amount: parseFloat(target) })
    });

    document.getElementById('goal-name').value = '';
    document.getElementById('goal-target').value = '';
    loadGoals();
}

async function updateGoalProgress(id, current) {
    const added = prompt("How much more did you save?");
    if (!added || isNaN(added)) return;

    await fetch('http://127.0.0.1:5000/update_goal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, amount: current + parseFloat(added) })
    });
    loadGoals();
}

async function deleteGoal(id) {
    if (!confirm("Delete this goal?")) return;
    await fetch(`http://127.0.0.1:5000/delete_goal/${id}`, { method: 'DELETE' });
    loadGoals();
}

// --- AI Advisor Chat ---
function initChat() {
    const input = document.getElementById('chat-input');
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;

    const chatBody = document.getElementById('chat-messages');
    
    // User Message
    chatBody.innerHTML += `<div class="message user">${text}</div>`;
    input.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    // AI Response
    try {
        const res = await fetch('http://127.0.0.1:5000/chat_advisor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                query: text, 
                expenses: currentExpenses, 
                health_score: currentHealthScore 
            })
        });
        const data = await res.json();
        
        setTimeout(() => {
            chatBody.innerHTML += `<div class="message ai">${data.response}</div>`;
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 600);
    } catch (e) {
        chatBody.innerHTML += `<div class="message ai">Sorry, I'm having trouble connecting right now.</div>`;
    }
}

// --- History & Analytics ---
async function loadHistory() {
    try {
        const res = await fetch('http://127.0.0.1:5000/history');
        const history = await res.json();
        const body = document.getElementById('history-body');
        body.innerHTML = '';

        history.forEach(item => {
            const healthClass = item.health_score >= 70 ? 'health-high' : item.health_score >= 40 ? 'health-mid' : 'health-low';
            const row = `
                <tr>
                    <td>${item.date.split(' ')[0]}</td>
                    <td>${currentCurrency}${formatNum(item.income)}</td>
                    <td>${currentCurrency}${formatNum(item.total_expense)}</td>
                    <td>${currentCurrency}${formatNum(item.savings)}</td>
                    <td><span class="health-badge ${healthClass}">${item.health_score}%</span></td>
                    <td><button class="export-btn" onclick="deleteHistoryItem(${item.id})"><i class="fas fa-trash"></i></button></td>
                </tr>
            `;
            body.innerHTML += row;
        });
    } catch (e) { console.error("Error loading history:", e); }
}

async function loadAnalytics() {
    const res = await fetch('http://127.0.0.1:5000/history?limit=10');
    const data = await res.json();
    renderTrendChart(data);
}

function renderTrendChart(historyData) {
    const ctx = document.getElementById('trend-chart').getContext('2d');
    if (trendChart) trendChart.destroy();

    const data = [...historyData].reverse();
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date.split(' ')[0]),
            datasets: [
                { label: 'Savings', data: data.map(d => d.savings), borderColor: '#10b981', tension: 0.4 },
                { label: 'Expenses', data: data.map(d => d.total_expense), borderColor: '#f43f5e', tension: 0.4 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#64748b' } } },
            scales: {
                x: { ticks: { color: '#64748b' } },
                y: { ticks: { color: '#64748b' } }
            }
        }
    });
}

function displayAdvice(advice, overspent) {
    const adviceList = document.getElementById('ai-advice-list');
    const overspentList = document.getElementById('overspent-list');

    adviceList.innerHTML = advice.length ? advice.map(a => `
        <div class="advice-list-item">
            <i class="fas fa-lightbulb"></i>
            <p>${a}</p>
        </div>
    `).join('') : '<div class="empty-state">No specific insights available.</div>';

    overspentList.innerHTML = Object.keys(overspent).length ? Object.entries(overspent).map(([cat, val]) => `
        <div class="advice-list-item">
            <i class="fas fa-exclamation-triangle" style="color: var(--accent)"></i>
            <p><strong>${cat}</strong>: Budget exceeded by ${currentCurrency}${formatNum(val)}</p>
        </div>
    `).join('') : '<div class="empty-state">No overspending detected! Great job.</div>';
}

// --- Utils ---
function formatNum(num) {
    return (num * currencyFactor).toLocaleString(undefined, { maximumFractionDigits: 0 });
}

function loadDashboard() {
    // Hidden empty states for charts initially
}

async function saveToHistory(data) {
    await fetch('http://127.0.0.1:5000/save_analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
}

function exportData() {
    // Simple CSV export of current analysis
    if (!currentExpenses) return alert("Run analysis first!");
    let csv = "Category,Value\n";
    Object.entries(currentExpenses).forEach(([k, v]) => csv += `${k},${v}\n`);
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'financial_report.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Currency Switcher
document.getElementById('currency-switch')?.addEventListener('change', (e) => {
    if (e.target.checked) {
        currentCurrency = '$';
        currencyFactor = 0.012; // Flat simulated rate
    } else {
        currentCurrency = '₹';
        currencyFactor = 1;
    }
    // Refresh lists if items exist
    loadGoals();
    loadHistory();
});
