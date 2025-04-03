from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

BUDGET_FILE = "budget_data.json"

def load_budget_data():
    if os.path.exists(BUDGET_FILE):
        try:
            with open(BUDGET_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {"budget": 0, "expenses": []}  
        except Exception as e:
            print(f"Error loading budget data: {e}")
            return {"budget": 0, "expenses": []}
    return {"budget": 0, "expenses": []}

def save_budget_data(data):
    try:
        with open(BUDGET_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving budget data: {e}")

@app.route("/")
def index():
    data = load_budget_data()
    # Calculation
    total_expenses = sum(expense['amount'] for expense in data["expenses"])
    remaining_budget = data["budget"] - total_expenses
    return render_template("index.html", budget=data["budget"], expenses=data["expenses"], remaining_budget=remaining_budget)

@app.route("/set_budget", methods=["POST"])
def set_budget():
    data = load_budget_data()
    new_budget = float(request.form.get("budget", 0))
    data["budget"] = new_budget
    save_budget_data(data)
    return jsonify({"success": True, "budget": new_budget})

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = load_budget_data()
    description = request.form.get("description", "")
    amount = float(request.form.get("amount", 0))
    
    if description and amount > 0:
        data["expenses"].append({"description": description, "amount": amount})
        save_budget_data(data)
    
    total_expenses = sum(expense['amount'] for expense in data["expenses"])
    remaining_budget = data["budget"] - total_expenses
    return jsonify({"success": True, "expenses": data["expenses"], "remaining_budget": remaining_budget})

@app.route("/reset", methods=["POST"])
def reset():
    data = {"budget": 0, "expenses": []}
    save_budget_data(data)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
