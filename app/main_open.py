import json
from bdd import  insert_forcast;
from open_meteo import get_weather_data,treatment_data,treatment_day_info,treatment_data_somg_and_uv,get_day_info,get_smog_info

forcast_data = {}
data = {}
data_dep = {}
data_day = {}
data_day_period = {}
data_day_afternoon = {}
data_day_evening = {}
data_day_night = {}
data_day_ww = {}
city = [49.13,6.16]


def convert(seconds:int)->list:
    """Convertie les secondes en heures et minutes

    Args:
        seconds (int): Nombre de secondes

    Returns:
        list: Retourne une liste contenant la valeur de l'heure et les minutes
    """
    hours = round(seconds / 3600)
    otherSeconds = seconds % 3600
    minutes = round(otherSeconds / 60)
    hours = hours -1
    return [hours ,minutes]

def format_date(date:str)->str:
    """Récupère la date

    Args:
        date (str): Date brut 

    Returns:
        str: Retourne la date nettoyée
    """
    new_date = date.split('T')
    return new_date[-1]


def create_forcast_data(name_city:str,city:list, forcast_data_api,info_data,uv_data)->dict:
    """Créer les données pour la carte de prévision

    Args:
        name_city (str): Nom de la ville
        city (list): Tableau de coordonnées de la ville [lat,lon]
        forcast_data_api (_type_): Données de prévisions mises en forme
        info_data (_type_): Données des infos complémentaires mises en forme
        uv_data (_type_): Index UV

    Returns:
        dict: Données prêtes à être insérées dans la base de données 
    """
    forcast_data = {}
    data_day = {}
    data_day_period = {}
    all_data = {}
    data_day_info = {}
    list_period = ['morning','afternoon','evening','night']
    for p_day in list_period:
        data_day_period['t2m'] = treatment_data(forcast_data_api,type_of_data='temperature_2m',period=p_day)
        data_day_period['ww'] = treatment_data(forcast_data_api,type_of_data='weather_code',period=p_day)
        data_day_period['max_wind'] = treatment_data(forcast_data_api,type_of_data='wind_gusts_10m', period=p_day)
        data_day_period['wind_dir'] = treatment_data(forcast_data_api,type_of_data='wind_direction_10m', period=p_day)
        data_day[p_day] = data_day_period
        data_day_period = {}
    uv_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=0)
    data_day_info['uv'] = uv_data['max']
    smog_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=0, type_of_data='european_aqi')
    data_day_info['smog'] = smog_data['max']
    sunset = format_date(treatment_day_info(info_data,type_of_data='sunset'))
    data_day_info['sunset'] = sunset
    sunrise =  format_date(treatment_day_info(info_data,type_of_data='sunrise'))
    data_day_info['sunrise'] =  sunrise
    day_duration = convert(treatment_day_info(info_data,type_of_data='daylight_duration'))
    data_day_info['daylight_duration'] = day_duration
    data_day['info'] = data_day_info
    data_day_info = {}
    all_data['J1'] = data_day
    data_day_J2 = {}
    data_day = {}
    
    for p_day in list_period:
        data_day_period['t2m'] = treatment_data(forcast_data_api,type_of_data='temperature_2m',period=p_day,day=1)
        data_day_period['ww'] = treatment_data(forcast_data_api,type_of_data='weather_code',period=p_day,day=1)
        data_day_period['max_wind'] = treatment_data(forcast_data_api,type_of_data='wind_gusts_10m', period=p_day,day=1)
        data_day_period['wind_dir'] = treatment_data(forcast_data_api,type_of_data='wind_direction_10m', period=p_day,day=1)
        data_day_J2[p_day] = data_day_period
        data_day_period = {}
    uv_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=0)
    data_day_info['uv'] = uv_data['max']
    smog_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=0, type_of_data='european_aqi')
    data_day_info['smog'] = smog_data['max']
    sunset = format_date(treatment_day_info(info_data,type_of_data='sunset',day=1)) 
    data_day_info['sunset'] = sunset
    sunrise =  format_date(treatment_day_info(info_data,type_of_data='sunrise',day=1))
    data_day_info['sunrise'] =  sunrise
    day_duration = convert(treatment_day_info(info_data,type_of_data='daylight_duration',day=1))
    data_day_info['daylight_duration'] = day_duration
    data_day_J2['info'] = data_day_info
    data_day_info = {}
    data_day_period = {}
    all_data['J2'] = data_day_J2
    data_day_period = {}
    data_day = {}   
    data_day_period = {}
    
    data_day = {}
    data_day_period = {}
    for p_day in list_period:
        data_day_period['t2m'] = treatment_data(forcast_data_api,type_of_data='temperature_2m',period=p_day,day=2)
        data_day_period['ww'] = treatment_data(forcast_data_api,type_of_data='weather_code',period=p_day,day=2)
        data_day_period['max_wind'] = treatment_data(forcast_data_api,type_of_data='wind_gusts_10m', period=p_day,day=2)
        data_day_period['wind_dir'] = treatment_data(forcast_data_api,type_of_data='wind_direction_10m', period=p_day,day=2)
        data_day[p_day] = data_day_period
        data_day_period = {}
        
    uv_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=2)
    data_day_info['uv'] = uv_data['max']
    smog_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=2, type_of_data='european_aqi')
    data_day_info['smog'] = smog_data['max']
    sunset = format_date(treatment_day_info(info_data,type_of_data='sunset',day=2))
    data_day_info['sunset'] = sunset
    sunrise =  format_date(treatment_day_info(info_data,type_of_data='sunrise',day=2))
    data_day_info['sunrise'] =  sunrise
    day_duration = convert(treatment_day_info(info_data,type_of_data='daylight_duration',day=2))
    data_day_info['daylight_duration'] = day_duration
    data_day['info'] = data_day_info
    data_day_info = {}
    all_data['J3'] = data_day
    data_day_period = {}
    data_day = {}
    for p_day in list_period:
        data_day_period['t2m'] = treatment_data(forcast_data_api,type_of_data='temperature_2m',period=p_day,day=3)
        data_day_period['ww'] = treatment_data(forcast_data_api,type_of_data='weather_code',period=p_day,day=3)
        data_day_period['max_wind'] = treatment_data(forcast_data_api,type_of_data='wind_gusts_10m', period=p_day,day=3)
        data_day_period['wind_dir'] = treatment_data(forcast_data_api,type_of_data='wind_direction_10m', period=p_day,day=3)
        data_day[p_day] = data_day_period
        data_day_period = {}

    uv_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=3)
    data_day_info['uv'] = uv_data['max']
    smog_data = treatment_data_somg_and_uv(get_smog_info(city=city),day=3, type_of_data='european_aqi')
    data_day_info['smog'] = smog_data['max']
    sunset = format_date(treatment_day_info(info_data,type_of_data='sunset',day=3))    
    data_day_info['sunset'] = sunset
    sunrise =  format_date(treatment_day_info(info_data,type_of_data='sunrise',day=3))
    data_day_info['sunrise'] =  sunrise
    day_duration = convert(treatment_day_info(info_data,type_of_data='daylight_duration',day=3))
    data_day_info['daylight_duration'] = day_duration
    data_day['info'] = data_day_info
    data_day_period = {}
    data_day_info = {}
    all_data['J4'] = data_day
    forcast_data = all_data

    return forcast_data


