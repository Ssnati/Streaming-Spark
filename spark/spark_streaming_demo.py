"""
DEMO: Spark Streaming para Análisis de Propiedades Inmobiliarias
================================================================

Este demo muestra cómo usar Spark Streaming para procesar datos de propiedades en tiempo real.

Características del demo:
- Generación de datos sintéticos de propiedades
- Procesamiento en tiempo real con Spark Streaming
- Múltiples análisis simultáneos:
  * Estadísticas de precios por ubicación
  * Análisis por tipo de propiedad
  * Detección de propiedades premium
  * Relación calidad-precio

Requisitos:
- Python 3.7+
- PySpark 3.3+
- Java 8 o 11

Instrucciones:
1. pip install pyspark pandas
2. python spark_streaming_demo.py
"""

import subprocess
import threading
import time
import os
import sys

def check_requirements():
    """Verifica que estén instaladas las dependencias necesarias."""
    try:
        import pyspark
        print(f"✅ PySpark {pyspark.__version__} encontrado")
    except ImportError:
        print("❌ PySpark no encontrado. Instalar con: pip install pyspark")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__} encontrado")
    except ImportError:
        print("❌ Pandas no encontrado. Instalar con: pip install pandas")
        return False
    
    return True

def run_demo():
    """Ejecuta el demo completo de Spark Streaming."""
    
    print("🏠 DEMO: SPARK STREAMING - ANÁLISIS DE PROPIEDADES")
    print("=" * 60)
    
    if not check_requirements():
        print("\n❌ Faltan dependencias. Ejecuta:")
        print("pip install pyspark pandas")
        return
    
    print("\n🎯 Este demo demuestra:")
    print("   • Generación de datos sintéticos en tiempo real")
    print("   • Procesamiento con Spark Streaming")
    print("   • Análisis de propiedades inmobiliarias")
    print("   • Múltiples consultas simultáneas")
    
    input("\n⏳ Presiona Enter para continuar...")
      # Limpiar datos anteriores
    print("\n🧹 Preparando entorno...")
    if os.path.exists("../data/streaming_data"):
        import shutil
        shutil.rmtree("../data/streaming_data")
    os.makedirs("../data/streaming_data", exist_ok=True)
    
    print("✅ Entorno preparado")
    
    # Iniciar generador de datos sintéticos
    print("\n📊 Iniciando generador de datos sintéticos...")
    
    def generate_data():
        try:
            subprocess.run([sys.executable, "synthetic_data_generator.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generando datos: {e}")
    
    # Ejecutar generador en hilo separado
    data_thread = threading.Thread(target=generate_data)
    data_thread.daemon = True
    data_thread.start()
    
    # Esperar a que se generen algunos archivos
    print("⏳ Esperando primeros datos...")
    time.sleep(8)
      # Verificar que existan datos
    if not os.listdir("../data/streaming_data"):
        print("❌ No se generaron datos. Verifica synthetic_data_generator.py")
        return
    
    print(f"✅ Datos iniciales generados: {len(os.listdir('../data/streaming_data'))} archivos")
    
    # Iniciar Spark Streaming
    print("\n⚡ Iniciando Spark Streaming...")
    print("📊 Se ejecutarán 5 análisis simultáneos:")
    print("   1. Todas las propiedades procesadas")
    print("   2. Estadísticas por ubicación")
    print("   3. Análisis por tipo de propiedad")
    print("   4. Mejores relaciones calidad-precio")
    print("   5. Alertas de propiedades premium")
    
    print("\n⚠️  IMPORTANTE:")
    print("   • El análisis comenzará en unos segundos")
    print("   • Verás datos actualizándose en tiempo real")
    print("   • Presiona Ctrl+C para detener el demo")
    
    input("\n⏳ Presiona Enter para iniciar Spark Streaming...")
    
    try:
        subprocess.run([sys.executable, "spark_streaming_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en Spark Streaming: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Demo detenido por usuario")
        print("✅ ¡Gracias por probar el demo!")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        print("\n🏁 Demo finalizado")
