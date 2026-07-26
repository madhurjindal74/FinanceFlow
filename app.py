from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import RegisterForm, LoginForm, ExpenseForm
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3

import os

DATABASE = os.path.join(os.path.dirname(__file__), "database.db") 
print("DATABASE PATH:", DATABASE)

def get_db_connection():
    return sqlite3.connect(DATABASE)

app = Flask(__name__)
app.config["SECRET_KEY"] = "financeflow-secret-key"

@app.route("/")
def home():

    """Display the authenticated user's dashboard."""

    if session.get("user_id"):

        connection = get_db_connection()
        cursor = connection.cursor()

        # ---------------- Financial Summary ----------------

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
        """, (session["user_id"],))

        total_expenses = cursor.fetchone()[0]

        cursor.execute("""
           SELECT budget
           FROM users
           WHERE id = ?
        """, (session["user_id"],))

        budget = cursor.fetchone()[0]
        if total_expenses is None:
         total_expenses = 0
        budget_left = budget - total_expenses

# ---------------- Quick Stats ----------------

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC
        """, (session["user_id"],))

        expenses = cursor.fetchall()

        cursor.execute("""
    SELECT COUNT(*)
    FROM expenses
    WHERE user_id = ?
""", (session["user_id"],))

        transaction_count = cursor.fetchone()[0]


        cursor.execute("""
    SELECT COUNT(DISTINCT category)
    FROM expenses
    WHERE user_id = ?
""", (session["user_id"],))

        category_count = cursor.fetchone()[0]


        cursor.execute("""
    SELECT date
    FROM expenses
    WHERE user_id = ?
    ORDER BY date DESC
    LIMIT 1
""", (session["user_id"],))

        latest = cursor.fetchone()

        latest_date = latest[0] if latest else "-"

# ---------------- Charts ----------------

        cursor.execute("""
           SELECT category, SUM(amount)
           FROM expenses
           WHERE user_id = ?
           GROUP BY category
        """, (session["user_id"],))

        category_data = cursor.fetchall()

        cursor.execute("""
    SELECT date, SUM(amount)
    FROM expenses
    WHERE user_id = ?
    GROUP BY date
    ORDER BY date
""", (session["user_id"],))

        daily_data = cursor.fetchall()

        connection.close()

        if total_expenses is None:
            total_expenses = 0

            # ---------------- Render Dashboard ----------------

        return render_template(
    "dashboard.html",
    total_expenses=total_expenses,
    expenses=expenses,
    budget=budget,
    budget_left=budget_left,
    category_data=category_data,
    daily_data=daily_data,
    transaction_count=transaction_count,
    category_count=category_count,
    latest_date=latest_date,
)

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()


    if form.validate_on_submit():

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, full_name, password FROM users WHERE email = ?",
            (form.email.data,)
        )

        user = cursor.fetchone()

        connection.close()

        if user:

          if user and check_password_hash(user[2], form.password.data):
            session["user_id"] = user[0]
            session["full_name"] = user[1]

            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        connection = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users (full_name, email, password)
                VALUES (?, ?, ?)
            """, (
                form.full_name.data,
                form.email.data,
                generate_password_hash(form.password.data)
            ))

            connection.commit()
            cursor.execute(
            "SELECT id, full_name FROM users WHERE email = ?",
            (form.email.data,)
        )

            user = cursor.fetchone()

            session["user_id"] = user[0]
            session["full_name"] = user[1]
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            return "An account with this email already exists."

        finally:
            if connection:
                connection.close()

    return render_template("register.html", form=form)

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    form = ExpenseForm()

    if form.validate_on_submit():

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO expenses (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            float(form.amount.data),
            form.category.data,
            form.description.data,
            str(form.date.data)
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    return render_template("add_expense.html", form=form)

@app.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, session["user_id"]))

    connection.commit()
    connection.close()

    return redirect(url_for("home"))

@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]

        cursor.execute("""
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?
            WHERE id = ? AND user_id = ?
        """, (
            amount,
            category,
            description,
            date,
            expense_id,
            session["user_id"]
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    cursor.execute("""
        SELECT amount, category, description, date
        FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, session["user_id"]))

    expense = cursor.fetchone()

    connection.close()

    return render_template("edit_expense.html", expense=expense)

@app.route("/set-budget", methods=["GET", "POST"])
def set_budget():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == "POST":

        budget = request.form["budget"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET budget = ?
            WHERE id = ?
        """, (budget, session["user_id"]))

        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    return render_template("set_budget.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)