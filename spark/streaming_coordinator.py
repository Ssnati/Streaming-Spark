import subprocess
import threading
import time
import os

def run_data_generator():
    """
    Ejecuta el generador de datos en un hilo separado.
    """
    print("🔄 Iniciando generador de datos...")
    try:
        subprocess.run(["python", "../scraping/detailed_scraper.py"], check=True)
        print("✅ Generador de datos completado")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en generador de datos: {e}")

def run_spark_streaming():
    """
    Ejecuta Spark Streaming en un hilo separado.
    """
    print("⚡ Iniciando Spark Streaming...")
    try:
        subprocess.run(["python", "spark_streaming_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en Spark Streaming: {e}")
    except KeyboardInterrupt:
        print("🛑 Spark Streaming detenido por usuario")

def main():
    """
    Coordina la ejecución del sistema completo.
    """
    print("🚀 SISTEMA DE STREAMING DE PROPIEDADES INMOBILIARIAS")
    print("=" * 60)
    print("📋 Este sistema demuestra:")
    print("   • Web Scraping en tiempo real")
    print("   • Procesamiento con Spark Streaming")
    print("   • Análisis de datos en vivo")
    print("=" * 60)
      # Verificar archivos necesarios
    required_files = ["../data/propiedades.csv", "../scraping/detailed_scraper.py", "spark_streaming_app.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        return
    
    # Crear directorio para datos de streaming
    os.makedirs("../data/streaming_data", exist_ok=True)
    
    print("\n🎯 Opciones de ejecución:")
    print("1. Solo generar datos (scraping detallado)")
    print("2. Solo ejecutar Spark Streaming")
    print("3. Ejecutar sistema completo (recomendado)")
    print("4. Limpiar datos anteriores y ejecutar completo")
    
    choice = input("\nSelecciona una opción (1-4): ").strip()
    
    if choice == "1":
        print("\n📊 Generando datos de streaming...")
        run_data_generator()
        
    elif choice == "2":
        print("\n⚡ Ejecutando solo Spark Streaming...")
        print("⚠️  Asegúrate de que existan datos en streaming_data/")
        time.sleep(2)
        run_spark_streaming()
        
    elif choice == "3":
        print("\n🚀 Ejecutando sistema completo...")
        
        # Iniciar generador de datos en un hilo
        data_thread = threading.Thread(target=run_data_generator)
        data_thread.daemon = True
        data_thread.start()
        
        # Esperar un poco para que se generen algunos archivos
        print("⏳ Esperando que se generen los primeros datos...")
        time.sleep(10)
        
        # Iniciar Spark Streaming
        try:
            run_spark_streaming()
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por usuario")

    elif choice == "4":
        print("\n🧹 Limpiando datos anteriores...")
        import shutil
        if os.path.exists("../data/streaming_data"):
            shutil.rmtree("../data/streaming_data")
        os.makedirs("../data/streaming_data", exist_ok=True)
        
        print("🚀 Ejecutando sistema completo...")
        
        # Iniciar generador de datos en un hilo
        data_thread = threading.Thread(target=run_data_generator)
        data_thread.daemon = True
        data_thread.start()
        
        # Esperar un poco para que se generen algunos archivos
        print("⏳ Esperando que se generen los primeros datos...")
        time.sleep(10)
        
        # Iniciar Spark Streaming
        try:
            run_spark_streaming()
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por usuario")
    
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()
