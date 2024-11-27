import pandas as pd

# data1 = pd.read_csv('pokemoncaracteristiques.csv', header = 0)
# data2 = pd.read_csv('pokemoncoeffdefense.csv', header = 0)
#
#
# data2["NationalNumber"] = data2["NationalNumber"].apply(lambda x: int(x[1:]))
#
# diet = pd.merge(data1[data1["Generation"] == 1] , data2, left_on = "Name", right_on = 'Pokemon', how = 'inner').drop(["Generation", "Pokemon", "NationalNumber"], axis = 1)
# print(diet.info())

data = pd.read_csv('pokedexbien.csv', header = 0)
data["Level"] = 1 #Niveau des pokemon (tous à 1 au départ)

data.to_csv("pokedexbien.csv", index = False)

