#!/usr/bin/env python3
"""
🏠 SISTEMA COMPLETO DE WEB SCRAPING + SPARK STREAMING
====================================================

Punto de entrada principal para el proyecto de análisis de propiedades inmobiliarias.

Estructura del proyecto:
📁 scraping/     - Módulos de web scraping
📁 spark/        - Módulos de Spark Streaming  
📁 data/         - Datos generados y archivos HTML

Opciones disponibles:
1. Web Scraping básico
2. Demo Spark Streaming (RECOMENDADO)
3. Sistema completo con datos reales
4. Generar datos sintéticos
"""

import sys
import os
import subprocess
from pathlib import Path

def print_banner():
    """Muestra el banner principal del sistema."""
    print("🏠" + "=" * 58 + "🏠")
    print("   SISTEMA DE ANÁLISIS DE PROPIEDADES INMOBILIARIAS")
    print("   Web Scraping + Apache Spark Streaming")
    print("🏠" + "=" * 58 + "🏠")
    print()

def check_dependencies():
    """Verifica las dependencias del sistema."""
    print("🔍 Verificando dependencias...")
    
    missing_deps = []
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requerido")
        return False
    
    # Verificar módulos esenciales
    try:
        import requests
        import bs4
        import pandas
        print("✅ Módulos de scraping: OK")
    except ImportError as e:
        missing_deps.append(f"Scraping: {e}")
    
    # Verificar PySpark (opcional)
    try:
        import pyspark
        print("✅ PySpark: OK")
    except ImportError:
        print("⚠️  PySpark no encontrado (necesario solo para Spark Streaming)")
        missing_deps.append("PySpark para Spark Streaming")
    
    if missing_deps:
        print("\n📦 Para instalar dependencias faltantes:")
        print("   pip install -r requirements-min.txt")
        return False
    
    return True

def run_basic_scraping():
    """Ejecuta el web scraping básico."""
    print("\n🕷️ EJECUTANDO WEB SCRAPING BÁSICO")
    print("=" * 50)
    print("📊 Extrayendo propiedades de Fincaraíz...")
    
    try:
        result = subprocess.run([
            sys.executable, "scraping/Spark.py"
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode == 0:
            print("✅ Scraping completado exitosamente!")
            print(f"📄 Resultados guardados en: data/propiedades.csv")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error en el scraping:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error ejecutando scraper: {e}")

def run_spark_streaming_demo():
    """Ejecuta el demo de Spark Streaming."""
    print("\n⚡ EJECUTANDO DEMO SPARK STREAMING")
    print("=" * 50)
    print("🎯 Este demo muestra:")
    print("   • Generación de datos en tiempo real")
    print("   • 5 análisis simultáneos con Spark")
    print("   • Procesamiento de stream de propiedades")
    
    try:
        # Cambiar al directorio spark para ejecutar
        result = subprocess.run([
            sys.executable, "spark_streaming_demo.py"
        ], cwd=Path.cwd() / "spark")
        
    except Exception as e:
        print(f"❌ Error ejecutando demo: {e}")

def run_complete_system():
    """Ejecuta el sistema completo con datos reales."""
    print("\n🚀 EJECUTANDO SISTEMA COMPLETO")
    print("=" * 50)
    print("📋 El sistema completo incluye:")
    print("   • Scraping detallado de propiedades reales")
    print("   • Procesamiento con Spark Streaming")
    print("   • Análisis en tiempo real")
    
    try:
        # Cambiar al directorio spark para ejecutar
        result = subprocess.run([
            sys.executable, "streaming_coordinator.py"
        ], cwd=Path.cwd() / "spark")
        
    except Exception as e:
        print(f"❌ Error ejecutando sistema completo: {e}")

def generate_synthetic_data():
    """Genera datos sintéticos para pruebas."""
    print("\n🎲 GENERANDO DATOS SINTÉTICOS")
    print("=" * 50)
    print("📊 Creando 50 propiedades sintéticas...")
    
    try:
        result = subprocess.run([
            sys.executable, "synthetic_data_generator.py"
        ], cwd=Path.cwd() / "spark")
        
    except Exception as e:
        print(f"❌ Error generando datos: {e}")

def show_project_structure():
    """Muestra la estructura del proyecto."""
    print("\n📁 ESTRUCTURA DEL PROYECTO")
    print("=" * 50)
    print("""
📁 Electiva-4/
├── 📄 main.py                    # ← Punto de entrada principal
├── 📄 README.md                  # Documentación completa
├── 📄 requirements-min.txt       # Dependencias esenciales
├── 📄 requirements.txt           # Todas las dependencias
├── 📁 scraping/                  # Módulos de web scraping
│   ├── 📄 Spark.py              # Scraper básico de Fincaraíz
│   └── 📄 detailed_scraper.py   # Scraper detallado individual
├── 📁 spark/                     # Módulos de Spark Streaming
│   ├── 📄 spark_streaming_app.py      # Motor de Spark Streaming
│   ├── 📄 spark_streaming_demo.py     # Demo completo
│   ├── 📄 synthetic_data_generator.py # Generador de datos
│   └── 📄 streaming_coordinator.py    # Coordinador del sistema
└── 📁 data/                      # Datos y archivos generados
    ├── 📄 propiedades.csv        # Datos de propiedades
    ├── 📄 html_response_*.html   # Respuestas HTML guardadas
    └── 📁 streaming_data/        # Datos para Spark (se crea automáticamente)
    """)

def main():
    """Función principal del sistema."""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n⚠️  Algunas dependencias faltan, pero puedes continuar con funciones limitadas.")
        input("Presiona Enter para continuar...")
    
    while True:
        print("\n🎯 OPCIONES DISPONIBLES:")
        print("=" * 30)
        print("1. 🕷️  Web Scraping básico")
        print("2. ⚡ Demo Spark Streaming (RECOMENDADO)")
        print("3. 🚀 Sistema completo (scraping real + streaming)")
        print("4. 🎲 Generar datos sintéticos")
        print("5. 📁 Ver estructura del proyecto")
        print("6. 🔧 Verificar dependencias")
        print("0. 🚪 Salir")
        
        choice = input("\n👉 Selecciona una opción (0-6): ").strip()
        
        if choice == "1":
            run_basic_scraping()
            
        elif choice == "2":
            run_spark_streaming_demo()
            
        elif choice == "3":
            run_complete_system()
            
        elif choice == "4":
            generate_synthetic_data()
            
        elif choice == "5":
            show_project_structure()
            
        elif choice == "6":
            check_dependencies()
            
        elif choice == "0":
            print("\n👋 ¡Gracias por usar el sistema!")
            print("🎓 Proyecto Electiva-4 - Análisis de Propiedades")
            break
            
        else:
            print("❌ Opción inválida. Por favor selecciona 0-6.")
        
        input("\n⏳ Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema interrumpido por el usuario")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("🔧 Por favor verifica la instalación del sistema")
