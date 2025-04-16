from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid warnings

# Initialize the database
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Id = db.Column(db.String(10), unique=True, nullable=False)
    Book_name = db.Column(db.String(50), nullable=False)
    Author = db.Column(db.String(50), nullable=False)
    Publisher = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"{self.Book_name} {self.Author} - {self.Publisher}"

# Create the database tables
with app.app_context():
    db.create_all()

# Function to collect Book data via terminal input
def collect_Book_data():
    with app.app_context():  # Ensures Flask recognizes the app context
        while True:
            mbr_num = input("Please enter Id (or 'ZZZ' to quit): ")
            if mbr_num.strip() == "ZZZ":
                break

            fir_name = input("Enter First Name: ")
            las_name = input("Enter Last Name: ")
            pos_desc = input("Enter Position Description: ")

            new_Book = Book(Id=mbr_num.strip(), Book_name=fir_name.strip(), Author=las_name.strip(), Publisher=pos_desc.strip())
            db.session.add(new_Book)
            db.session.commit()
            print(f"Book {fir_name} {las_name} added successfully!")

# Flask route to list all Books
@app.route('/Books', methods=['GET'])
def get_Books():
    Books = Book.query.all()
    return jsonify([{"Id": m.Id, "Book_name": m.Book_name, "Author": m.Author, "Publisher": m.Publisher} for m in Books])

# Flask route to find a Book by last name
@app.route('/lookup/<las_name>', methods=['GET'])
def lookup_Book(las_name):
    Book = Book.query.filter_by(Author=las_name).first()
    if Book:
        return jsonify({"Id": Book.Id, "Book_name": Book.Book_name, "Author": Book.Author, "Publisher": Book.Publisher})
    else:
        return jsonify({"message": "Book not found"})

# Function to look up Books by last name in the terminal
def lookup_Book_terminal():
    with app.app_context():
        while True:
            las_name = input("Please input Last Name to look up a Book (or 'AAA' to quit): ")
            if las_name.strip() == "AAA":
                break

            Book = Book.query.filter_by(Author=las_name.strip()).first()
            if Book:
                print(f"Book Found: {Book.Book_name} {Book.Author} - {Book.Publisher}")
            else:
                print("Book not found.")

# Run the terminal input collection, lookup function, and start Flask
if __name__ == "__main__":
    collect_Book_data()
    lookup_Book_terminal()
    print("Starting Flask server... Open http://127.0.0.1:5001/Books to view data.")
    app.run(debug=True)
