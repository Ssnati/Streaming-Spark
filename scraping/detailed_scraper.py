import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json
from datetime import datetime

def scrape_property_details(property_url):
    """
    Extrae detalles completos de una propiedad individual.
    Devuelve más información para alimentar Spark Streaming.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resp = requests.get(property_url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Extraer información detallada
        details = {
            "url": property_url,
            "timestamp": datetime.now().isoformat(),
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Título principal
        title_elem = soup.select_one("h1, .property-title, .listing-title")
        details["title"] = title_elem.get_text(strip=True) if title_elem else "N/A"
        
        # Precio
        price_selectors = [".price", ".property-price", "[class*='price']", ".valor"]
        price_elem = None
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                break
        
        if price_elem:
            price_text = price_elem.get_text()
            price_clean = re.sub(r'[^\d]', '', price_text)
            details["price"] = int(price_clean) if price_clean.isdigit() else 0
        else:
            details["price"] = 0
        
        # Ubicación detallada
        location_selectors = [".location", ".address", ".direccion", "[class*='location']"]
        location_elem = None
        for selector in location_selectors:
            location_elem = soup.select_one(selector)
            if location_elem:
                break
        details["location"] = location_elem.get_text(strip=True) if location_elem else "N/A"
        
        # Características de la propiedad
        characteristics = {}
        
        # Buscar características en diferentes formatos
        char_patterns = [
            (r'(\d+)\s*(?:habitaciones?|habs?|rooms?)', 'rooms'),
            (r'(\d+)\s*(?:baños?|bathrooms?)', 'bathrooms'),
            (r'(\d+)\s*m[²2]', 'area_m2'),
            (r'(\d+)\s*(?:pisos?|floors?)', 'floors'),
            (r'(\d+)\s*(?:garajes?|parking|estacionamientos?)', 'parking'),
        ]
        
        page_text = soup.get_text()
        for pattern, key in char_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            characteristics[key] = int(match.group(1)) if match else 0
        
        details.update(characteristics)
        
        # Descripción
        desc_selectors = [".description", ".property-description", ".detalle"]
        desc_elem = None
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                break
        
        if desc_elem:
            description = desc_elem.get_text(strip=True)
            details["description"] = description[:500] + "..." if len(description) > 500 else description
        else:
            details["description"] = "N/A"
        
        # Amenidades/características adicionales
        amenities = []
        amenity_keywords = ["piscina", "gimnasio", "seguridad", "parqueadero", "balcón", 
                           "terraza", "jardín", "ascensor", "aire acondicionado"]
        
        for keyword in amenity_keywords:
            if keyword.lower() in page_text.lower():
                amenities.append(keyword)
        
        details["amenities"] = ", ".join(amenities) if amenities else "N/A"
        
        # Tipo de propiedad
        property_types = ["casa", "apartamento", "duplex", "penthouse", "loft"]
        property_type = "N/A"
        for ptype in property_types:
            if ptype.lower() in page_text.lower():
                property_type = ptype.capitalize()
                break
        details["property_type"] = property_type
        
        # Año de construcción (si está disponible)
        year_match = re.search(r'(?:año|year|construido|built)[:\s]*(\d{4})', page_text, re.IGNORECASE)
        details["construction_year"] = int(year_match.group(1)) if year_match else None
        
        # Estado de la propiedad
        condition_keywords = ["nuevo", "usado", "remodelado", "excelente", "bueno"]
        condition = "N/A"
        for cond in condition_keywords:
            if cond.lower() in page_text.lower():
                condition = cond.capitalize()
                break
        details["condition"] = condition
        
        return details
        
    except Exception as e:
        print(f"Error scrapeando {property_url}: {e}")
        return {
            "url": property_url,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def create_streaming_data_from_csv(csv_file="../data/propiedades.csv", output_dir="../data/streaming_data"):
    """
    Lee el CSV de propiedades y genera datos detallados para streaming.
    """
    import os
    
    # Crear directorio para datos de streaming
    os.makedirs(output_dir, exist_ok=True)
    
    # Leer URLs del CSV
    try:
        df = pd.read_csv(csv_file)
        urls = df['url'].dropna().tolist()
        
        print(f"📊 Encontradas {len(urls)} URLs para procesar")
        print(f"💾 Datos se guardarán en: {output_dir}/")
        
        for i, url in enumerate(urls, 1):
            print(f"🔍 Procesando {i}/{len(urls)}: {url}")
            
            # Scrapear detalles
            details = scrape_property_details(url)
            
            # Guardar como JSON para Spark Streaming
            filename = f"{output_dir}/property_{i:03d}_{int(time.time())}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(details, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Guardado: {filename}")
            
            # Pausa para simular streaming
            time.sleep(2)
            
    except FileNotFoundError:
        print(f"❌ Archivo {csv_file} no encontrado")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Generar datos para Spark Streaming
    create_streaming_data_from_csv()
