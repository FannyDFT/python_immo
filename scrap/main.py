# Import des variables de configuration
from conf import main_url, departement_imo, rubrique_imo, nature_imo
# Permet d'effectuer des requêtes HTTP
import requests
# Analyse le HTML des pages web
from bs4 import BeautifulSoup
# Manipulation de données en json
import json
# Permet la connexion la BDD
import psycopg2

#Connexion à la bdd PostgreSql
conn = psycopg2.connect(
    host="localhost",
    database="python",
    user="postgres",
    password="postgres"
)

# Permet d'écrire des instructions à la BDD
cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE annonces (
#     id SERIAL PRIMARY KEY,
#     titre VARCHAR(255),
#     url VARCHAR(255) UNIQUE,
#     prix VARCHAR(255),
#     surface VARCHAR(255)
#     )
# """)

# Fonction pour scraper la page concernant les bureaux-Coworking 33 & 64
def scraper_page_Bureaux_Coworking(departement_imo, rubrique_imo, nature_imo):
    titres = []  # Initialisation de la liste des titres
    urls = []  # Initialisation de la liste des liens
    prix = []  # Initialisation de la liste des prix
    surface = []  # Initialisation de la liste des surfaces
    page = 1  # Numéro de la page

    base_url = "https://www.cessionpme.com"

    # Répère la fonction jusqu'à la dernière page à itérer
    while True:
        # url pour extraire les biens concernant la rubrique "Bureau et Coworking"
        url_with_params = f"{main_url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
        # Requête qui récupère le contenu HTTP de la page web
        page_response = requests.get(url_with_params)
        # Analyse le contenu HTML 
        soup = BeautifulSoup(page_response.text, 'html.parser')
        # Récupère tous les éléments HTML correspondant aux annonces
        annonces = soup.find_all('div', class_='offers-list__item')

        if not annonces:  # Si aucune annonce trouvée, c'est la dernière page
            break

        for annonce in annonces: # Itération sur chaque annonces
            titre = annonce.find('h2').text.strip() # Extrait le texte 
            titres.append(titre) # Ajout du texte à la liste des titres

            # Recherche tous les éléments correspondant aux liens
            a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
            if a_element: # Si un lien existe...
                annonce_url = base_url + a_element['href'] # Extraction de l'url
                urls.append(annonce_url) # Ajout de l'url

            # Recherche tous les éléments avec la classe correspondante
            info_containers = annonce.find_all('div', class_='badge badge--accent-light')

            # Variables temporaires
            prix_text = "Prix inconnu"
            surface_text = "Surface inconnue"

            # Pour chaque container ...
            for info_container in info_containers:
                # J'extrait le label ("Prix de vente", "Surface", "Montant au m²")
                label_span = info_container.find('span', class_='badge__label')

                if label_span:
                    # J'extrait le texte de la balise 
                    label_text = label_span.text.strip()

                    if label_text == "Prix de vente":
                        # J'extrait l'élément avec le prix 
                        prix_annonce = info_container.find('span', class_="badge__content__inner")
                        if prix_annonce:
                            # J'extrait le texte
                            prix_text = prix_annonce.text.strip()
                            
                        else:
                            prix.append("Prix indisponible")

                    elif label_text == "Surface":
                        surface_annonce = info_container.find('span', class_="badge__content__inner")
                        if surface_annonce:
                            surface_text = surface_annonce.text.strip()
        
                        else:
                            surface.append("Surface inconnue")

                    elif label_text == "Montant au m²":
                        continue

            # Ajout des valeurs aux listes respectives        
            prix.append(prix_text)
            surface.append(surface_text)   

        page += 1  # Passe à la page suivante

    return titres, urls, prix, surface
   
   
# Fonction pour scraper une page concernant les Locaux, Entrepôts, Terrains 33 & 64
def scraper_page_Locaux_Entrepots_Terrains(departement_imo, rubrique_imo, nature_imo):
    titres = []  
    urls = []  
    prix = [] 
    surface = []  
    page = 1  

    base_url = "https://www.cessionpme.com"

    while True:
        # url pour extraire les biens concernant la rubrique "Locaux, Entrepôts, Terrains"
        url_with_params = f"{main_url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo&region_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
        page_response = requests.get(url_with_params)
        soup = BeautifulSoup(page_response.text, 'html.parser')
        annonces = soup.find_all('div', class_='offers-list__item')

        if not annonces: 
            break

        for annonce in annonces:
            titre = annonce.find('h2').text.strip()
            titres.append(titre)

            a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
            if a_element:
                annonce_url = base_url + a_element['href']
                urls.append(annonce_url)

            info_containers = annonce.find_all('div', class_='badge badge--accent-light')

            prix_text = "Prix inconnu"
            surface_text = "Surface inconnue"

             
            for info_container in info_containers:
                label_span = info_container.find('span', class_='badge__label')

                if label_span:
                    label_text = label_span.text.strip()

                    if label_text == "Prix de vente": 
                        prix_annonce = info_container.find('span', class_="badge__content__inner")
                        if prix_annonce:
                            prix_text = prix_annonce.text.strip()
                        
                        else:
                            prix.append("Prix indisponible")

                    elif label_text == "Surface":
                        surface_annonce = info_container.find('span', class_="badge__content__inner")
                        if surface_annonce:
                            surface_text = surface_annonce.text.strip()
                    
                        else:
                            surface.append("Surface inconnue")
                    
                    elif label_text == "Montant au m²":
                        continue
            
            prix.append(prix_text)
            surface.append(surface_text)
        
        page += 1 

    return titres, urls, prix, surface


# Appel des fonctions 

# Biens à l'achat, dans le 64 et la rubrique "Locaux, Entrepôt, Terrains"
# Appel la fonction avec les paramètres nécessaire, les données récupérées sont stockées dans les variables correspondante
titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64 = scraper_page_Locaux_Entrepots_Terrains("93", "2", "V")
for titre, url, prix, surface in zip(titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64):
    print("Locaux, Entrepôts, Terrains - 64: ", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   

# Biens à l'achat, dans le 64 et la rubrique "Bureaux, Coworking"
titres_bureaux_64, urls_bureaux_64, prix_bureaux_64, surface_bureaux_64 = scraper_page_Bureaux_Coworking("93", "52", "V")
for titre, url, prix, surface in zip(titres_bureaux_64, urls_bureaux_64, prix_bureaux_64, surface_bureaux_64):
    print("Bureaux, Coworking - 64:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
    

# Biens à l'achat, dans le 33 et la rubrique "Locaux, Entrepôt, Terrains"
titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33 = scraper_page_Locaux_Entrepots_Terrains("87", "2", "V")
for titre, url, prix, surface in zip(titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33):
    print("Locaux, Entrepôts, Terrains - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
  

# Biens à l'achat, dans le 33 et la rubrique "Bureaux, Coworking"
titres_bureaux_33, urls_bureaux_33, prix_bureaux_33, surface_bureaux_33 = scraper_page_Bureaux_Coworking("87", "52", "V")
for titre, url, prix, surface in zip(titres_bureaux_33, urls_bureaux_33, prix_bureaux_33, surface_bureaux_33):
    print("Bureaux, Coworking - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   

# Création d'un dictionnaire Python 
# Stocke les données extraite dans les bonnes catégories
data_64 = {
    "Annonces 'Locaux, Entrepôts, Terrains, 64'": [
        {
            "Titre": titres_locaux_64[i] if i < len(titres_locaux_64) else "", # Itère sur les indices `i` de 0 à la longueur de la liste
            "URL": urls_locaux_64[i] if i < len(urls_locaux_64) else "", # Condition pour s'assurer que les indices ne dépassent pas la longueur de la liste
            "Prix": prix_locaux_64[i] if i < len(prix_locaux_64) else "",
            "Surface": surface_locaux_64[i] if i < len(surface_locaux_64) else ""
        }
        for i in range(len(titres_locaux_64))
    ],
    
    "Annonces 'Bureaux Coworking, 64'": [
        {
            "Titre": titres_bureaux_64[i] if i < len(titres_bureaux_64) else "",
            "URL": urls_bureaux_64[i] if i < len(urls_bureaux_64) else "",
            "Prix": prix_bureaux_64[i] if i < len(prix_bureaux_64) else "",
            "Surface": surface_bureaux_64[i] if i < len(surface_bureaux_64) else ""
        }
        for i in range(len(titres_bureaux_64))
    ]
}


data_33 = {
    "Annonces 'Locaux, Entrepôts, Terrains, 33'": [
        {
            "Titre": titres_locaux_33[i] if i < len(titres_locaux_33) else "",
            "URL": urls_locaux_33[i] if i < len(urls_locaux_33) else "",
            "Prix": prix_locaux_33[i] if i < len(prix_locaux_33) else "",
            "Surface": surface_locaux_33[i] if i < len(surface_locaux_33) else ""
        }
        for i in range(len(titres_locaux_33))
    ],
    
    "Annonces 'Bureaux Coworking, 33'": [
        {
            "Titre": titres_bureaux_33[i] if i < len(titres_bureaux_33) else "",
            "URL": urls_bureaux_33[i] if i < len(urls_bureaux_33) else "",
            "Prix": prix_bureaux_33[i] if i < len(prix_bureaux_33) else "",
            "Surface": surface_bureaux_33[i] if i < len(surface_bureaux_33) else ""
        }
        for i in range(len(titres_bureaux_33))
    ]
}


# Ouvre un fichier JSOON pour le département 64 qui contient les données correspondante
with open('datas/resultats_64.json', 'r', encoding='utf-8') as json_file:
    data_64 = json.load(json_file)

# Insérez les données du département 64 dans la table
data_to_insert_64 = [] # Création de la liste pour stocker les informations de la table dans la BDD
for annonce_type, annonces in data_64.items():
    for annonce in annonces: # Pour chaque annonce il extrait les valeurs pour les colonnes
        data_to_insert_64.append((annonce["Titre"], annonce["URL"], annonce["Prix"], annonce["Surface"]))

# Insére les données dans les colonnes correspondante de la table "annonces"
# ON CONFLICT permet d'éviter de dupliquer l'insertion d'une annonce qui exite déjà dans la table en fonction de son URL
cur.executemany("""
    INSERT INTO annonces (titre, url, prix, surface)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING 
""", data_to_insert_64)

# Pour le département 33
with open('datas/resultats_33.json', 'r', encoding='utf-8') as json_file:
    data_33 = json.load(json_file)

# Insérez les données du département 33 dans la table
data_to_insert_33 = []
for annonce_type, annonces in data_33.items():
    for annonce in annonces:
        data_to_insert_33.append((annonce["Titre"], annonce["URL"], annonce["Prix"], annonce["Surface"]))

cur.executemany("""
    INSERT INTO annonces (titre, url, prix, surface)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING
""", data_to_insert_33)


# J'arrête le curseur
cur.close()

# J'enregistre mes nouvelles données insérées 
conn.commit()

# Je ferme la connexion
conn.close()