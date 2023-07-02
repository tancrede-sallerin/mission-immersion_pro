import requests
import json
import unicodedata

# ====> REMARQUE : Les Url ci-dessous sont différentes que celles affichées dans la vidéo.
# C'est normal, continuez bien avec les url de ce fichier
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.codeavecjonathan.com/res/mission/openquizzdb_86.json"),
    #### le lien ci-dessous était érroné 
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124737627/OpenQuizzDB_124/openquizzdb_124.json"),
    ("Cinéma", "Alien", "https://www.codeavecjonathan.com/res/mission/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.codeavecjonathan.com/res/mission/openquizzdb_90.json"),
)


def strip_accents(s):
    """The strip_accents function removes accents from characters in a string using Unicode normalization."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    """The get_quizz_filename function generates a filename for the JSON file based on the quiz's category, 
    title, and difficulty. It uses the strip_accents function to remove accents and replaces spaces with underscores."""
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    """The generate_json_file function takes the quiz's category, title, and URL as parameters. It creates a dictionary
     out_questionnaire_data to hold the quiz data and makes a GET request to the specified URL."""
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    response = requests.get(url)
    data = json.loads(response.text) # The JSON response is loaded into the data variable, and the quiz data is extracted from the "quizz" key.
    all_quizz = data["quizz"]["fr"] # on prrend que le quizz en fr
    # (en-dessous) la clé est (debutant, expert ou confirme) et la valeur (toutes les questions, la reponse, l'anecdote...)
    # Il y a 10 questions (quizz_data) par niveau (quizz_title) - les ids vont jusqu'a 30 en tout ducoup 
    for quizz_title, quizz_data in all_quizz.items(): # The code iterates over each quiz in the all_quizz dictionary. For each quiz, it generates a filename using the get_quizz_filename function and sets the quiz's difficulty level in out_questionnaire_data.
        out_filename = get_quizz_filename(categorie, titre, quizz_title)
        print(out_filename)
        out_questionnaire_data["difficulte"] = quizz_title
        for question in quizz_data:             # question - propositions - choix
            question_dict = {}
            question_dict["titre"] = question["question"] # récupèrre seulement les questions (et pas les anecdotes et tout le bazar)
            question_dict["choix"] = []
            for ch in question["propositions"]: # It then iterates over each question in the quiz and creates a dictionary question_dict to store the question's title and choices. The choices are extracted from the question's "propositions" field, and a tuple is created for each choice, indicating whether it is the correct answer or not.
                question_dict["choix"].append((ch, ch==question["réponse"])) # ajoute les propositions asscociées à un booléen, qui sera True si l'une d'elles est égal à la boone réponse
            out_questions_data.append(question_dict) # The question_dict is added to the out_questions_data list. This list stores all the questions for the quiz.
        out_questionnaire_data["questions"] = out_questions_data # After processing all the questions, the out_questions_data list is assigned to out_questionnaire_data["questions"].
        out_json = json.dumps(out_questionnaire_data) # The out_questionnaire_data dictionary is converted to JSON using json.dumps.

        # The JSON data is written to a file with the generated filename using open, write, and close operations.
        file = open(out_filename, "w")
        file.write(out_json)
        file.close()
        print("end")


# Finally, the code loops through the open_quizz_db_data tuple, which contains the quiz categories, titles, and URLs. 
# It calls the generate_json_file function for each quiz, passing the corresponding data.
for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])

