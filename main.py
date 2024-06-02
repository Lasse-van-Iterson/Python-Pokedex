import requests

def main():
    print("Hello, welcome to the python pokedex!")
    print("Please enter the name or id of the pokemon you would like to search for: ")
    pokemon_name = input()
    pokemon = get_pokemon(pokemon_name)
    print_pokemon(pokemon)
    

def get_pokemon(pokemon_name):
    pokemon_name = pokemon_name.replace(" ", "-").lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)        
    pokemon = response.json()
    return pokemon

def print_pokemon(pokemon):
    print(f"Name: {pokemon['name']}")
    print(f"ID: {pokemon['id']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print(f"Types: ")
    for type in pokemon['types']:
        print(f"  - {type['type']['name']}")

if __name__ == "__main__":
    main()
