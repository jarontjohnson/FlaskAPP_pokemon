from flask import Flask, request, render_template, jsonify  # Import jsonify for converting data to JSON
import requests

app = Flask(__name__)

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


def getPokemoninfo(pokemon):
    url = "https://pokeapi.co/api/v2/pokemon"
    response = requests.get(f"{url}/{pokemon}")
    output = []
    if response.status_code == 200:
        data = response.json()
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        return {
            "name": data['name'],
            "ability": abilities[0] if abilities else "N/A",
            "base_experience": data['base_experience'],
            "sprite_image": data['sprites']['front_default']
        }
    else:
        return None

pokemon_list = ["pikachu", "snorlax", "raichu", "charmeleon", "charizard", "eternatus"]

pokemon_info_list = []  # Initialize an empty list

for pokemon in pokemon_list:
    pokemon_info = getPokemoninfo(pokemon)
    if pokemon_info:
        pokemon_info_list.append(pokemon_info)  # Append each Pokémon info dictionary to the list

@app.route("/pokeapi", methods=["GET", "POST"])
def pokeapi():
    if request.method == "POST":
        name = request.form.get("name")
        stat = request.form.get("base_experience")
        front_shiny = request.form.get("https://pokeapi.co/api/v2/pokemon")
        abilities = request.form.get("ability")
        pokemon = {
        "name": name,
        "base_experience": stat,
        "sprite_image": front_shiny,
        "ability": abilities
    }
        # pokemon = pokemon_info(name, stat, front_shiny, abilities)
        return render_template("pokeapi.html", pokemon=pokemon)
        # return f"{name} {stat} {front_shiny} {abilities}"
    else:
        # Return the list of Pokémon info dictionaries as JSON
        return render_template("pokeapi.html")
