from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:906@localhost:5432/crud_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    type_item = db.Column(db.String(100))

    def __init__(self, title, supplier, type_item):
        self.title = title
        self.supplier = supplier
        self.type_item = type_item


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", products=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        title = request.form['title']
        supplier = request.form['supplier']
        type_item = request.form['type_item']

        my_data = Data(title, supplier, type_item)
        db.session.add(my_data)
        db.session.commit()

        flash("Товар добавлен успешно")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.title = request.form['title']
        my_data.supplier = request.form['supplier']
        my_data.type_item = request.form['type_item']

        db.session.add(my_data)
        db.session.commit()
        flash("Товар изменен успешно")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Товар удален')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
