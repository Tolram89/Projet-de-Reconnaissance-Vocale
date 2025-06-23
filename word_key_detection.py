from datetime import datetime
import requests
from googletrans import Translator
import asyncio
from langue import lang_map  # Importer le dictionnaire de langues
import spacy
from vocal_retranscription import assistant_speech
import dateparser
import re
import string

try:
    NER = spacy.load("fr_core_news_md")
except OSError:
    import spacy.cli
    print("Le modèle spaCy 'fr_core_news_md' n'est pas installé. Téléchargement en cours...")
    spacy.cli.download("fr_core_news_md")
    NER = spacy.load("fr_core_news_md")#Named Enitity Recognition

def recup_ville(phrase_utilisateur) :
    ville = "dijon" #met dijon de base
    doc = NER(phrase_utilisateur)
    for word in doc.ents:#permet de recuperer la ville dans la phrase
        ville = word.text
    return ville
def couper_phrase(mot, phrase_utilisateur):
    date_phrase = re.split(mot, phrase_utilisateur)[1]#récupere ce qu'il ya apres du
    if re.search(r"à", date_phrase) :
        date_phrase = re.split("à", date_phrase)[0] # empeche les bugs quans on demande une ville apres la date
    for punctuation in string.punctuation:
        date_phrase = date_phrase.replace(punctuation, "")#enlève la ponctuation
    start_date = dateparser.parse(date_phrase, languages=["fr"]) #récupere la date et
    start_date = start_date.strftime("%Y-%m-%d")
    return date_phrase, start_date

def recup_date(phrase_utilisateur) :
    try:
        if re.search(r"demain", phrase_utilisateur) : #demain
            start_date = dateparser.parse("demain", languages=["fr"]) #récupere la date et
            date_phrase = "demain"
            start_date = start_date.strftime("%Y-%m-%d")

        elif re.search(r" du ", phrase_utilisateur) : #du 20 juin
            date_phrase, start_date = couper_phrase(" du ", phrase_utilisateur)

        elif re.search(r" le ", phrase_utilisateur) : # le 20 juin
            date_phrase, start_date = couper_phrase(" le ", phrase_utilisateur)

        elif re.search(r" ce ", phrase_utilisateur) : # ce 20 juin
            date_phrase, start_date = couper_phrase(" ce ", phrase_utilisateur)
        elif re.search(r" pour ", phrase_utilisateur) : # pour le 20 juin
            date_phrase, start_date = couper_phrase("pour", phrase_utilisateur)
            

        else :
            start_date = datetime.now().strftime("%Y-%m-%d")#par défaut
            date_phrase = "aujourd'hui"
    
        end_date = start_date
    except:#gere quand un utilisateur dit ce weekend ou samedi que le programme ne comprend pas pour lui permettre de reformuler correctement
        assistant_speech("Désolé, je ne comprends pas les expressions comme ce weekend, samedi, etc. Veuillez donner une date exacte comme 20 juin, merci.", "fr")
        return None, None, None

    return start_date, end_date, date_phrase

def recup_meteo(lat, lon, start_date, end_date, ville, date_phrase):
    today_str = datetime.now().strftime("%Y-%m-%d")

    if start_date==today_str or date_phrase == "demain":
        # Si la date demandée est aujourd'hui ou demain
        #On récupère la température actuelle avec current_weather
        url = "https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+"&current_weather=true"
        meteo = requests.get(url)
        data_meteo=meteo.json()
        temperature = data_meteo["current_weather"]["temperature"]
        #On récupère aussi les prévisions min/max pour la journée
        url = "https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&start_date="+str(start_date)+"&end_date="+str(end_date)+"&timezone=Europe/Paris"
        meteo = requests.get(url)
        data_meteo=meteo.json()
        temperature_max = data_meteo["daily"]["temperature_2m_max"][0]
        temperature_min = data_meteo["daily"]["temperature_2m_min"][0]
        #On construit une phrase complète avec la température actuelle et les prévisions
        phrase = "{} à {}, il fait actuellement {}°C. Les températures prévues sont entre {}°C et {}°C.".format(date_phrase, ville, temperature, temperature_min, temperature_max)
    else :
        # Si la date demandée est une date future (autre que aujourd'hui/demain)
        # on récupère uniquement les prévisions min/max pour cette date
        url = "https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(lon)+"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&start_date="+str(start_date)+"&end_date="+str(end_date)+"&timezone=Europe/Paris"
        meteo = requests.get(url)
        data_meteo=meteo.json()
        temperature_max = data_meteo["daily"]["temperature_2m_max"][0]
        temperature_min = data_meteo["daily"]["temperature_2m_min"][0]
        # on construit une phrase avec uniquement les prévisions
        phrase = "Ce {} à {}, les températures prévues sont entre {}°C et {}°C.".format(date_phrase, ville, temperature_min, temperature_max)
    return phrase
    


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

