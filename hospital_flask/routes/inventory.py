from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

inventory = Blueprint("inventory", __name__)

@inventory.route("/inventory")
def inventory_list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("inventory.html", inventory=items)

@inventory.route("/add_inventory", methods=["GET", "POST"])
def add_inventory():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        item_name = request.form["item_name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        supplier = request.form["supplier"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventory (item_name, category, quantity, supplier)
            VALUES (%s, %s, %s, %s)
        """, (item_name, category, quantity, supplier))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Inventory item added successfully!")
        return redirect(url_for("inventory.inventory_list"))

    return render_template("add_inventory.html")
