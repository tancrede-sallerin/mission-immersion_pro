# PROJET QUESTIONNAIRE V3 : POO
#
# - Pratiquer sur la POO
# - Travailler sur du code existant
# - Mener un raisonnement
#
# -> Définir les entitées (données, actions)
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#


import json
import sys  # pour passer le nom du questionnaire json en ligne de commande



class Question:
    def __init__(self, titre, choix):
        self.titre = titre
        self.choix = choix

    def FromData(data):
        # ....
        q = Question(data[2], data[0], data[1])
        return q

    def poser(self, n_question):
        """poser() : affiche la question ainsi que les choix de réponses possibles. Elle demande ensuite à l'utilisateur
         de saisir sa réponse et vérifie si la réponse est correcte en comparant la réponse de l'utilisateur avec la 
         bonne réponse. La méthode retourne un booléen indiquant si la réponse est correcte ou non."""
        print("QUESTION", n_question)
        print("  " + self.titre)
        bonne_reponse = ""
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i][0])  ##le premier des 2 éléments
            if self.choix[i][1]:   # trouver la bonne réponse
                bonne_reponse = self.choix[i][0]

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1][0].lower() == bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        '''Eviter les erreurs liées au réponses immpossibles : on ne veut que des nombres compris entre 1 et le 
        nombre total de question'''
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions):
        self.questions = questions

    def lancer(self):
        score = 0
        compteur = 0
        for question in self.questions:
            compteur += 1
            if question.poser(str(compteur)+"/"+str(len(self.questions))):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


"""Questionnaire(
    (
    Question("Quelle est la capitale de la France ?", (("Marseille", False), "Nice", "Paris", "Nantes", "Lille")), 
    Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"))
    )
).lancer()"""

# On veut un tuple de questions

def extraire_questions_du_fichier_json(chemin):
    """Fonction qui récupère les questions du fichier json puis qui lance le questionnaire"""
    with open(chemin) as f:
        data = json.load(f) 
    
    print("\n"*3)  
    print("*"*100)
    print("Questionnnaire:", data['titre'], "- Catégorie:", data['categorie'], "- difficulté:", data['difficulte'])
    print("*"*100, "\n")
    questions_pretes = [Question(data['questions'][i]['titre'], data['questions'][i]['choix']) for i in range(10)]
    return Questionnaire(questions_pretes).lancer()
    

# lancer le script
# pour qu'il y ait bien 2 arguments quand on veut lancer le onm de notre script : questionnaire.py et le nom qu fichier json
if len(sys.argv) > 2:
    print("ERROR: vous devez spécifier le nom du fichier json à charger")
    exit(0)
json_filename = sys.argv[1]
extraire_questions_du_fichier_json(json_filename)
