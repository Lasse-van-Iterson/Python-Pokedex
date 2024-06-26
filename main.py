import requests
from PIL import Image
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def main():
    print("Please enter the name or id of the pokemon you would like to search for: ")
    while True:
        pokemon_name = input()
        pokemon_name = pokemon_name.replace(" ", "-").lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url) 
        if response.status_code != 200:
            print(f"I could not find that pokemon, please try again")
        else: break
    print(response.status_code)      
    pokemon = response.json()
    print_sprite(pokemon)
    play_sound(pokemon)
    repeat = input("Would you like to search for another pokemon? (y/n)")
    if repeat.lower() == 'y':
        main()
    else:
        print("We hope to see you again!")

def invalid_pokemon():
    print("Invalid pokemon name or id, please try again")

def print_pokemon(pokemon):
    print(f"Name: {pokemon['name']}")
    print(f"ID: {pokemon['id']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print(f"Types: ")
    for type in pokemon['types']:
        print(f"  - {type['type']['name']}")
    print_sprite(pokemon['sprites']['front_default'])
    print(f"Sprite: {pokemon['sprites']['front_default']}")

def rgb_to_ansi(r, g, b):
    return f"\033[48;2;{r};{g};{b}m  \033[0m"

def play_sound(pokemon):
    url = pokemon['cries']['latest']
    response = requests.get(url)
    audio = AudioSegment.from_file(BytesIO(response.content), format="ogg")
    play(audio)

def print_sprite(pokemon):
    url = pokemon['sprites']['front_default']
    info_height = 30
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        print(img.width, img.height)
        img = img.crop((5, 5, 90, 90)) 
        img = img.resize((40, 40))  

        
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        
        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                if len(pixel) == 4:
                    r, g, b, a = pixel
                    if a > 0:
                        print(rgb_to_ansi(r, g, b), end='')
                    else:
                        print('  ', end='')
                else: 
                    r, g, b = pixel
                    print(rgb_to_ansi(r, g, b), end='')
            if y == info_height:
                print(f"Name: {pokemon['name']}")
            elif y ==  info_height + 1:
                print(f"ID: {pokemon['id']}")
            elif y == info_height + 2:
                print(f"Height: {pokemon['height']}")
            elif y == info_height + 3:
                print(f"Weight: {pokemon['weight']}")
            elif y == info_height + 4:
                print(f"Types: {', '.join([f' {t["type"]["name"]}' for t in pokemon["types"]])}")
            elif y == info_height + 5:
                print(f"First game apperance: {pokemon['game_indices'][0]['version']['name']}")

            else:
                print('')

if __name__ == "__main__":
    print("Hello, welcome to the python pokedex!")
    main()
