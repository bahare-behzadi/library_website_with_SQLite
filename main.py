from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

db1 = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///new-books-collection.db'
db1.init_app(app)


class Book(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    title = db1.Column(db1.String, unique=True, nullable=False)
    author = db1.Column(db1.String, unique=True, nullable=False)
    rating = db1.Column(db1.FLOAT, nullable=False)


with app.app_context():
    db1.create_all()


@app.route('/', methods=['GET','POST'])
def home():
    all_books = []
    with app.app_context():
        result = db1.session.query(Book).order_by(Book.title).all()
        for book in result:
            field = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "rating": book.rating,
            }
            all_books.append(field)

    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
            db1.session.add(new_book)
            db1.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db1.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db1.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db1.get_or_404(Book, book_id)
    return render_template("edit.html", book1=book_selected)

if __name__ == "__main__":
    app.run(debug=True)

