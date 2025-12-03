#all imports needed for this project
from flask import Flask, render_template, request
from flask import session, redirect, url_for
from pymysql.err import IntegrityError
from werkzeug.security import generate_password_hash
import pymysql
from pymongo import MongoClient
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

#flask and mongoDB setup
app = Flask(__name__)

#loads .env for credentials
load_dotenv()

mongo_client = MongoClient(
    "mongodb+srv://s5623281_db_user:w1GZ1lWaa0yQSTlu@cluster0.3joitcy.mongodb.net/?appName=Cluster0"
)

mongo_db = mongo_client["gamestore"]
reviews_collection = mongo_db["reviews"]

#gets all games from the DB
def get_all_games():
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM games")
            return cursor.fetchall()

#connection to the database
def get_db_connection():
    connection = pymysql.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DB"),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

#gets the game by ID
def get_game(game_id):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM games WHERE id=%s", (game_id,))
            return cursor.fetchone()

#fetch featured games from cloud run
@app.route("/featured")
def featured():
    url = "https://featured-games-104703165942.europe-west2.run.app"
    response = requests.get(url)

    if response.status_code == 200:
        featured_games = response.json()["featured"]
    else:
        featured_games = []

    return render_template("featured.html", games=featured_games)

#grabs reviews when called by ID
def get_reviews_for_game(game_id):
    return list(reviews_collection.find({"game_id": game_id}).sort("timestamp", -1))

#function to add reviews
def add_review(game_id, user_email, text):
    review_doc = {
        "game_id": game_id,
        "user_email": user_email,
        "text": text,
        "timestamp": datetime.utcnow()
    }
    reviews_collection.insert_one(review_doc)

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
def game_detail(game_id):
    game = get_game(game_id)

    if not game:
        return render_template("404.html"), 404

    #post a review
    if request.method == "POST":
        if "user" not in session:
            return redirect("/login")

        review_text = request.form.get("review")
        if review_text:
            add_review(game_id, session["user"], review_text)

        return redirect(f"/game/{game_id}")

    #load mongodb reviews
    reviews = get_reviews_for_game(game_id)

    return render_template(
        "game_detail.html",
        game=game,
        reviews=reviews
    )

@app.route("/buy/<int:game_id>")
def buy(game_id):
    #fetch game from SQL
    game = get_game(game_id)

    if not game:
        return "Game not found", 404

    return render_template("buy.html", game=game)

@app.route("/")
@app.route("/home")
def home():
    games = get_all_games()

    mesh_url = "https://europe-west2-gamestorewebsiteproject.cloudfunctions.net/mesh-service"

    try:
        mesh_response = requests.get(mesh_url, timeout=5)

        if mesh_response.status_code == 200:
            data = mesh_response.json()
            featured_games = data.get("featured", [])
            top_reviews = data.get("top_reviews", [])
        else:
            featured_games = []
            top_reviews = []
    except:
        featured_games = []
        top_reviews = []

    return render_template(
        "home.html",
        games=games,
        featured_games=featured_games,
        reviews=top_reviews
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #if already logged in send user back home
    if session.get('user'):
        return redirect(url_for('home'))

    error = None

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        else:
            password_hash = generate_password_hash(password)

            try:
                connection = get_db_connection()
                with connection:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
                        cursor.execute(sql, (email, password_hash))
                    connection.commit()

                #redirect user to login
                return redirect(url_for('login'))

            except IntegrityError:
                error = "That email is already registered."

    return render_template("register.html", error=error)

@app.route('/submitted', methods=['POST'])
#account created form
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_account.html',
        name=name,
        email=email,
        site=site,
        comments=comments
    )

#temp will be moved to yaml
app.secret_key = "dev_key_for_now"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #finds account in DB and checks credentials if exists
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email=%s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

        if user:
            from werkzeug.security import check_password_hash
            if check_password_hash(user['password_hash'], password):
                session['user'] = user['email']
                return redirect(url_for('home'))
            else:
                error = "Incorrect password."
        else:
            error = "User not found."

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def calculate_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError("Invalid discount percentage")
    return round(price * (1 - percent / 100), 2)


#run the app when everything is ready
if __name__ == '__main__':
    app.run(debug=True)