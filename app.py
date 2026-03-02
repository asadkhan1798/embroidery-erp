from flask import Flask, render_template_string, request
import sqlite3
from flask import send_from_directory
import os
app = Flask(__name__)

# Database
conn = sqlite3.connect("erp.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer TEXT,
amount REAL
)
""")
conn.commit()

HTML = """<img src="{{ logo }}" width="150">
<h1>🔥 Embroidery Live ERP</h1>

<form method="POST">
Customer: <input type="text" name="customer"><br><br>
Amount: <input type="number" name="amount"><br><br>
<button type="submit">Add Sale</button>
</form>

<h2>📊 Sales Data</h2>
{% for sale in sales %}
<p>{{sale[1]}} - {{sale[2]}}</p>
{% endfor %}
"""

@app.route("/", methods=["GET","POST"])
def home(logo_url = "/logo.png"):
    if request.method == "POST":
        customer = request.form["customer"]
        amount = request.form["amount"]
        cursor.execute("INSERT INTO sales(customer,amount) VALUES(?,?)",(customer,amount))
        conn.commit()

    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    return render_template_string(HTML, sales=sales, logo=logo_url)(HTML, sales=sales)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
