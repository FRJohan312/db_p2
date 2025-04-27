import json
import xml.etree.ElementTree as ET

JSON_FILE = 'encuestas.json'
XML_FILE = 'resumen_encuestas.xml'

# Crear archivo JSON con las encuestas
def crear_encuestas_json():
    encuestas = [
        {'ciudad': 'Madrid', 'personas_encuestadas': 500, 'transporte_mas_utilizado': 'Metro'},
        {'ciudad': 'Barcelona', 'personas_encuestadas': 350, 'transporte_mas_utilizado': 'Autobús'},
        {'ciudad': 'Sevilla', 'personas_encuestadas': 200, 'transporte_mas_utilizado': 'Tramvia'}
    ]
    
    with open(JSON_FILE, 'w') as f:
        json.dump(encuestas, f, indent=2)
    print("Archivo encuestas.json creado.")

# Generar resumen en XML
def generar_resumen_xml():
    try:
        with open(JSON_FILE, 'r') as f:
            encuestas = json.load(f)
    except FileNotFoundError:
        print(f"El archivo {JSON_FILE} no existe. Por favor, crea las encuestas primero.")
        return

    root = ET.Element('resumen')
    
    for encuesta in encuestas:
        ciudad = encuesta['ciudad']
        personas_encuestadas = encuesta['personas_encuestadas']
        transporte_mas_utilizado = encuesta['transporte_mas_utilizado']
        
        ciudad_elem = ET.SubElement(root, 'ciudad', nombre=ciudad)
        ET.SubElement(ciudad_elem, 'personas_encuestadas').text = str(personas_encuestadas)
        ET.SubElement(ciudad_elem, 'transporte_mas_utilizado').text = transporte_mas_utilizado

    tree = ET.ElementTree(root)
    tree.write(XML_FILE, encoding='utf-8', xml_declaration=True)
    print(f"Resumen guardado en {XML_FILE}")

# Visualizar los resultados en consola y guardar en XML
def visualizar_resultados():
    try:
        with open(JSON_FILE, 'r') as f:
            encuestas = json.load(f)
    except FileNotFoundError:
        print(f"El archivo {JSON_FILE} no existe. Por favor, crea las encuestas primero.")
        return

    print("\n--- Resumen de Encuestas ---")
    for encuesta in encuestas:
        print(f"\nCiudad: {encuesta['ciudad']}")
        print(f"Personas encuestadas: {encuesta['personas_encuestadas']}")
        print(f"Transporte más utilizado: {encuesta['transporte_mas_utilizado']}")
    
    # Generar el resumen XML
    generar_resumen_xml()

# Menú para el usuario
def menu():
    while True:
        print("\n--- Menú Encuestas ---")
        print("1. Crear encuestas (JSON)")
        print("2. Generar resumen en XML")
        print("3. Visualizar resultados")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            crear_encuestas_json()
        elif opcion == '2':
            generar_resumen_xml()
        elif opcion == '3':
            visualizar_resultados()
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
