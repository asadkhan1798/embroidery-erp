from flask import Flask, render_template_string
import sqlite3
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

# Home Page HTML
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Al.Kher ERP</title>
</head>
<body style="text-align:center; font-family:Arial;">

<img src="/logo.png" width="200">

<h1>🔥 Al.Kher Embroidery Textile</h1>

<form method="POST">
Customer:<br>
<input type="text" name="customer"><br><br>
Amount:<br>
<input type="number" name="amount"><br><br>
<button type="submit">Add Sale</button>
</form>

<h2>📊 Sales Data</h2>

{% for sale in sales %}
<p>{{sale[1]}} - {{sale[2]}}</p>
{% endfor %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    if flask_request := __import__("flask").request:
        if flask_request.method == "POST":
            customer = flask_request.form["customer"]
            amount = flask_request.form["amount"]
            cursor.execute("INSERT INTO sales(customer,amount) VALUES(?,?)",(customer,amount))
            conn.commit()

    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()

    return render_template_string(HTML, sales=sales)

@app.route("/logo.png")
def logo():
    return app.send_static_file("logo.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
