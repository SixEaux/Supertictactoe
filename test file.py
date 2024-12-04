import pandas as pd
import random
import csv

pokedex = pd.read_csv('pokedexbien.csv', header=0, index_col="Name")



def calculate_damage(pokemon1, pokemon2):
    Pokemon1 = pokedex.loc[pokemon1]
    Pokemon2 = pokedex.loc[pokemon2]
    random_factor = random.uniform(0.85, 1.0)  # we use a random factor between 85% and 100%
    type1 = Pokemon1["Type_1"]
    if not pd.isnull(Pokemon1["Type_2"]):
        type2 = Pokemon1["Type_2"]
        mc = Pokemon2[type1] * Pokemon2[type2] * random_factor
    else:
        mc = Pokemon2[type1] * random_factor
    damage = (((((Pokemon1["Level"] * 0.4 + 2) * Pokemon1["Attack"]) / Pokemon2["Defense"]) / 50) + 2) * mc*10
    return max(damage, 1)  #pokeons cant deal less than 0 damage


#print(calculate_damage("Venusaur", "Bulbasaur"))
def pokemon_combat(Pokemon1, Pokemon2):
    pokemon11 = pokedex.loc[Pokemon1]
    pokemon22 = pokedex.loc[Pokemon2]
    pokemon1_name = pokemon11.name
    pokemon2_name = pokemon22.name
    HP1 = pokemon11["HP"]
    HP2 = pokemon22["HP"]

    while HP1 >0 and HP2 >0:
        damage1 = calculate_damage(pokemon1_name,  pokemon2_name )
        damage2 = calculate_damage(pokemon2_name , pokemon1_name)

        HP1  -= damage2
        HP2  -= damage1

    # Determine the result
    if HP1 <= 0 and HP2 <= 0:
        print  (" both fainted! its a draw.")
        return ("DRAW")
    elif HP1 <= 0:
        print (f"{pokemon1_name} is Dead! {pokemon2_name} WINS THE FIGHT.")
        return pokemon2_name
    elif HP2 <= 0:
        print (f"{pokemon2_name} is Dead! {pokemon1_name} WINS THE FIGHT.")
        return pokemon1_name
    else:
        print ("Both Pokémon survived!")
        return ("DRAW")

print(pokemon_combat("Paras", "Charmander"))

def combat_probability_safe(pokemon1, pokemon2, simulations=10):
    pokemon1_wins = 0
    for _ in range(simulations):
        result = pokemon_combat(pokemon1, pokemon2)
        if pokemon1 in result:
            pokemon1_wins += 1
    return pokemon1_wins / simulations
import os

# Create output directory
os.makedirs('output_directory', exist_ok=True)

# Generate the corrected probability matrix
limited_pokemon_names = pokedex.index.tolist()
probability_matrix_safe = pd.DataFrame(index=limited_pokemon_names, columns=limited_pokemon_names)

for p1 in limited_pokemon_names:
    for p2 in limited_pokemon_names:
        print(f"Processing: {p1} vs {p2}")  # Debug log
        if p1 != p2:
            try:
                probability_matrix_safe.at[p1, p2] = combat_probability_safe(p1, p2)
            except Exception as e:
                print(f"Error processing {p1} vs {p2}: {e}")
                probability_matrix_safe.at[p1, p2] = None
        else:
            probability_matrix_safe.at[p1, p2] = 0.5
    # Save progress periodically
    probability_matrix_safe.to_csv('output_directory/pokemon_battle_probabilities_safe_partial.csv')

# Save the final CSV
output_path_safe = 'output_directory/pokemon_battle_probabilities_safe1.csv'
probability_matrix_safe.to_csv(output_path_safe)

print(f"File saved at: {output_path_safe}")