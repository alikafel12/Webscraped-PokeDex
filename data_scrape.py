import bs4 as bs
import sqlite3, requests, os, threading
from utilities import *

# setting directory for storing data
project_dir = os.getcwd()
img_dir = project_dir + '/imgs/'
os.makedirs(project_dir + '/imgs')

# starting page for scrape
start_url = 'https://pokemondb.net'
main_url = 'https://pokemondb.net/pokedex/all'
source = requests.get(main_url).content
parsed_source = bs.BeautifulSoup(source, 'lxml')

# scraping pokemon data table
table = parsed_source.find('table')
table_rows = table.find_all('tr')
pokemon_dict = {}

# scraping pokemon data
before = ''
for tr in table_rows:
    td = tr.find_all('td')
    row = [data.text for data in td]
    if row == []:
        continue
    row[1] = fix_name(row[1])
    row[2] = fix_type(row[2])
    temp_pokemon = Pokemon(int(row[0]), row[1], row[2], row[3], row[4], row[5],
                           row[6], row[7], row[8], row[9])
    if temp_pokemon.number in pokemon_dict:
        continue
    pokemon_dict[temp_pokemon.number] = temp_pokemon

# scraping pokemon image links
before = ''
pages = []
for data in parsed_source.find_all('a', class_ = 'ent-name'):
    curr = start_url + data['href']
    if before == curr:
        continue
    before = curr
    pages.append(start_url + data['href'])

# saving all pokemon images locally using multi-threading
num_threads = 10
num_pokemon = 809

def get_pic(start, end):
    # thread routine, stores a certain number of pokemon's images to a given directory
    for pokemon_num in range(start, end):
        pokemon = pokemon_dict[pokemon_num]
        poke_url = pages[pokemon.number - 1]
        source = requests.get(poke_url).content
        parsed_source = bs.BeautifulSoup(source, 'lxml')
        img_url = parsed_source.find('img')['src']
        pic = requests.get(img_url)
        pokemon.img = img_dir + pokemon.name
        open(pokemon.img, 'wb').write(pic.content)

# start of threading
threads = []
start = 1
split_factor = int(num_pokemon/num_threads)
end = split_factor + 1
for i in range(num_threads):
    thread = threading.Thread(target=get_pic, args=(start, end,))
    threads.append(thread)
    thread.start()
    start = end
    end += split_factor + 1
    if end > 810:
        end = 810

for thread in threads:
    thread.join()

# storing all scraped pokemon data in a sql database
connection = sqlite3.connect("pokemon.db")

cursor = connection.cursor()

sql_command = """
CREATE TABLE pokemon (
Number INTEGER PRIMARY KEY,
Name VARCHAR(50),
Type VARCHAR(30),
HP INTEGER,
Attack INTEGER,
Defense INTEGER,
Sp_Atk INTEGER,
Sp_Def INTEGER,
Speed INTEGER,
Total INTEGER,
Image VARCHAR(80));"""

cursor.execute(sql_command)

for pokemon in pokemon_dict.values():
    sql_command = """INSERT INTO pokemon (Number, Name, Type, HP, Attack, Defense, Sp_Atk, Sp_Def, Speed, Total, Image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    args = (pokemon.number, pokemon.name, pokemon.type, pokemon.hp, pokemon.attack, pokemon.defense, pokemon.sp_atk,
            pokemon.sp_def, pokemon.speed, pokemon.total, pokemon.img)
    cursor.execute(sql_command, args)

connection.commit()

connection.close()


