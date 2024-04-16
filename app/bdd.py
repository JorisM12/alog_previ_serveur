import mysql.connector

def insert_forcast(data:object,sector:str):
    """Insère les données de prévisions dans la base de donnée

    Args:
        data (object): Donnée de prévisions
        sector (str): Secteur concerné
    """
    connexion = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    curseur = connexion.cursor()
    requete = "INSERT INTO forcasts (data_for,sector_for) VALUES (%s,%s)"
    valeurs = (data, sector)  
    curseur.execute(requete, valeurs)

    connexion.commit()
    curseur.close()
    connexion.close()
