import json
import time
import random
from datetime import datetime
import os

def generate_synthetic_property_data():
    """
    Genera datos sintéticos de propiedades para demostrar Spark Streaming.
    Más fácil de probar que scraping real.
    """
    
    # Datos base para generar propiedades sintéticas
    locations = ["Tunja Centro", "La Calleja", "Villa de Leyva", "Patricios", "Norte", "Sur"]
    property_types = ["Casa", "Apartamento", "Duplex", "Penthouse"]
    conditions = ["Nuevo", "Usado", "Excelente", "Bueno", "Remodelado"]
    amenities_options = [
        ["Piscina", "Gimnasio", "Seguridad"],
        ["Parqueadero", "Balcón", "Terraza"],
        ["Jardín", "BBQ", "Zona Social"],
        ["Ascensor", "Aire Acondicionado", "Calefacción"],
        ["Jacuzzi", "Sauna", "Cancha"]
    ]
    
    os.makedirs("../data/streaming_data", exist_ok=True)
    
    print("🏠 Generando datos sintéticos de propiedades...")
    print("💡 Esto simula un flujo de datos en tiempo real para Spark Streaming")
    print("=" * 60)
    
    for i in range(1, 51):  # Generar 50 propiedades
        # Generar datos aleatorios pero realistas
        rooms = random.randint(2, 6)
        bathrooms = random.randint(1, rooms)
        area_m2 = random.randint(80, 300)
        price_per_m2 = random.randint(1500000, 4000000)  # COP por m²
        price = area_m2 * price_per_m2
        
        property_data = {
            "url": f"https://example.com/property-{i}",
            "timestamp": datetime.now().isoformat(),
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": f"Hermosa {random.choice(property_types)} en {random.choice(locations)}",
            "price": price,
            "location": random.choice(locations),
            "rooms": rooms,
            "bathrooms": bathrooms,
            "area_m2": area_m2,
            "floors": random.randint(1, 3) if random.choice(property_types) == "Casa" else 1,
            "parking": random.randint(1, 3),
            "description": f"Excelente {random.choice(property_types).lower()} ubicada en {random.choice(locations)}, perfecta para familias.",
            "amenities": ", ".join(random.choice(amenities_options)),
            "property_type": random.choice(property_types),
            "construction_year": random.randint(2000, 2024),
            "condition": random.choice(conditions),
            "price_per_m2": price_per_m2
        }
          # Guardar como JSON
        filename = f"../data/streaming_data/synthetic_property_{i:03d}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(property_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {i}/50 - {property_data['title']} - ${property_data['price']:,}")
        
        # Simular llegada de datos en tiempo real
        time.sleep(random.uniform(1, 3))  # Pausa aleatoria entre 1-3 segundos
    
    print(f"\n🎉 ¡Generación completa! 50 propiedades creadas en streaming_data/")

if __name__ == "__main__":
    generate_synthetic_property_data()
