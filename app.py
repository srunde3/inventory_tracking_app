"""Main application file.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\sqlite\\Databases\\python_crud_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone



@app.route('/')
def Index():
    all_data = InventoryItem.query.all()
    return render_template("index.html", data=all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        data = InventoryItem(name, email, phone)
        db.session.add(data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Index'))  # redirect user back to index

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = InventoryItem.query.get(request.form.get('id'))  # the hidden ID from the form
        data.name = request.form['name']
        data.email = request.form['email']
        data.phone = request.form['phone']

        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = InventoryItem.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
