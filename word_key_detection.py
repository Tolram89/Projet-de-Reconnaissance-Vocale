import os
from datetime import datetime
import requests



def key_word(text):
    resultat=""
    if text.count('météo') >= 1:
        headers = {
            "User-Agent": "mon-assistant-vocal (ton.email@example.com)"
        }

        response = requests.get("https://nominatim.openstreetmap.org/search?q=Dijon&format=json&limit=1", headers=headers)
        data=response.json()
        first_result = data[0]  # Premier élément du tableau
        lon = first_result["lon"]
        lat = first_result["lat"]
        print(lon, lat)
        url = "https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+"&current_weather=true"
        meteo = requests.get(url)
        data_meteo=meteo.json()
        temperature = data_meteo["current_weather"]["temperature"]
        windspeed = data_meteo["current_weather"]["windspeed"]

        resultat= f"La température est de {temperature}°C et la vitesse du vent est de {windspeed} km/h"
        
    if text.count('date') >= 1:
        now = datetime.now()
        match now.month:
            case 1:
                month= "janvier"
            case 2:
                month= "février"
            case 3:
                month= "mars"
            case 4:
                month= "avril"
            case 5:
                month= "mail"
            case 6:
                month= "juin"
            case 7:
                month= "juillet"
            case 8:
                month= "aout"
            case 9:
                month= "septembre"
            case 10:
                month= "octobre"
            case 11:
                month= "novembre"
            case 12:
                month= "décembre"
           
            
        resultat = resultat + "on est le "+str(now.day)+ " " + month
        
    
    if text.count('heure') >= 1 :
        now = datetime.now()
        resultat = resultat +  "il est "+str(now.hour)+" heures et "+str(now.minute)+ " minutes"

    return resultat
        