import requests

def get_weather_data(city:list = [49.13,6.16]):
    """Recupère depuis l'API, les données pour construire les prévisions

    Args:
        city (list, optional): Tableau contenant les coordonnées de la ville.

    Returns:
        _type_: _description_
    """
    url = "https://api.open-meteo.com/v1/dwd-icon?latitude="+str(city[0])+"&longitude="+str(city[1])+"&hourly=temperature_2m,weather_code,cloud_cover_high,wind_speed_10m,wind_direction_10m,wind_gusts_10m&forecast_days=5&daily=sunrise,sunset,daylight_duration"
    reponse = requests.get(url)
    data = reponse.json()
    return data['hourly']


def get_day_info(city:list = [49.13,6.16]):
    """Récupère les informations générales (Lever et coucher du soleil et durée du jour)

    Args:
        city (list, optional): Tableau contenant les coordonnées de la ville.

    Returns:
        _type_: Données du jour
    """
    url = "https://api.open-meteo.com/v1/dwd-icon?latitude="+str(city[0])+"&longitude="+str(city[1])+"&forecast_days=5&daily=sunrise,sunset,daylight_duration&timezone=Europe%2FBerlin"
    reponse = requests.get(url)
    data = reponse.json()
    return data['daily']


def get_smog_info(city:list = [49.13,6.16]):
    """Récupère les infos liées à la qualité de l'air (european aqi , Index UV) depuis l'API Open Météo

    Args:
        city (list, optional): Tableau contenant les coordonnées de la ville.


    Returns:
        _type_: _description_ European aqi et  Index UV
    """
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude="+str(city[0])+"&longitude="+str(city[1])+"&hourly=uv_index,european_aqi"
    reponse = requests.get(url)
    data = reponse.json()
    return data['hourly']

   

   
def treatment_data(data_json:object ,day = 0, period:str = 'morning', type_of_data:str = '')->dict: 
    """Traite les données et les regroupes en fonction de la période de la journée et du jour

    Args:
        data_json (object): JSON contenant les données à traiter
        day (int, optional): _description_. Defaults to 0.
        period (str, optional): periode de la journée
        type_of_data (str, optional): Type de données

    Returns:
        dict: Dictionnaire contenant les données traitées
    """
    bornInf = 0
    bornSup = 0
    if(day == 0 and period == 'morning'):
        bornInf = 5
        bornSup = 11
    elif(day == 0 and period == 'afternoon'):
        bornInf = 11
        bornSup = 17
    elif(day == 0 and period == 'evening'):
        bornInf = 18
        bornSup = 23
    elif(day == 0 and period == 'night'):
        bornInf = 23
        bornSup = 29
    elif(day == 1 and period == 'morning'):
        bornInf = 29
        bornSup = 35
    elif(day == 1 and period == 'afternoon'):
        bornInf = 35
        bornSup = 42
    elif(day == 1 and period == 'evening'):
        bornInf = 42
        bornSup = 47
    elif(day == 1 and period == 'night'):
        bornInf = 47
        bornSup = 53
    elif(day == 2 and period == 'morning'):
        bornInf = 53
        bornSup = 59
    elif(day == 2 and period == 'afternoon'):
        bornInf = 59
        bornSup = 65
    elif(day == 2 and period == 'evening'):
        bornInf = 65
        bornSup = 71
    elif(day == 2 and period == 'night'):
        bornInf = 71
        bornSup = 77
    elif(day == 3 and period == 'morning'):
        bornInf = 77
        bornSup = 83
    elif(day == 3 and period == 'afternoon'):
        bornInf = 83
        bornSup = 89
    elif(day == 3 and period == 'evening'):
        bornInf = 89
        bornSup = 95
    elif(day == 3 and period == 'night'):
        bornInf = 95
        bornSup = 101
    tab = data_json
    values = tab[type_of_data]
    index = 0
    weather_data = []
    for hour in values:
        if(index >= bornInf and index < bornSup): 
            weather_data.append(round(values[index]))
        index+=1

    forcast = {}
    
    forcast['full'] = weather_data
    if(weather_data):
        forcast['max'] = round(max(weather_data))
        forcast['min'] = round(min(weather_data))
        
    return  forcast



def treatment_data_somg_and_uv(data_json,day = 0, period:str = 'morning', type_of_data:str = 'uv_index')->dict: 
    """Met en forme les données de qualité de l'air et UV

    Args:
        data_json (_type_): Données bruts
        day (int, optional): Defaults to 0.
        period (str, optional): Periode de la journée
        type_of_data (str, optional): Type de données

    Returns:
        dict: Dictionnaire contenant les données traitées
    """
    bornInf = 0
    bornSup = 0
    if(day == 0 ):
        bornInf = 0
        bornSup = 23
    elif(day == 1):
        bornInf = 24
        bornSup = 48
    elif(day == 2):
        bornInf = 48
        bornSup = 72
    elif(day == 3):
        bornInf = 72
        bornSup = 96

    data = {}
    tab = data_json
    values = tab[type_of_data]
    index = 0
    weather_data = []
    for hour in values:
        if(index >= bornInf and index < bornSup): 
            weather_data.append(round(values[index]))
        index+=1

    forcast = {}
    
    
    forcast['full'] = weather_data
    if(weather_data):
        forcast['max'] = round(max(weather_data))
        forcast['min'] = round(min(weather_data))
    return  forcast


def treatment_day_info(data_json:object,day:int = 0, type_of_data:str = 'uv_index'): 
    """Met en forme les données générales (durée du jour etc)

    Args:
        data_json (object): Données bruts
        day (int, optional): Numéro du jour 0 à 3
        type_of_data (str, optional): Type de données

    Returns:
        _type_: Données traitées
    """
    tab = data_json
    values = tab[type_of_data]
    if(day == 0 ):
        values = values[0]
    elif(day == 1):
        values = values[1]
        
    elif(day == 2):
        values = values[2]
        
    elif(day == 3):
        values = values[3]    
    return values