def recup_calcul(phrase_utilisateur):
    texte = phrase_utilisateur.lower()  # Convertir la phrase en minuscules pour la comparaison
    # On utilise eval pour évaluer l'expression mathématique
    try:
        match1= re.match("calcule-moi", texte)  # Si la phrase commence par "calcule moi"
        match2= re.match("calcule", texte)  # Si la phrase commence par "calcule"
        match3= re.match("fais le calcul", texte)  # Si la phrase commence par "fais le calcul"
        match4= re.match("resous moi", texte)  # Si la phrase commence par "resous moi"
        mathc5 = re.match("fais moi", texte)  # Si la phrase commence par "fais moi"

        if match1:  # Si la phrase commence par "calcule moi"
            expression = re.search(r"calcule-moi(.*)", texte).group(1)  # Récupérer l'expression après "moi"*
        elif match2:  # Si la phrase commence par "calcule"
            expression = re.search(r"calcule(.*)", texte).group(1)  # Récupérer l'expression après "calcule"
        elif match3:  # Si la phrase commence par "fais le calcul"
            expression = re.search(r"le calcul(.*)", texte).group(1)
        elif match4:  # Si la phrase commence par "resous moi"
            expression = re.search(r"résous-moi(.*)", texte).group(1)  # Récupérer l'expression après "resous moi"
        elif mathc5:  # Si la phrase commence par "fais moi"
            expression = re.search(r"fais-moi(.*)", texte).group(1)  # Récupérer l'expression après "fais moi"

        match6 = re.findall(r"x", texte)  # recherche tout les x de l'expression
        
        if match6:
            for x in match6:  # Si on trouve des 'x' dans l'expression
                expression = re.sub(r"x", "*",expression)  # Remplacer 'x' par '*' pour les multiplications        
        resultat = eval(expression)  # Évaluer l'expression mathématique    
        return expression , resultat  # Retourner l'expression et le résultat
    except Exception as e:
        return "Désolé, je n'ai pas pu comprendre le calcul. Veuillez reformuler."

def key_word(tag, phrase_utilisateur):
    resultat=""
    langue_cible = "fr"  # Langue par défaut

    if tag == 'meteo':
        headers = {
            "User-Agent": "mon-assistant-vocal (ton.email@example.com)"
        }
        assistant_speech("D'accord, je récupère la météo", langue_cible)
        ville = recup_ville(phrase_utilisateur) # recup la ville
        response = requests.get(f"https://nominatim.openstreetmap.org/search?q={ville}&format=json&limit=1", headers=headers)
        data=response.json()
        first_result = data[0]  # Premier élément du tableau
        lon = first_result["lon"]#recupere la longitude
        lat = first_result["lat"]# la latitude
        print(lon, lat)
        start_date, end_date, date_phrase = recup_date(phrase_utilisateur)
        if start_date ==None:
            resultat == None
        else :
            resultat = recup_meteo(lat, lon, start_date, end_date, ville, date_phrase)
        
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
        

    if tag == 'calculette':
        # On utilise eval pour évaluer l'expression mathématique
        expression, resultat = recup_calcul(phrase_utilisateur)
        resultat ="le résultat de " + expression + " est " + str(resultat)

    return resultat,langue_cible