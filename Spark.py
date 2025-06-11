import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_listings(page_url):
    """
    Extrae título, precio y ubicación de las propiedades en una página.
    Ajusta los selectores CSS según la estructura del sitio real.    """
    resp = requests.get(page_url)
    resp.raise_for_status()
    
    # Guardar el HTML en un archivo local
    if 'pagina' in page_url:
        page_number = page_url.split('pagina')[-1]
        html_filename = f"html_response_pagina{page_number}.html"
    else:
        html_filename = "html_response_pagina1.html"
    
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(resp.text)
    # print(f"HTML guardado en: {html_filename}")
    
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
            # Extraer barrio del título
            neighborhood = "N/A"
            if title != "N/A":
                # Patrones para extraer barrio: "en [Barrio]," o "en [Barrio], Tunja"
                neighborhood_patterns = [
                    r'Venta\s+en\s+([^,]+),\s*Tunja',  # "Venta en La calleja, Tunja"
                    r'venta\s+en\s+([^,]+),\s*Tunja',  # "venta en La calleja, Tunja" 
                    r'en\s+([^,]+),\s*Tunja',          # "en La calleja, Tunja"
                    r'en\s+([^,]+),',                  # "en Centro,"
                ]
                
                for pattern in neighborhood_patterns:
                    match = re.search(pattern, title, re.IGNORECASE)
                    if match:
                        potential_neighborhood = match.group(1).strip()
                        
                        # Filtrar palabras que no son barrios
                        exclude_words = ['venta', 'tunja', 'casa', 'apartamento']
                        clean_neighborhood = potential_neighborhood.lower()
                        
                        # Verificar que no contenga palabras excluidas
                        is_valid = True
                        for exclude_word in exclude_words:
                            if exclude_word in clean_neighborhood:
                                is_valid = False
                                break
                        
                        if is_valid and len(potential_neighborhood) > 1:
                            # Aplicar Pascal case (Primera letra de cada palabra en mayúscula)
                            neighborhood = potential_neighborhood.title()
                            break
            
            # Extraer características (habitaciones, baños, área)
            typology_elem = card.select_one(".lc-typologyTag")
            rooms = bathrooms = area = "N/A"
            if typology_elem:
                typology_text = typology_elem.get_text()
                # Extraer habitaciones
                rooms_match = re.search(r'(\d+)\s*Habs', typology_text)
                rooms = rooms_match.group(1) if rooms_match else "N/A"
                
                # Extraer baños
                bathrooms_match = re.search(r'(\d+)\s*Baños', typology_text)
                bathrooms = bathrooms_match.group(1) if bathrooms_match else "N/A"
                
                # Extraer área
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
    base_url = "https://www.fincaraiz.com.co/venta/casas/tunja/boyaca"
    all_listings = []
    
    # Scrapear 5 páginas para obtener más propiedades
    for page in range(1, 6):
        if page == 1:
            # Primera página usa la URL base
            url = base_url
        else:
            # Páginas adicionales usan el formato /paginaX
            url = f"{base_url}/pagina{page}"
        
        # print(f"Scrapeando página {page}: {url}...")
        try:
            page_listings = scrape_listings(url)
            all_listings += page_listings
            # print(f"  -> {len(page_listings)} propiedades encontradas en página {page}")
        except Exception as e:
            print(f"Error scrapeando página {page}: {e}")
        
        # Pausa entre páginas para respetar el servidor
        time.sleep(2)
    
    # Guardar a CSV
    df = pd.DataFrame(all_listings)
    df.to_csv("propiedades.csv", index=False, encoding="utf-8")
    print(f"\n✅ Total: {len(df)} anuncios guardados en propiedades.csv")
    
    # Mostrar resumen de los datos extraídos
    """
    if len(df) > 0:
        print(f"\nResumen de datos extraídos:")
        print(f"- Precio promedio: ${df['price'].mean():,.0f}")
        print(f"- Precio mínimo: ${df['price'].min():,.0f}")
        print(f"- Precio máximo: ${df['price'].max():,.0f}")
        print(f"- Ubicaciones encontradas: {df['location'].nunique()}")
        print(f"- Inmobiliarias encontradas: {df['publisher'].nunique()}")
    """

if __name__ == "__main__":
    main()
