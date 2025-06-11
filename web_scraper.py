import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
import argparse

# Configuración de argumentos
parser = argparse.ArgumentParser(description='Scraper de propiedades de fincaraiz.com.co')
parser.add_argument('-p', '--pages', type=int, default=5,
                    help='Número de páginas a scrapear (por defecto: 5)')
parser.add_argument('-s', '--single', action='store_true',
                    help='Scrapear solo la primera página')
parser.add_argument('-u', '--url', type=str, default="https://www.fincaraiz.com.co/venta/casas/tunja/boyaca",
                    help='URL base para scraping')
args = parser.parse_args()

# Ajustar número de páginas según parámetros
if args.single:
    total_pages = 1
else:
    total_pages = args.pages

def scrape_listings(page_url):
    """
    Extrae título, precio y ubicación de las propiedades en una página.
    Ajusta los selectores CSS según la estructura del sitio real.
    """
    resp = requests.get(page_url)
    resp.raise_for_status()

    # Crear carpeta scrapped_data si no existe
    os.makedirs('scrapped_data', exist_ok=True)

    # Guardar el HTML en un archivo local
    if 'pagina' in page_url:
        page_number = page_url.split('pagina')[-1]
        html_filename = f"scrapped_data/pagina{page_number}.html"
    else:
        html_filename = "scrapped_data/pagina1.html"

    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(resp.text)

    soup = BeautifulSoup(resp.text, "html.parser")

    listings = []
    for card in soup.select(".listingCard"):
        try:
            # Extraer título
            title_elem = card.select_one(".lc-title")
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            # Extraer precio
            price_elem = card.select_one(".price strong")
            price_text = price_elem.get_text(strip=True) if price_elem else "0"
            # Limpiar precio: remover $ y puntos/comas
            price_clean = price_text.replace("$", "").replace(".", "").replace(",", "").strip()
            price = float(price_clean) if price_clean.isdigit() else 0

            # Extraer ubicación
            location_elem = card.select_one(".lc-location")
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            # Extraer barrio del título y ubicación
            neighborhood = "N/A"
            if title != "N/A":
                # Patrones para extraer barrio del título
                patterns = [
                    r'(?i)(?:Venta|Casa|Apartamento)[^,]*en\s+([^,]+?)(?:,|$)',  # "Venta en La calleja" o "Casa en Centro"
                    r'(?i)en\s+([^,]+?)(?:,|$)',  # "en La calleja"
                    r'(?i)(?:Barrio|Sector|Sector de|Zona de)\s+([^,]+?)(?:,|$)'  # "Barrio Centro"
                ]
                
                # Primero intentamos extraer del título
                for pattern in patterns:
                    match = re.search(pattern, title)
                    if match:
                        potential = match.group(1).strip()
                        if len(potential) > 2:  # Asegurarse que no sea muy corto
                            neighborhood = potential
                            break
                
                # Si no se encontró en el título, intentamos con la ubicación
                if neighborhood == "N/A" and location_elem:
                    location_text = location_elem.get_text(strip=True)
                    # Buscar el barrio después de la última coma (asumiendo formato: Ciudad, Barrio, Dirección)
                    parts = [p.strip() for p in location_text.split(',') if p.strip()]
                    if len(parts) >= 2:
                        potential = parts[-2]  # El penúltimo elemento suele ser el barrio
                        if len(potential) > 2:
                            neighborhood = potential
                
                # Limpieza final del barrio
                if neighborhood != "N/A":
                    # Eliminar solo palabras específicas no deseadas, manteniendo los artículos
                    stop_words = {'venta', 'casa', 'apartamento', 'tunja', 'en', 'de'}
                    
                    # Limpiar saltos de línea y espacios múltiples
                    neighborhood = ' '.join(neighborhood.split())
                    
                    # Separar palabras manteniendo su posición
                    words = neighborhood.split()
                    cleaned_words = []
                    
                    # Mantener artículos cuando son parte del nombre del barrio
                    i = 0
                    while i < len(words):
                        word = words[i].lower()
                        
                        # Si la palabra es un artículo y hay una siguiente palabra, juntarlas
                        if word in {'la', 'el', 'los', 'las', 'del'} and i + 1 < len(words):
                            # Unir el artículo con la siguiente palabra
                            combined = f"{words[i]} {words[i+1]}"
                            cleaned_words.append(combined)
                            i += 2  # Saltar la siguiente palabra ya que la incluimos
                        elif word not in stop_words:
                            cleaned_words.append(words[i])
                            i += 1
                        else:
                            i += 1
                    
                    neighborhood = ' '.join(cleaned_words)
                    
                    # Aplicar formato de título (primera letra mayúscula)
                    neighborhood = neighborhood.title()
                    
                    # Limpiar caracteres especiales al inicio/final
                    neighborhood = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', neighborhood)
                    
                    # Si después de la limpieza queda vacío, volver a N/A
                    if not neighborhood.strip():
                        neighborhood = "N/A"

            # Extraer características
            typology_elem = card.select_one(".lc-typologyTag")
            rooms = bathrooms = area = "N/A"
            if typology_elem:
                typology_text = typology_elem.get_text()
                rooms_match = re.search(r'(\d+)\s*Habs', typology_text)
                rooms = rooms_match.group(1) if rooms_match else "N/A"

                bathrooms_match = re.search(r'(\d+)\s*Baños', typology_text)
                bathrooms = bathrooms_match.group(1) if bathrooms_match else "N/A"

                area_match = re.search(r'(\d+)\s*m²', typology_text)
                area = area_match.group(1) if area_match else "N/A"

            # Extraer inmobiliaria
            publisher_elem = card.select_one(".publisher strong")
            publisher = publisher_elem.get_text(strip=True) if publisher_elem else "N/A"

            # Extraer URL de la propiedad
            link_elem = card.select_one("a[href*='/casa-en']")
            property_url = "https://www.fincaraiz.com.co" + link_elem['href'] if link_elem else "N/A"

            listings.append({
                "title": title,
                "price": price,
                "location": location,
                "neighborhood": neighborhood,
                "rooms": rooms,
                "bathrooms": bathrooms,
                "area_m2": area,
                "publisher": publisher,
                "url": property_url
            })

        except Exception as e:
            print(f"Error procesando una propiedad: {e}")
            continue

    return listings

def main():
    all_listings = []
    os.makedirs('files/csv', exist_ok=True)

    print(f"Scrapeando {total_pages} página(s) desde: {args.url}")

    for page in range(1, total_pages + 1):
        url = f"{args.url}/pagina{page}" if page > 1 else args.url

        print(f"Scrapeando página {page}: {url}...")
        try:
            page_listings = scrape_listings(url)

            if page_listings:
                df_page = pd.DataFrame(page_listings)
                csv_filename = f"files/csv/propiedades_pagina_{page}.csv"
                df_page.to_csv(csv_filename, index=False, encoding="utf-8")
                print(f"  -> {len(page_listings)} propiedades guardadas en {csv_filename}")
                all_listings += page_listings

        except Exception as e:
            print(f"Error scrapeando página {page}: {e}")

        time.sleep(2)

    if all_listings:
        df_all = pd.DataFrame(all_listings)
        output_file = "files/propiedades_todas.csv"
        df_all.to_csv(output_file, index=False, encoding="utf-8")
        print(f"\n✅ Total: {len(df_all)} anuncios guardados en {output_file}")
    else:
        print("No se encontraron propiedades para guardar.")

if __name__ == "__main__":
    main()