import pandas as pd

"""
data1 = pd.read_csv('pokemoncaracteristiques.csv', header = 0)
data2 = pd.read_csv('pokemoncoeffdefense.csv', header = 0)


data2["NationalNumber"] = data2["NationalNumber"].apply(lambda x: int(x[1:]))

diet = pd.merge(data1[data1["Generation"] == 1] , data2, left_on = "Name", right_on = 'Pokemon', how = 'inner').drop(["Generation", "Pokemon", "NationalNumber"], axis = 1)
#print(diet.info())

# diet.to_csv("pokedexbien.csv", index = False)
"""
data = pd.read_csv('pokedexbien.csv', header = 0, index_col = "Name")
data["Level"] = 1 #Niveau des pokemon (tous à 1 au départ)
data["Image"] = data.index.map(lambda nom: f"{nom.lower()}.png")
print(data["Image"])


def selectionner_pokemon(data, n):
    df = data.sample(2*n)
    m = df["Total"].mean()
    groupe1 = [df.index[0]]
    groupe2 = [df.index[1]]

    somme1 = df.iloc[0]["Total"]
    somme2 = df.iloc[1]["Total"]
    for i in range (2, n*2):
        s = df.iloc[i]["Total"]
        if len(groupe2)== 60:
            somme1 += s
            groupe1.append(df.index[i])
        elif len(groupe1) == 60:
            somme2 += s
            groupe2.append(df.index[i])
        elif abs(somme1+s - somme2) > abs(somme2+s - somme1):
            somme2 += s
            groupe2.append(df.index[i])
        else:
            somme1 += s
            groupe1.append(df.index[i])
    #df1 = pd.DataFrame(groupe1)
    #df2 = pd.DataFrame(groupe2)
    print(groupe1)
    print(groupe2)
    print(len(groupe1), len(groupe2))
    m1 = somme1/n
    m2 = somme2/n
    print(m1,m2)
    print(100*(abs(m1-m2)/m)) #pourcentage de différence des totaux
    return groupe1, groupe2

selectionner_pokemon(data, 60)
