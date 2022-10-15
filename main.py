from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)


db.create_all()


@app.route("/")
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/delete", methods=["GET"])
def delete():
    id_to_delete = request.args.get("id")
    book_to_delete = Books.query.get(id_to_delete)
    db.session.delete(book_to_delete)
    db.session.commit()
    all_books = db.session.query(Books).all()
    return redirect(url_for("home"))


@app.route("/edit", methods=["POST", "GET"])
def edit_page():
    if request.method == "POST":
        new_rating = request.form["rating"]
        current_id = request.form["book_id"]
        book_to_update = Books.query.filter_by(id=current_id).first()
        book_to_update.rating = float(new_rating)
        db.session.commit()
        return redirect(url_for("home"))
    id = request.args.get("id")
    bookto_edit = Books.query.filter_by(id=id).first()
    print(bookto_edit.title)
    return render_template("edit.html", edit_book=bookto_edit)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=float(request.form["rating"]),
        )
        db.session.add(new_book)
        db.session.commit()
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
