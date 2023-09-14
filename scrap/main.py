from conf import url, departement_imo, rubrique_imo, nature_imo
import requests
from bs4 import BeautifulSoup

# Fonction pour scraper la page concernant les bureaux-Coworking 33 & 64
def scraper_page_Bureaux_Coworking(departement_imo, rubrique_imo, nature_imo, page):
    titres = []  # Initialisation de la liste des titres
    urls = []  # Initialisation de la liste des liens
    prix = [] # Initialisation de la liste des prix
    surface = [] # Initialisation de la liste des surfaces
    # page = 1
    # while True:

    # Défintion de l'url de base
    base_url = "https://www.cessionpme.com"
    # Défintion de l'url comprenant les paramètres
    url_with_params = f"{url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
    # Import de la page HTML 
    page = requests.get(url_with_params)
    # Création d'un nouvel objet
    soup = BeautifulSoup(page.text, 'html.parser')
    # Extraction de toutes les annonces concernant la page
    annonces = soup.find_all('div', class_='offers-list__item')

    for annonce in annonces:
        # Titres
        titre = annonce.find('h2').text.strip()
        titres.append(titre)

        # URL
        # Extraction du lien 
        if annonce:
             a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
        if a_element:
             annonce_url = base_url + a_element['href']
             urls.append(annonce_url)

         # Balise contenant les informations (prix ou surface)
        info_containers = annonce.find_all('div', class_='badge badge--accent-light')

        for info_container in info_containers:
            # Balise contenant le label ("Prix de vente" ou "Surface")
            if info_container:
                label_span = info_container.find('span', class_='badge__label')

            if label_span:
                label_text = label_span.text.strip()
                # Si le label indique "Prix de vente", c'est le prix
                if label_text == "Prix de vente":
                    prix_annonce = info_container.find('span', class_="badge__content__inner")
                    if prix_annonce:
                        prix_text = prix_annonce.text.strip()
                        prix.append(prix_text)
                    else:
                        prix.append("Prix indisponible")
                # Si le label indique "Surface", c'est la surface
                elif label_text == "Surface":
                    surface_annonce = info_container.find('span', class_="badge__content__inner")
                    if surface_annonce:
                        surface_text = surface_annonce.text.strip()
                        surface.append(surface_text)
                    else:
                        surface.append("Surface inconnue")
        else:
            prix.append("Prix indisponible")
            surface.append("Surface inconnue")

    return titres, urls, prix, surface
   
   
# Fonction pour scraper une page concernant les Locaux, Entrepôts, Terrains 33 & 64
def scraper_page_Locaux_Entrepots_Coworking(departement_imo, rubrique_imo, nature_imo, page):
    titres = []  # Initialisation de la liste des titres
    urls = []  # Initialisation de la liste des liens
    prix = [] # Initialisation de la liste des prix
    surface = [] # Initialisation de la liste des surfaces
    # page = 1
    # while True:

    # Défintion de l'url de base
    base_url = "https://www.cessionpme.com"
    # Défintion de l'url comprenant les paramètres
    url_with_params = f"{url}/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo={nature_imo}&rubrique_imo&region_imo={rubrique_imo}&region_imo=2&departement_imo={departement_imo}&commune_imo=0&multiple_lieu_imo&trap_imo&secteur_activite_imo&ou_imo=Pyr%25E9n%25E9es%20Atlantiques%20%252864%2529&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo&page={page}"
    # Import de la page HTML
    page = requests.get(url_with_params)
    # Création d'un nouvel objet
    soup = BeautifulSoup(page.text, 'html.parser')
    # Extraction de toutes les annonces concernant la page
    annonces = soup.find_all('div', class_='offers-list__item')
  

    for annonce in annonces:
        # Titres
        titre = annonce.find('h2').text.strip()
        titres.append(titre)

        # URL
        # Extraction du lien 
        if annonce:
            a_element = annonce.find('a', class_='button card offer-card offer-card-list btn btn--link card--bordered')
        if a_element:
            annonce_url = base_url + a_element['href']
            urls.append(annonce_url)

        # Balise contenant les informations (prix ou surface)
        info_containers = annonce.find_all('div', class_='badge badge--accent-light')

        for info_container in info_containers:
            # Balise contenant le label ("Prix de vente" ou "Surface")
            if info_container:
                label_span = info_container.find('span', class_='badge__label')

            if label_span:
                label_text = label_span.text.strip()
                # Si le label indique "Prix de vente", c'est le prix
                if label_text == "Prix de vente":
                    prix_annonce = info_container.find('span', class_="badge__content__inner")
                    if prix_annonce:
                        prix_text = prix_annonce.text.strip()
                        prix.append(prix_text)
                        print("prix:", prix)
                    else:
                        prix.append("Prix indisponible")
                # Si le label indique "Surface", c'est la surface
                elif label_text == "Surface":
                    surface_annonce = info_container.find('span', class_="badge__content__inner")
                    if surface_annonce:
                        surface_text = surface_annonce.text.strip()
                        surface.append(surface_text)
                    else:
                        surface.append("Surface inconnue")
        else:
            prix.append("Prix indisponible")
            surface.append("Surface inconnue")
                
    

    return titres, urls, prix, surface


# Appel des fonctions 

# Biens à l'achat, dans le 64 et la rubrique Locaux, Entrepôt, Terrains
titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64 = scraper_page_Locaux_Entrepots_Coworking("93", "2", "V", 1)
for titre, url, prix, surface in zip(titres_locaux_64, urls_locaux_64, prix_locaux_64, surface_locaux_64):
    print("Titre Locaux, Entrepôts, Terrains - 64: ", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   

# Biens à l'achat, dans le 64 et la rubrique Bureaux, Coworking
titres_bureaux_64, urls_bureaux_64, prix_locaux_64, surface_locaux_64 = scraper_page_Bureaux_Coworking("93", "52", "V", 1)
for titre, url, prix, surface in zip(titres_bureaux_64, urls_bureaux_64, prix_locaux_64, surface_locaux_64):
    print("Titre Bureaux, Coworking - 64:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
    

# Biens à l'achat, dans le 33 et la rubrique Locaux, Entrepôt, Terrains
titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33 = scraper_page_Locaux_Entrepots_Coworking("87", "2", "V", 1)
for titre, url, prix, surface in zip(titres_locaux_33, urls_locaux_33, prix_locaux_33, surface_locaux_33):
    print("Titre Locaux, Entrepôts, Terrains - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
  

# Biens à l'achat, dans le 33 et la rubrique Bureaux, Coworking
titres_bureaux_33, urls_bureaux_33, prix_locaux_33, surface_locaux_33 = scraper_page_Bureaux_Coworking("87", "52", "V", 1)
for titre, url, prix, surface in zip(titres_bureaux_33, urls_bureaux_33, prix_locaux_33, surface_locaux_33):
    print("Titre Bureaux, Coworking - 33:", titre, "URL de l'annonce:", url, "Prix:", prix, "Surface:", surface)
   
   

print("Hello")