list_city = ['ARDENNES','MARNE','AUBE','HAUTE-MARNE','MEUSE','MEURTHE-ET-MOSELLE','MOSELLE','VOSGES','BAS-RHIN','HAUT-RHIN']
list_coord_city = [[49.46,4.43],[49.15,4.10],[48.17,4.08],[48.11,5.13],[49.16,5.38],[48.68,6.20],[49.13,6.16],[48.18,6.45],[48.58,7.75],[47.75,7.33]]

list_city_moselle = ['METZ','THIONVILLE','FORBACH','BITCHE','CHATEAU-SALIN','SARREBOURG','SARREGUEMINE','BOUZONVILLE','FRANCALTROFF'];
list_coord_city_moselle = [
    [49.1193, 6.1757],  
    [49.3611, 6.1644],   
    [49.1883, 6.8978],  
    [49.0486, 7.4267],  
    [48.8353, 6.5167],   
    [48.7372, 7.0547],   
    [49.1125, 7.0694],  
    [49.2822, 6.5178],  
    [49.0208, 6.7025]    
]

list_city_meurthe_et_moselle= ['NANCY','PONT-A-MOUSSON','BACCARAT','SAXON-SION','TOUL','JARNY','VAL-DE-BRIEY','LONGWY','AUDUN-LE-ROMAN','ROZELIEURES']
list_coord_city_meurthe_et_moselle = [
    [48.691, 6.182],   # Nancy
    [48.908, 6.06],    # Pont-à-Mousson
    [48.453, 6.747],   # Baccarat
    [48.428, 6.085],   # Saxon-Sion
    [48.681, 5.893],   # Toul
    [49.158, 5.879],   # Jarny
    [49.259, 5.930],   # Val-de-Briey
    [49.517, 5.761],   # Longwy
    [49.366, 5.894],   # Audun-le-Roman
    [48.451, 6.443]    # Rozelieures
]

