from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

billing = Blueprint('billing', __name__, url_prefix='/billing')

@billing.route("/create", methods=["GET", "POST"])
def create_bill():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Use correct column names for patients and appointments
        cursor.execute("""
            SELECT a.appointment_id, p.name as patient_name, 
                   p.patient_id, d.name as doctor_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.status = 'completed'
        """)
        appointments = cursor.fetchall()

        if request.method == "POST":
            appointment_id = request.form["appointment_id"]
            amount = request.form["amount"]
            payment_method = request.form["payment_method"]
            
            cursor.execute("""
                INSERT INTO bills 
                (appointment_id, amount, payment_method)
                VALUES (%s, %s, %s)
            """, (appointment_id, amount, payment_method))
            
            # Update appointment status
            cursor.execute("""
                UPDATE appointments SET status = 'billed'
                WHERE appointment_id = %s
            """, (appointment_id,))
            
            conn.commit()
            flash("Bill created successfully!", "success")
            return redirect(url_for("billing.list"))

        return render_template("create_bill.html", 
                            appointments=appointments)
        
    except Exception as e:
        conn.rollback()
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("billing.create"))
    finally:
        cursor.close()
        conn.close()