#!/usr/bin/env python3
"""
Script de prueba rápida para verificar la estructura del proyecto.
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Prueba que la estructura del proyecto esté correcta."""
    print("🔍 Verificando estructura del proyecto...")
    
    # Verificar directorios principales
    required_dirs = ["scraping", "spark", "data"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directorio {dir_name}/ encontrado")
        else:
            print(f"❌ Directorio {dir_name}/ faltante")
            return False
    
    # Verificar archivos principales
    required_files = {
        "scraping/Spark.py": "Scraper básico",
        "scraping/detailed_scraper.py": "Scraper detallado",
        "spark/spark_streaming_app.py": "Motor Spark Streaming",
        "spark/spark_streaming_demo.py": "Demo Spark Streaming",
        "spark/synthetic_data_generator.py": "Generador datos sintéticos",
        "main.py": "Punto de entrada principal",
        "README.md": "Documentación",
        "requirements-min.txt": "Dependencias mínimas"
    }
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description} FALTANTE")
            return False
    
    print("\n🎉 ¡Estructura del proyecto verificada correctamente!")
    return True

def test_imports():
    """Prueba las importaciones básicas."""
    print("\n🔍 Verificando dependencias básicas...")
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError:
        print("❌ requests - FALTANTE")
    
    try:
        import bs4
        print("✅ beautifulsoup4 - OK")
    except ImportError:
        print("❌ beautifulsoup4 - FALTANTE")
    
    try:
        import pandas
        print("✅ pandas - OK")
    except ImportError:
        print("❌ pandas - FALTANTE")
    
    try:
        import pyspark
        print("✅ pyspark - OK")
    except ImportError:
        print("⚠️ pyspark - OPCIONAL (solo para Spark Streaming)")

def main():
    """Función principal del test."""
    print("🧪 PRUEBA RÁPIDA DEL PROYECTO")
    print("=" * 40)
    
    success = test_project_structure()
    test_imports()
    
    if success:
        print("\n✅ PROYECTO LISTO PARA USAR")
        print("\n🚀 Para comenzar, ejecuta:")
        print("   python main.py")
    else:
        print("\n❌ PROYECTO INCOMPLETO")
        print("Verifica que todos los archivos estén en su lugar")

if __name__ == "__main__":
    main()