list_city_meuse = ['VERDUN','MONTMEDY','ETAIN','CLERMONT-EN-ARGONNE','SPINCOURT','SAINT-MIHIEL','COMMERCY','BAR-LE-DUC','GONDRECOURT-LE-CHATEAU','PAGNY-SUR-MEUSE']
list_coord_city_meuse = [
    [49.160, 5.390],   # Verdun
    [49.518, 5.368],   # Montmédy
    [49.212, 5.619],   #Etain
    [49.105, 5.065],   # Clermont-en-Argonne
    [49.328, 5.566],   # Spincourt
    [48.890, 5.540],   # Saint-Mihiel
    [48.765, 5.590],   # Commercy
    [48.772, 5.152],   # Bar-le-Duc
    [48.513, 5.508],   # Gondrecourt-le-Château
    [48.687, 5.720]    # Pagny-sur-Meuse
]

list_city_vosges = ['EPINAL','REMIREMONT','GERARDMER','SAINT-DIE-DES-VOSGES','CHARMES','MIRECOURT','NEUFCHATEAU','VITTEL','SAINT-JULIEN','PLOMBIERES-LES-BAINS']
list_coord_city_vosges = [
    [48.169, 6.449],    #Epinal
    [48.016, 6.595],    # Remiremont
    [48.072, 6.877],    # Gérardmer
    [48.284, 6.949],    # Saint-Dié-des-Vosges
    [48.371, 6.291],    # Charmes
    [48.314, 6.101],    # Mirecourt
    [48.354, 5.692],    # Neufchâteau
    [48.203, 5.942],    # Vittel
    [48.019, 6.896],    # Saint-Julien
    [47.965, 6.460]     # Plombières-les-Bains
]

list_city_bas_rhin = ['STRASBOURG','HAGUENAU','WISSEMBOURG','SAVERNE','SCHIRMECK','SELESTAT','BARR','RHINAU','SELTZ','PHILIPPSBOURG','SARRE-UNION']
list_coord_city_bas_rhin = [
    [48.581, 7.748],    # Strasbourg
    [48.817, 7.791],    # Haguenau
    [49.036, 7.947],    # Wissembourg
    [48.740, 7.361],    # Saverne
    [48.479, 7.217],    # Schirmeck
    [48.260, 7.454],    # Sélestat
    [48.407, 7.454],    # Barr
    [48.317, 7.704],    # Rhinau
    [48.865, 8.106],    # Seltz
    [48.983, 7.967],     # Philippsbourg
    [48.940, 7.088]     # Sarre-Union
]

list_city_haut_rhin = ['COLMAR','MUNSTER','MULHOUSE','SAINT-LOUIS','FERRETTE','KRUTH','GUEBWILLER','RIBEAUVILLÉ','FESSENHEIM','ROUFFACH']
list_coord_city_haut_rhin = [
    [48.079, 7.352],     # Colmar
    [48.043, 7.130],     # Munster
    [47.747, 7.333],     # Mulhouse
    [47.592, 7.562],     # Saint-Louis
    [47.495, 7.311],     # Ferrette
    [47.929, 6.965],     # Kruth
    [47.907, 7.210],     # Guebwiller
    [48.187, 7.324],     # Ribeauvillé
    [47.900, 7.507],     # Fessenheim
    [47.957, 7.295]      # Rouffach
]

list_city_ardennes = ['CHARLEVILLE-MEZIERES','REVIN','SEDAN','MARGUT','FLEVILLE','RETHEL','LIART','NEUVILLE-LEZ-BEAULIEU','MONTHOIS','BUZANCY']
list_coord_city_ardennes = [
    [49.760, 4.719],     # Charleville-Mézières
    [49.938, 4.832],     # Revin
    [49.699, 4.948],     # Sedan
    [49.585, 5.260],     # Margut
    [49.304, 4.968],     # Fleville
    [49.508, 4.363],     # Rethel
    [49.770, 4.342],     # Liart
    [49.899, 4.346],     # Neuvile-lez-Beaulieu
    [49.317, 4.707],     # Monthois
    [49.426, 4.955]      # Buzancy
]

