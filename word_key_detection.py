import os
from datetime import datetime

def key_word(text):
    resultat=""
    if text.count('météo') >= 1:
        print("Vous avez dit : météo")
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
        