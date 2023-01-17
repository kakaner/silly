from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize your Flask app and create the database client
# Replace the values starting with DB to connect
app = Flask(__name__)

DB_USER = None
DB_PSWD = None
DB_NAME = None
DB_HOST = None

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{DB_USER}:{DB_PSWD}@{DB_NAME}.{DB_HOST}:5432"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Our simple and only table in the database! A table of all the words we have collected
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)

# Helper function to insert a new word into the database
def insert_word(word):
    new_word = Word(word=word)
    db.session.add(new_word)
    db.session.commit()

# Define what happens when someone hits the homepage    
@app.route('/', methods=["GET", "POST"])
def index():

    # If the user is submitting a word, save it in the database
    if request.method == "POST":
        input_word = request.form["word"].strip()
        if len(input_word) > 1:
            insert_word(input_word)        

    # Regardless if it is a form submission or page load, update the words shown
    words = Word.query.all()    
    return render_template("words.html", words=words)

# run the app on port 5000
app.run(host='0.0.0.0', port=5000)
