from conf import main_url, departement_imo, rubrique_imo, nature_imo
# Effectue des requêtes HTTP
import requests
# Analyse le HTML des pages web
from bs4 import BeautifulSoup
# Manipulation de données en json
import json

# Fonction pour scraper la page concernant les bureaux-Coworking 33 & 64
def scraper_page_Bureaux_Coworking(departement_imo, rubrique_imo, nature_imo):
    titres = []  # Initialisation de la liste des titres
    urls = []  # Initialisation de la liste des liens
    prix = []  # Initialisation de la liste des prix
    surface = []  # Initialisation de la liste des surfaces
    page = 1  # Numéro de la page

    base_url = "https://www.cessionpme.com"

    while True:
        url_with_params = f"{main_url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
        page_response = requests.get(url_with_params)
        soup = BeautifulSoup(page_response.text, 'html.parser')
        annonces = soup.find_all('div', class_='offers-list__item')

        if not annonces:  # Si aucune annonce trouvée, c'est la dernière page
            break

        for annonce in annonces:
            titre = annonce.find('h2').text.strip()
            titres.append(titre)

            a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
            if a_element:
                annonce_url = base_url + a_element['href']
                urls.append(annonce_url)

            info_containers = annonce.find_all('div', class_='badge badge--accent-light')

            last_label = None  # Garder une trace du dernier label traité

            for info_container in info_containers:
                label_span = info_container.find('span', class_='badge__label')

                if label_span:
                    label_text = label_span.text.strip()

                    if label_text == "Prix de vente":
                        prix_annonce = info_container.find('span', class_="badge__content__inner")
                        if prix_annonce:
                            prix_text = prix_annonce.text.strip()
                            prix.append(prix_text)
                            last_label = "Prix de vente"
                        else:
                            prix.append("Prix indisponible")
                    elif label_text == "Surface":
                        surface_annonce = info_container.find('span', class_="badge__content__inner")
                        if surface_annonce:
                            surface_text = surface_annonce.text.strip()
                            surface.append(surface_text)
                            last_label = "Surface"
                        else:
                            surface.append("Surface inconnue")
                    else:
                        if last_label == "Prix de vente":
                            prix_annonce = info_container.find('span', class_="badge__content__inner")
                            if prix_annonce:
                                prix_text = prix_annonce.text.strip()
                                prix.append(prix_text)
                        elif last_label == "Surface":
                            surface_annonce = info_container.find('span', class_="badge__content__inner")
                            if surface_annonce:
                                surface_text = surface_annonce.text.strip()
                                surface.append(surface_text)

        page += 1  # Passer à la page suivante

    return titres, urls, prix, surface
   
   
# Fonction pour scraper une page concernant les Locaux, Entrepôts, Terrains 33 & 64
def scraper_page_Locaux_Entrepots_Terrains(departement_imo, rubrique_imo, nature_imo):
    titres = []  # Initialisation de la liste des titres
    urls = []  # Initialisation de la liste des liens
    prix = []  # Initialisation de la liste des prix
    surface = []  # Initialisation de la liste des surfaces
    page = 1  # Numéro de la page

    base_url = "https://www.cessionpme.com"

    while True:
        url_with_params = f"{main_url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo&region_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
        page_response = requests.get(url_with_params)
        soup = BeautifulSoup(page_response.text, 'html.parser')
        annonces = soup.find_all('div', class_='offers-list__item')

        if not annonces:  # Si aucune annonce trouvée, c'est la dernière page
            break

        for annonce in annonces:
            titre = annonce.find('h2').text.strip()
            titres.append(titre)

            a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
            if a_element:
                annonce_url = base_url + a_element['href']
                urls.append(annonce_url)

            info_containers = annonce.find_all('div', class_='badge badge--accent-light')

            last_label = None  # Garder une trace du dernier label traité

            for info_container in info_containers:
                label_span = info_container.find('span', class_='badge__label')

                if label_span:
                    label_text = label_span.text.strip()

                    if label_text == "Prix de vente":
                        prix_annonce = info_container.find('span', class_="badge__content__inner")
                        if prix_annonce:
                            prix_text = prix_annonce.text.strip()
                            prix.append(prix_text)
                            last_label = "Prix de vente"
                        else:
                            prix.append("Prix indisponible")
                    elif label_text == "Surface":
                        surface_annonce = info_container.find('span', class_="badge__content__inner")
                        if surface_annonce:
                            surface_text = surface_annonce.text.strip()
                            surface.append(surface_text)
                            last_label = "Surface"
                        else:
                            surface.append("Surface inconnue")
                    else:
                        if last_label == "Prix de vente":
                            prix_annonce = info_container.find('span', class_="badge__content__inner")
                            if prix_annonce:
                                prix_text = prix_annonce.text.strip()
                                prix.append(prix_text)
                        elif last_label == "Surface":
                            surface_annonce = info_container.find('span', class_="badge__content__inner")
                            if surface_annonce:
                                surface_text = surface_annonce.text.strip()
                                surface.append(surface_text)

        page += 1  # Passer à la page suivante

    return titres, urls, prix, surface


# Appel des fonctions 

# Biens à l'achat, dans le 64 et la rubrique Locaux, Entrepôt, Terrains
titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64 = scraper_page_Locaux_Entrepots_Terrains("93", "2", "V")
for titre, url, prix, surface in zip(titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64):
    print("url:", url)
    print("Titre Locaux, Entrepôts, Terrains - 64: ", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   

# Biens à l'achat, dans le 64 et la rubrique Bureaux, Coworking
titres_bureaux_64, urls_bureaux_64, prix_bureaux_64, surface_bureaux_64 = scraper_page_Bureaux_Coworking("93", "52", "V")
for titre, url, prix, surface in zip(titres_bureaux_64, urls_bureaux_64, prix_bureaux_64, surface_bureaux_64):
    print("Titre Bureaux, Coworking - 64:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
    

# Biens à l'achat, dans le 33 et la rubrique Locaux, Entrepôt, Terrains
titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33 = scraper_page_Locaux_Entrepots_Terrains("87", "2", "V")
for titre, url, prix, surface in zip(titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33):
    print("Titre Locaux, Entrepôts, Terrains - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
  

# Biens à l'achat, dans le 33 et la rubrique Bureaux, Coworking
titres_bureaux_33, urls_bureaux_33, prix_bureaux_33, surface_bureaux_33 = scraper_page_Bureaux_Coworking("87", "52", "V")
for titre, url, prix, surface in zip(titres_bureaux_33, urls_bureaux_33, prix_bureaux_33, surface_bureaux_33):
    print("Titre Bureaux, Coworking - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   


data_64 = {
    "Annonces 'Locaux, Entrepôts, Terrains, 64'": [
        {
            "Titre": titres_locaux_64[i] if i < len(titres_locaux_64) else "",
            "URL": urls_locaux_64[i] if i < len(urls_locaux_64) else "",
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


# Pour le département 64
with open('datas/resultats_64.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_64, json_file, ensure_ascii=False, indent=4)

# Pour le département 33
with open('datas/resultats_33.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_33, json_file, ensure_ascii=False, indent=4)