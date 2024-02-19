from flask import request, render_template, flash, redirect, url_for
import requests
from app import app
from app.models import User
from .forms import LoginForm , SignupForm
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit:
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username, email, password)
        new_user.save()
        flash('Success! Thank you for Signing up', 'Success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit:
        email = form.email.data
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Welcome {queried_user.username}!', 'info')
            login_user(queried_user)
            return redirect(url_for('home'))
        else: 
            flash('incorrect username, email or password....please try again', 'warning')
        return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
#
def get_pokemon_info(pokemon):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    output = []
    if response.status_code == 200:
        data = response.json()
        p_info = {
            'name': data['name'],
            'hp': data['stats'][0]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'ability': data['abilities'][0]['ability']['name'] if data['abilities'] else None,
            'base_experience': data['base_experience'],
            'sprite': data['sprites']['front_default']
        }
        # pokemon = pokemon_info(name, stat, front_shiny, abilities)

        return p_info
    else:
        return output.append
    # Define a list of Pokemon names
pokemon_names = ["pikachu", "snorlax", "raichu", "charmeleon", "charizard", "eternatus"]
    # pokemon_info = [get_pokemon_info(name) for name in pokemon_names]
pokemon_info_list = []
def get_pokemon_info(pokemon):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    if response.ok:
        data = response.json()
        p_info = {
            'name': data['name'],
            'hp': data['stats'][0]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'ability': data['abilities'][0]['ability']['name'] if data['abilities'] else None,
            # 'base_experience': data['base_experience'],
            'sprite': data['sprites']['front_default']
        } 

        return p_info

@app.route("/pokemon", methods=["GET", "POST"])
def pokemon():
    if request.method == "POST":
        name = request.form.get("name")
        pokemon = get_pokemon_info(name)
        # name = request.form.get("name")
        return render_template("pokeapi.html", pokemon=pokemon)
        # return f"{get_pokemon_info}"
    else:
        # Return the list of Pokemon info dictionaries as JSON  
        # return jsonify(pokemon_info)
        return render_template("pokeapi.html")

