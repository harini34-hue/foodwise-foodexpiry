from flask import Flask, render_template, request, redirect, url_for
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, date

app = Flask(__name__)

# ============================================================
# FOOD DATA
# ============================================================

foods = [
    {
        "id": 1,
        "name": "Milk",
        "category": "Dairy",
        "purchase_date": "2026-10-01",
        "expiry_date": "2026-10-07",
        "quantity": 2
    },
    {
        "id": 2,
        "name": "Bread",
        "category": "Bakery",
        "purchase_date": "2026-10-02",
        "expiry_date": "2026-10-06",
        "quantity": 1
    },
    {
        "id": 3,
        "name": "Apples",
        "category": "Fruits",
        "purchase_date": "2026-09-28",
        "expiry_date": "2026-10-10",
        "quantity": 5
    },
    {
        "id": 4,
        "name": "Rice",
        "category": "Grains",
        "purchase_date": "2026-09-01",
        "expiry_date": "2027-02-01",
        "quantity": 5
    },
    {
        "id": 5,
        "name": "Tomatoes",
        "category": "Vegetables",
        "purchase_date": "2026-10-02",
        "expiry_date": "2026-10-08",
        "quantity": 4
    }
]

# ============================================================
# LINEAR REGRESSION MODEL
# ============================================================

X = np.array([
    [5],
    [10],
    [15],
    [20],
    [25],
    [30],
    [35]
])

y = np.array([
    14,
    12,
    10,
    8,
    6,
    4,
    2
])

model = LinearRegression()
model.fit(X, y)

SLOPE = float(model.coef_[0])
INTERCEPT = float(model.intercept_)
R2_SCORE = float(model.score(X, y))

# ============================================================
# HELPER FUNCTION
# ============================================================

def get_food_status(expiry_date):
    today = date.today()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    days_left = (expiry - today).days

    if days_left < 0:
        status = "Expired"
    elif days_left <= 3:
        status = "Expiring Soon"
    else:
        status = "Fresh"

    return days_left, status


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def home():
    total_items = len(foods)

    total_quantity = sum(
        food["quantity"]
        for food in foods
    )

    expired = 0
    expiring = 0
    fresh = 0

    for food in foods:
        days_left, status = get_food_status(food["expiry_date"])

        if status == "Expired":
            expired += 1
        elif status == "Expiring Soon":
            expiring += 1
        else:
            fresh += 1

    return render_template(
        "index.html",
        total_items=total_items,
        total_quantity=total_quantity,
        expired=expired,
        expiring=expiring,
        fresh=fresh
    )


# ============================================================
# INVENTORY
# ============================================================

@app.route("/inventory", methods=["GET", "POST"])
def inventory():

    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        purchase_date = request.form.get("purchase_date")
        expiry_date = request.form.get("expiry_date")
        quantity = request.form.get("quantity")

        if name and category and purchase_date and expiry_date and quantity:
            new_food = {
                "id": len(foods) + 1,
                "name": name,
                "category": category,
                "purchase_date": purchase_date,
                "expiry_date": expiry_date,
                "quantity": int(quantity)
            }

            foods.append(new_food)

        return redirect(url_for("inventory"))

    return render_template(
        "inventory.html",
        foods=foods
    )


# ============================================================
# EXPIRY TRACKER
# ============================================================

@app.route("/expiry")
def expiry():
    expiry_data = []

    for food in foods:
        days_left, status = get_food_status(food["expiry_date"])

        expiry_data.append({
            "name": food["name"],
            "category": food["category"],
            "expiry_date": food["expiry_date"],
            "days_left": days_left,
            "status": status
        })

    expiry_data.sort(key=lambda x: x["days_left"])

    return render_template(
        "expiry.html",
        foods=expiry_data
    )


# ============================================================
# LINEAR REGRESSION PREDICTOR
# ============================================================

@app.route("/predictor", methods=["GET", "POST"])
def predictor():
    prediction = None
    temperature = None
    prediction_message = None

    if request.method == "POST":
        try:
            temperature = float(request.form.get("temperature"))
            prediction = float(model.predict(np.array([[temperature]]))[0])
            prediction = max(0, round(prediction, 2))

            if prediction <= 3:
                prediction_message = "High temperature risk – food may have a short shelf life."
            elif prediction <= 7:
                prediction_message = "Moderate shelf life – monitor the food regularly."
            else:
                prediction_message = "Longer expected shelf life under these conditions."

        except (ValueError, TypeError):
            prediction = None
            temperature = None
            prediction_message = "Please enter a valid temperature."

    return render_template(
        "predictor.html",
        prediction=prediction,
        temperature=temperature,
        prediction_message=prediction_message
    )


# ============================================================
# WASTE MANAGEMENT
# ============================================================

@app.route("/waste")
def waste():
    total_quantity = sum(food["quantity"] for food in foods)
    estimated_waste = round(total_quantity * 0.15, 2)
    potentially_saved = round(total_quantity - estimated_waste, 2)

    return render_template(
        "waste.html",
        total_quantity=total_quantity,
        estimated_waste=estimated_waste,
        potentially_saved=potentially_saved
    )


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
def analytics():
    categories = {}

    for food in foods:
        category = food["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += food["quantity"]

    category_names = list(categories.keys())
    category_values = list(categories.values())

    return render_template(
        "analytics.html",
        categories=categories,
        category_names=category_names,
        category_values=category_values
    )


# ============================================================
# REGRESSION LAB
# ============================================================

@app.route("/regression")
def regression():
    return render_template(
        "regression.html",
        slope=round(SLOPE, 4),
        intercept=round(INTERCEPT, 4),
        r2=round(R2_SCORE, 4)
    )


# ============================================================
# FOOD SAVING TIPS
# ============================================================

@app.route("/tips")
def tips():
    tips_list = [
        {
            "title": "Follow FIFO",
            "description": "Use the food purchased first before newer food."
        },
        {
            "title": "Check Expiry Dates",
            "description": "Regularly check expiry dates to avoid unnecessary waste."
        },
        {
            "title": "Correct Storage",
            "description": "Store food at suitable temperature and humidity."
        },
        {
            "title": "Plan Meals",
            "description": "Plan meals before shopping to avoid buying excess food."
        },
        {
            "title": "Freeze Food",
            "description": "Freeze suitable food when it cannot be consumed immediately."
        },
        {
            "title": "Donate Surplus",
            "description": "Donate safe and usable surplus food instead of throwing it away."
        },
        {
            "title": "Buy Required Quantity",
            "description": "Purchase quantities according to actual household requirements."
        },
        {
            "title": "Reuse Leftovers",
            "description": "Use safe leftovers creatively in another meal."
        }
    ]

    return render_template(
        "tips.html",
        tips=tips_list
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return """
    <h1>404 - Page Not Found</h1>
    <p>The requested page does not exist.</p>
    <a href="/">Return to FoodWise</a>
    """, 404


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )