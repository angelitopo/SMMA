# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import threading
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# ================== Data Handling ================== #

# Path to the data file
DATA_FILE = 'data.json'

# Lock for thread-safe file operations
lock = threading.Lock()

# Function to load data from the JSON file
def load_data():
    with lock:
        if not os.path.exists(DATA_FILE):
            # Initialize with default structure if file doesn't exist
            default_data = {
                "strategic_objectives": {
                    "Biga": [
                        "Create 3 trend videos",
                        "Post two pictures and story posts",
                        "Conduct twice polls (e.g., favorite drink, duel between plates)"
                    ],
                    "Tricolor": [
                        "Create 3 trend videos focusing on food",
                        "Post two pictures and story posts",
                        "Conduct twice polls (e.g., favorite arepa)"
                    ]
                },
                "content_ideas": {
                    "Biga": [
                        {"idea": "On and off coffee video", "category": "Reels"},
                        {"idea": "Do you work here", "category": "Trendy Posts"},
                        {"idea": "Enjoy you too video", "category": "Reels"},
                        {"idea": "ASMR video", "category": "Carousels"},
                        {"idea": "Ghost pour over", "category": "Reels"},
                        {"idea": "Zombie mask video", "category": "Reels"}
                    ],
                    "Tricolor": [
                        {"idea": "Colombian beverage try for people in the street", "category": "Reels"},
                        {"idea": "Empanada try three types", "category": "Carousels"},
                        {"idea": "Which type are you poll", "category": "Polls"},
                        {"idea": "Mystery empanada", "category": "Trendy Posts"},
                        {"idea": "Arepa reaction", "category": "Reels"},
                        {"idea": "Word of the week: Colombian slang", "category": "Trendy Posts"},
                        {"idea": "Trick or Treat", "category": "Reels"}
                    ]
                },
                "weekly_goals": {
                    "Biga": [],
                    "Tricolor": []
                },
                "captions": {
                    "Biga": [],
                    "Tricolor": []
                },
                "notes": {
                    "Biga": [],
                    "Tricolor": []
                },
                "analytics": {
                    "Biga": {"views": 0, "engagement": 0, "likes": 0},
                    "Tricolor": {"views": 0, "engagement": 0, "likes": 0}
                },
                "pricing": {
                    "Biga": {"amount": 0, "due_date": ""},
                    "Tricolor": {"amount": 0, "due_date": ""}
                },
                "goals": {
                    "Biga": {"Views": 10000, "Engagements": 500, "Likes": 1000},
                    "Tricolor": {"Views": 8000, "Engagements": 400, "Likes": 800}
                }
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(default_data, f, indent=4)
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        # Ensure 'goals' section exists
        if 'goals' not in data:
            data['goals'] = {
                "Biga": {"Views": 10000, "Engagements": 500, "Likes": 1000},
                "Tricolor": {"Views": 8000, "Engagements": 400, "Likes": 800}
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)

        # Ensure each client has goals
        for client in ["Biga", "Tricolor"]:
            if client not in data['goals']:
                data['goals'][client] = {
                    "Views": 10000, "Engagements": 500, "Likes": 1000
                } if client == "Biga" else {
                    "Views": 8000, "Engagements": 400, "Likes": 800
                }
        return data

# Function to save data to the JSON file
def save_data(data):
    with lock:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

# ================== Routes ================== #

@app.route('/')
def home():
    return redirect(url_for('strategic_objectives'))

@app.route('/strategic_objectives', methods=['GET', 'POST'])
def strategic_objectives():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    if request.method == 'POST':
        client = request.form.get('client')
        objective = request.form.get('objective')
        if objective:
            data['strategic_objectives'][client].append(objective)
            save_data(data)
            flash("Objective added!", "success")
            return redirect(url_for('strategic_objectives'))
        else:
            flash("Please enter an objective.", "warning")
    return render_template('strategic_objectives.html', data=data['strategic_objectives'], clients=clients)

@app.route('/content_ideas', methods=['GET', 'POST'])
def content_ideas():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    categories = ["Trendy Posts", "Carousels", "Reels", "Polls"]
    if request.method == 'POST':
        client = request.form.get('client')
        idea = request.form.get('idea')
        category = request.form.get('category')
        if idea and category:
            data['content_ideas'][client].append({'idea': idea, 'category': category})
            save_data(data)
            flash("Content idea added!", "success")
            return redirect(url_for('content_ideas'))
        else:
            flash("Please enter a content idea and select a category.", "warning")
    return render_template('content_ideas.html', data=data['content_ideas'], clients=clients, categories=categories)

@app.route('/weekly_goals', methods=['GET', 'POST'])
def weekly_goals():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    if request.method == 'POST':
        client = request.form.get('client')
        goal = request.form.get('goal')
        if goal:
            data['weekly_goals'][client].append(goal)
            save_data(data)
            flash("Goal added!", "success")
            return redirect(url_for('weekly_goals'))
        else:
            flash("Please enter a goal.", "warning")
    return render_template('weekly_goals.html', data=data['weekly_goals'], clients=clients)

@app.route('/captions', methods=['GET', 'POST'])
def captions():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    if request.method == 'POST':
        client = request.form.get('client')
        caption = request.form.get('caption')
        if caption:
            data['captions'][client].append(caption)
            save_data(data)
            flash("Caption added!", "success")
            return redirect(url_for('captions'))
        else:
            flash("Please enter a caption.", "warning")
    return render_template('captions.html', data=data['captions'], clients=clients)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    if request.method == 'POST':
        client = request.form.get('client')
        note = request.form.get('note')
        if note:
            data['notes'][client].append(note)
            save_data(data)
            flash("Note added!", "success")
            return redirect(url_for('notes'))
        else:
            flash("Please enter a note.", "warning")
    return render_template('notes.html', data=data['notes'], clients=clients)

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    selected_client = request.args.get('client', 'Biga')
    if request.method == 'POST':
        selected_client = request.form.get('client')
        views = request.form.get('views')
        engagements = request.form.get('engagements')
        likes = request.form.get('likes')
        try:
            views = int(views) if views else 0
            engagements = int(engagements) if engagements else 0
            likes = int(likes) if likes else 0
            data['analytics'][selected_client]['views'] += views
            data['analytics'][selected_client]['engagement'] += engagements
            data['analytics'][selected_client]['likes'] += likes
            save_data(data)
            flash("Analytics updated!", "success")
            return redirect(url_for('analytics', client=selected_client))
        except ValueError:
            flash("Please enter valid numbers.", "warning")
    # Generate plot
    client_data = data['analytics'][selected_client]
    goals = data['goals'][selected_client]
    metrics = ["Views", "Engagements", "Likes"]
    current_values = [client_data['views'], client_data['engagement'], client_data['likes']]
    goal_values = [goals['Views'], goals['Engagements'], goals['Likes']]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(metrics))

    bars1 = ax.bar([i - bar_width/2 for i in x], current_values, bar_width, label='Current', color='skyblue')
    bars2 = ax.bar([i + bar_width/2 for i in x], goal_values, bar_width, label='Goal', color='lightgreen')

    ax.set_xlabel('Metrics')
    ax.set_ylabel('Count')
    ax.set_title(f'Current Metrics vs Goals for {selected_client}')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()

    # Adding value labels on top of bars
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    # Save plot to a PNG in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)

    return render_template('analytics.html',
                           data=data['analytics'],
                           goals=data['goals'],
                           clients=clients,
                           selected_client=selected_client,
                           plot_image=image_base64)

@app.route('/pricing_billing', methods=['GET', 'POST'])
def pricing_billing():
    data = load_data()
    clients = ["Biga", "Tricolor"]
    if request.method == 'POST':
        client = request.form.get('client')
        amount = request.form.get('amount')
        try:
            amount = float(amount)
            data['pricing'][client]['amount'] = amount
            # Set due date as the 30th of the next month
            today = datetime.today()
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=30)
            else:
                next_month = today.replace(month=today.month + 1, day=30)
            due_date = next_month.strftime("%d/%m/%Y")
            data['pricing'][client]['due_date'] = due_date
            save_data(data)
            flash(f"Pricing set! Billing Date: {due_date}", "success")
            return redirect(url_for('pricing_billing'))
        except ValueError:
            flash("Please enter a valid amount.", "warning")
    return render_template('pricing_billing.html', data=data['pricing'], clients=clients)

# ================== Footer ================== #

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# ================== Run the App ================== #

if __name__ == '__main__':
    app.run(debug=True)
