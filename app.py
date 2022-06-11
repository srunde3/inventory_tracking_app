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
    name = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=True)
    warehouse = db.relationship('Warehouse', back_populates='inventory_items')

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    inventory_items = db.relationship('InventoryItem', back_populates='warehouse')

    def __init__(self, name):
        self.name = name


@app.route('/')
def Index():
    inventory_data = InventoryItem.query.all()
    warehouse_data = Warehouse.query.all()
    return render_template("index.html", inventory_data=inventory_data, warehouse_data=warehouse_data)


@app.route('/insert_item', methods=['POST'])
def insert_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        data = InventoryItem(name, quantity)
        db.session.add(data)
        db.session.commit()

        flash("Inserted Inventory Item Successfully")
        return redirect(url_for('Index'))  # redirect user back to index


@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    if request.method == 'POST':
        data = InventoryItem.query.get(request.form.get('id'))  # the hidden ID from the form
        data.name = request.form['name']
        data.quantity = request.form['quantity']

        db.session.commit()

        flash("Updated Inventory Item Successfully")
        return redirect(url_for('Index'))


@app.route('/delete_item/<id>/', methods=['GET', 'POST'])
def delete_item(id):
    data = InventoryItem.query.get(id)

    db.session.delete(data)
    db.session.commit()

    flash("Deleted Inventory Item Successfully")
    return redirect(url_for('Index'))


@app.route('/insert_warehouse', methods=['POST'])
def insert_warehouse():
    if request.method == 'POST':
        name = request.form['name']

        data = Warehouse(name)
        db.session.add(data)
        db.session.commit()

        flash("Inserted Warehouse Successfully")

        return redirect(url_for('Index'))  # redirect user back to index


@app.route('/update_warehouse', methods=['GET', 'POST'])
def update_warehouse():
    if request.method == 'POST':
        data = Warehouse.query.get(request.form.get('id'))  # the hidden ID from the form
        data.name = request.form['name']

        db.session.commit()
        flash("Updated Warehouse Successfully")
        return redirect(url_for('Index'))


@app.route('/delete_warehouse/<id>/', methods=['GET', 'POST'])
def delete_warehouse(id):
    data = Warehouse.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Deleted Warehouse Successfully")
    return redirect(url_for('Index'))


if __name__ == "__main__":
    db.drop_all()  # clear db tables for development purposes
    db.create_all()  # create database tables
    app.run(debug=True)