list_city_marne = ['REIMS','CHALONS-EN-CHAMPAGNE','VITRY-LE-FRANCOIS','SEZANNE','EPERNAY','SAINTE-MENEHOULD','CHARMONT','AUGLURE','MONTMIRAIL','SUIPPES']
list_coord_city_marne = [
    [49.256, 4.029],     # Reims
    [48.953, 4.367],     # Châlons-en-Champagne
    [48.721, 4.584],     # Vitry-le-François
    [48.717, 3.723],     # Sézanne
    [49.044, 3.958],     #Épernay
    [49.082, 4.762],     # Sainte-Menehould
    [48.869, 4.865],     # Charmont
    [48.808, 4.467],     #Auglure
    [48.872, 3.539],     # Montmirail
    [49.130, 4.532]      # Suippes
]

list_city_aube = ['TROYES','ARCIS-SUR-AUBE','DOLANCOURT-NIGLOLAND','BAR-SUR-AUBE','BAR-SUR-SEINE','AUXON','NOGENT-SUR-SEINE','CHESLEY']
list_coord_city_aube = [
    [48.297, 4.075],       # Troyes
    [48.453, 4.140],       #Arcis-sur-Aube
    [48.265, 4.616],       # Dolancourt
    [48.234, 4.718],       # Bar-sur-Aube
    [48.116, 4.376],       # Bar-sur-Seine
    [48.102, 3.918],       #Auxon
    [48.495, 3.497],       # Nogent-sur-Seine
    [47.980, 4.112]        # Chesley
]

list_city_haute_marne = ['CHAUMONT','JOINVILLE','SAINT-DIZIER','CHALVRAINES','VAL-DE-MEUSE','LANGRES','CUSEY','COUPRAY','VILLARS-EN-AZOIS','LA-PORTE-DU-DER']
list_coord_city_haute_marne = [
    [48.111, 5.134],     # Chaumont
    [48.445, 5.143],     # Joinville
    [48.636, 4.950],     # Saint-Dizier
    [48.221, 5.245],     # Chalvraines
    [47.992, 5.550],     # Val-de-Meuse
    [47.865, 5.334],     # Langres
    [47.630, 5.339],     # Cusey
    [47.977, 4.943],     # Coupray
    [48.067, 4.745],     # Villars-en-Azois
    [48.461, 4.847]      # La Porte-du-Der
]
index = 0
def start_forcast(list_city:list,list_coords_city:list,name_dep:str):
    """Parcours les tableaux de données de chaques villes et génère les prévisions associées
    Args:
        list_city (list): Liste des villes 
        list_coords_city (list): liste des tableaux correspondant aux villes
        name_dep (str): Nom du département
    """
    forcast_data = {}
    data_dep = {}
    index = 0
    for coord in list_coords_city:
        print(coord)
        api_data = get_weather_data(city=coord)
        info_data = get_day_info(coord)
        city = list_city[index]
        data_dep[city] = create_forcast_data(city, coord,api_data,info_data=info_data,uv_data=0)
        index += 1
    
    forcast_data = data_dep
    json_data = json.dumps(forcast_data)
    #insert_forcast(json_data, name_dep)
    print(json_data)
  
    
start_forcast(list_city,list_coord_city,'REGION')
# start_forcast(list_city_moselle,list_coord_city_moselle,'MOSELLE')
# start_forcast(list_city_meurthe_et_moselle,list_coord_city_meurthe_et_moselle,'MEURTHE-ET-MOSELLE')
# start_forcast(list_city_meuse,list_coord_city_meuse,'MEUSE')
# start_forcast(list_city_vosges,list_coord_city_vosges,'VOSGES')
# start_forcast(list_city_ardennes,list_coord_city_ardennes,'ARDENNES')
# start_forcast(list_city_marne,list_coord_city_marne,'MARNES')
# start_forcast(list_city_aube,list_coord_city_aube,'AUBE')
# start_forcast(list_city_haute_marne,list_coord_city_haute_marne,'HAUTE-MARNE')
# start_forcast(list_city_bas_rhin,list_coord_city_bas_rhin,'BAS-RHIN')
# start_forcast(list_city_haut_rhin,list_coord_city_haut_rhin,'HAUT-RHIN')
