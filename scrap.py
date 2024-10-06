import requests
from bs4 import BeautifulSoup
import csv
import time

# Fonction pour extraire les informations d'un ebook donné
def extract_book_info(book_id):
    url = f"http://www.gutenberg.org/ebooks/{book_id}"
    response = requests.get(url)

    # Vérification si la requête est un succès
    if response.status_code != 200:
        print(f"Failed to fetch book ID {book_id}, Status code: {response.status_code}")
        return None

    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        # Extraire l'auteur
        author = soup.find('a', {'rel': 'marcrel:aut'}).text.strip() if soup.find('a', {'rel': 'marcrel:aut'}) else "Unknown"

        # Extraire le titre
        title = soup.find('h1').text.strip() if soup.find('h1') else "No Title"

        # Extraire la note
        note_section = soup.find('tr', string="Note")
        note = note_section.find_next('td').text.strip() if note_section else "No Note"

        # Extraire le résumé
        summary_section = soup.find('tr', string="Summary")
        summary = summary_section.find_next('td').text.strip() if summary_section else "No Summary"

        # Extraire la langue
        language = soup.find('td', {'itemprop': 'inLanguage'}).text.strip() if soup.find('td', {'itemprop': 'inLanguage'}) else "Unknown"

        # Extraire les classes LoC (Library of Congress)
        loc_classes = [loc.text for loc in soup.find_all('a', href=True) if "/browse/loccs/" in loc['href']]

        # Extraire les sujets
        subjects = [subject.text for subject in soup.find_all('a', href=True) if "/ebooks/subject/" in subject['href']]

        # Extraire la catégorie
        category_section = soup.find('tr', string="Category")
        category = category_section.find_next('td').text.strip() if category_section else "No Category"

        # Extraire le numéro d'eBook
        ebook_no_section = soup.find('tr', string="EBook-No.")
        ebook_no = ebook_no_section.find_next('td').text.strip() if ebook_no_section else str(book_id)

        # Extraire la date de publication
        release_date_section = soup.find('tr', string="Release Date")
        release_date = release_date_section.find_next('td').text.strip() if release_date_section else "No Release Date"

        # Extraire la dernière date de mise à jour
        updated_date_section = soup.find('tr', string="Most Recently Updated")
        updated_date = updated_date_section.find_next('td').text.strip() if updated_date_section else "No Update Date"

        # Extraire le statut de copyright
        copyright_section = soup.find('tr', string="Copyright Status")
        copyright_status = copyright_section.find_next('td').text.strip() if copyright_section else "Unknown"

        return [author, title, note, summary, language, ', '.join(loc_classes), ', '.join(subjects), category, ebook_no, release_date, updated_date, copyright_status]

    except Exception as e:
        print(f"Error extracting data for book ID {book_id}: {e}")
        return None

# Initialiser le fichier CSV
with open('gutenberg_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Écrire les en-têtes de colonnes
    writer.writerow(["Author", "Title", "Note", "Summary", "Language", "LoC Classes", "Subjects", "Category", "EBook-No.", "Release Date", "Most Recently Updated", "Copyright Status"])

    # Boucle sur 5000 ebooks
    for book_id in range(1, 5001):
        print(f"Processing book ID: {book_id}")
        book_info = extract_book_info(book_id)

        # Si l'extraction est réussie, ajouter les informations dans le fichier CSV
        if book_info:
            writer.writerow(book_info)
        else:
            print(f"Skipping book ID: {book_id} due to missing data.")