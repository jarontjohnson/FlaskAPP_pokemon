from flask import request, render_template
import requests
from app import app


@app.route("/")
def hello_world():
    return "<p> Hello Thieves! intro Flask <p/>"

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("passsword")
        return f"{email} {password}"
    else:
        return render_template("login.html")

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