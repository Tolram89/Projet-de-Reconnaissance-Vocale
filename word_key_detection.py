from datetime import datetime
import requests
import re
from googletrans import Translator
import asyncio
from langue import lang_map  # Importer le dictionnaire de langues
async def translate_text(texte, dest,src): # Fonction asynchrone qui permet de traduire le texte asynchrone= n'attend pas la fin de la fonction pour continuer l'exécution du programme
    async with Translator() as translator:
        result = await translator.translate(texte, dest, src) 
         # Si le résultat est une liste (plusieurs phrases)
        if isinstance(result, list):    # Vérifie si le résultat est une liste
            return [r.text for r in result]
        else:
            return result.text
        
async def detect_languages(texte):
    async with Translator() as translator:
        result = await translator.detect(texte)
        result = result.lang  # Récupérer le code de la langue détectée
        return result

def extraire_info(phrase_utilisateur):
            texte = phrase_utilisateur.lower() # Convertir le texte en minuscules pour la comparaison
            langue_cible = None  # Initialiser la langue cible à None
            
            # Trouver la langue 
            for langue in lang_map:
                if f"en {langue}" in texte:
                    langue_cible = lang_map[langue]  # Utiliser le code de langue correspondant
                    break
                
            # Extraire le contenu à traduire  avec bibliothèque re
            match1=re.match("traduis-moi", texte)
            match2=re.match("traduis", texte)
            if match1: # Si la phrase commence par "traduis moi"
                match = re.search(r"moi(.*)en(?!.*en)", texte) # Prendre tout entre moi et en 
            elif match2:
                match = re.search(r"traduis(.*)en(?!.*en)",texte) # Si la phrase commence par "traduis"  
            texte_a_traduire = match.group(1)

            
            langue_source=asyncio.run(detect_languages(texte_a_traduire))  # Détecter la langue du texte à traduire
            return texte_a_traduire, langue_cible ,langue_source

def key_word(tag, phrase_utilisateur):
    resultat=""
    langue_cible = "fr"  # Langue par défaut
    if tag == 'meteo':
        headers = {
            "User-Agent": "mon-assistant-vocal (ton.email@example.com)"
        }

        response = requests.get("https://nominatim.openstreetmap.org/search?q=Dijon&format=json&limit=1", headers=headers)
        data=response.json()
        first_result = data[0]  # Premier élément du tableau
        lon = first_result["lon"]#recupere la longitude
        lat = first_result["lat"]# la latitude
        print(lon, lat)
        url = "https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+"&current_weather=true"
        meteo = requests.get(url)
        data_meteo=meteo.json()
        temperature = data_meteo["current_weather"]["temperature"]
        windspeed = data_meteo["current_weather"]["windspeed"]

        resultat = (temperature, windspeed)
        
    if tag == 'date':
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
           
            
        resultat = resultat +str(now.day)+ " " + month
        
    
    if tag == 'heure' :
        now = datetime.now()
        resultat = resultat +str(now.hour)+" heures et "+str(now.minute)+ " minutes"



    if tag == 'traduction':
    
        texte_a_traduire, langue_cible,langue_source = extraire_info(phrase_utilisateur)
        resultat =asyncio.run(translate_text(texte_a_traduire,langue_cible,langue_source))
        
   
    return resultat,langue_cible

