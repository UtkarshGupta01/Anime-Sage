import pandas as pd
from flask import Flask, render_template, url_for, session, redirect, request
import pickle
from datetime import datetime
import mysql.connector
 
# connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="123")
dbcursor = db.cursor()

# Create the database if it doesn't exist
dbcursor.execute("CREATE DATABASE IF NOT EXISTS ANIME_RECOMMENDER")
dbcursor.execute("USE ANIME_RECOMMENDER")

# Create the userinfo table if it doesn't exist
dbcursor.execute("""
    CREATE TABLE IF NOT EXISTS userinfo (
        user_name VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        user_password VARCHAR(50)
    )
""")

# load the data
anime_data = pickle.load(open('anime_data.pkl', 'rb'))
similarity = pickle.load(open('similarities.pkl', 'rb'))
popular_anime = pickle.load(open('popular_anime.pkl', 'rb'))

#  Encode password function
def encode_password(password):
    encrpyt_password = ""
    for i in password:
        encrpyt_password += chr(ord(i)+1)
    return encrpyt_password[::-1]

# recommend anime function
def recommend_anime(anime_name):
    anime_name = anime_name.lower()
    anime_index = anime_data[(anime_data['Name'].str.lower() == anime_name) | (
        anime_data['English name'].str.lower() == anime_name)].index[0]
    distance = similarity[anime_index]
    anime_list = sorted(list(enumerate(distance)),
                        reverse=True, key=(lambda x: x[1]))[1:33]
    recommended_anime_name = []
    recommended_anime_image = []
    recommended_anime_genre = []
    for i in anime_list:
        recommended_anime_name.append(anime_data.iloc[i[0]].Name)
        recommended_anime_image.append(anime_data.iloc[i[0]].Img_url)
        recommended_anime_genre.append(anime_data.iloc[i[0]].Genres)
    return recommended_anime_name, recommended_anime_image, recommended_anime_genre


app = Flask(__name__)

app.secret_key = "mykey"


# ==========Routes

# for the home page
@app.route('/home')
@app.route('/')
def home():
    return render_template("index.html", anime_name=list(popular_anime['Name'].values),
                           anime_poster=list(popular_anime['Img_url'].values),
                           anime_genre=list(popular_anime['Genres'].values))


# for the recommendation page
@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    anime_list = anime_data['Name'].values
    status = False
    error_msg = False
    if request.method == 'POST':
        try:
            if request.form:
                anime_name = request.form['searched_anime']

                recommended_anime_name, recommended_anime_image, recommended_anime_genre = recommend_anime(
                    anime_name)

                # # For debugging purposes
                # print(f"Received anime_name: {anime_name}")

                # # For debugging purposes recommended_anime_name
                # print(f"Recommended anime names: {recommended_anime_name}")

                status = True
                error_msg = False

                return render_template("recommend.html", anime_name=recommended_anime_name, anime_poster=recommended_anime_image, anime_genre=recommended_anime_genre, anime_list=anime_list, status=status, error_msg=error_msg)

        except Exception as e:
            error = {"error": e}
            return render_template("recommend.html", anime_list=anime_list, status=status, error=error, error_msg=True)
    else:
        return render_template("recommend.html", anime_list=anime_list, status=status, error_msg=error_msg)

# for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# for the login page
@app.route('/login')
def login():
    return render_template("login.html")

# for logging in the user
@app.route("/index", methods=["GET", "POST"])
def login_user(): 

    incorrect = False

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pwd')
        password = encode_password(password)
        dbcursor.execute(
            "SELECT user_name, user_password FROM userinfo WHERE user_name = %s AND user_password = %s", (username, password))
        user_details = dbcursor.fetchone()
        if user_details:
            session['username'] = user_details[0]
            return redirect("/home")
        else:
            incorrect = True
            return render_template("login.html", incorrect=incorrect)

    return render_template("login.html")

# for signup page
@app.route('/signup')
def signup():
    return render_template("signup.html")


# for registering the user
@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    registered = False
    if request.method == "POST":
        firstname = request.form.get('f_name')
        lastname = request.form.get('l_name')
        username = request.form.get('username')
        password = request.form.get('pwd')
        confirm_password = request.form.get('c_pwd')
        if password == confirm_password:
            confirm_password = encode_password(confirm_password)
            try:
                dbcursor.execute("INSERT INTO userinfo VALUES (%s, %s, %s, %s)",
                                 (username, firstname, lastname, confirm_password))
                db.commit()
                registered = True
                return render_template("login.html",registered=registered)
            except Exception as e:
                return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
    dbcursor.close()
    db.close()
