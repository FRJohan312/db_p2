import json
import xml.etree.ElementTree as ET

# Archivos donde se almacenarán los datos
XML_FILE = 'empleados.xml'
JSON_FILE = 'empleados.json'

def inicializar():
    """
    Verifica que existan los archivos XML y JSON.
    Si no existen, los crea vacíos (estructura básica en XML y lista vacía en JSON).
    """
    try:
        tree = ET.parse(XML_FILE)  # Intenta cargar el archivo XML
    except FileNotFoundError:
        # Si no existe, crea la estructura básica del XML
        root = ET.Element('empleados')
        ET.ElementTree(root).write(XML_FILE, encoding="utf-8", xml_declaration=True)
    
    try:
        with open(JSON_FILE, 'r') as f:
            json.load(f)  # Intenta cargar el archivo JSON
    except FileNotFoundError:
        # Si no existe, crea una lista vacía
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)

def agregar_empleado(nombre, edad, departamento, salario):
    """
    Agrega un nuevo empleado tanto en el archivo XML como en el archivo JSON.
    """
    inicializar()  # Asegura que los archivos existan

    # --- Parte XML ---
    tree = ET.parse(XML_FILE)  # Carga el XML
    root = tree.getroot()
    
    # Crea un nuevo elemento 'empleado' con sus subelementos
    empleado = ET.Element('empleado')
    ET.SubElement(empleado, 'nombre').text = nombre
    ET.SubElement(empleado, 'edad').text = str(edad)
    ET.SubElement(empleado, 'departamento').text = departamento
    ET.SubElement(empleado, 'salario').text = str(salario)
    
    # Agrega el nuevo empleado al XML
    root.append(empleado)
    tree.write(XML_FILE)

    # --- Parte JSON ---
    with open(JSON_FILE, 'r') as f:
        empleados = json.load(f)  # Carga los empleados existentes
    
    # Agrega el nuevo empleado como un diccionario
    empleados.append({
        'nombre': nombre,
        'edad': edad,
        'departamento': departamento,
        'salario': salario
    })
    
    # Guarda los cambios en el archivo JSON
    with open(JSON_FILE, 'w') as f:
        json.dump(empleados, f, indent=2)

def actualizar_salario(nombre, nuevo_salario):
    """
    Actualiza el salario de un empleado tanto en XML como en JSON.
    """
    inicializar()  # Asegura que los archivos existan

    # --- Parte XML ---
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Busca el empleado por nombre y actualiza el salario
    for emp in root.findall('empleado'):
        if emp.find('nombre').text == nombre:
            emp.find('salario').text = str(nuevo_salario)
            break
    tree.write(XML_FILE)

    # --- Parte JSON ---
    with open(JSON_FILE, 'r') as f:
        empleados = json.load(f)
    
    # Busca el empleado por nombre y actualiza el salario
    for emp in empleados:
        if emp['nombre'] == nombre:
            emp['salario'] = nuevo_salario
            break
    
    with open(JSON_FILE, 'w') as f:
        json.dump(empleados, f, indent=2)

def consultar_empleado(nombre):
    """
    Consulta la información de un empleado tanto en XML como en JSON.
    """
    inicializar()  # Asegura que los archivos existan

    encontrado = False  # Bandera para saber si se encontró al empleado

    # --- Parte XML ---
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Busca el empleado por nombre
    for emp in root.findall('empleado'):
        if emp.find('nombre').text == nombre:
            print("\nDesde XML:")
            print(f"Nombre: {emp.find('nombre').text}")
            print(f"Edad: {emp.find('edad').text}")
            print(f"Departamento: {emp.find('departamento').text}")
            print(f"Salario: {emp.find('salario').text}")
            encontrado = True
            break

    # --- Parte JSON ---
    with open(JSON_FILE, 'r') as f:
        empleados = json.load(f)
    
    for emp in empleados:
        if emp['nombre'] == nombre:
            print("\nDesde JSON:")
            print(f"Nombre: {emp['nombre']}")
            print(f"Edad: {emp['edad']}")
            print(f"Departamento: {emp['departamento']}")
            print(f"Salario: {emp['salario']}")
            encontrado = True
            break

    # Si no se encontró en ninguno de los dos archivos
    if not encontrado:
        print(f"\nEmpleado '{nombre}' no encontrado.")

def menu():
    """
    Muestra un menú simple para interactuar con el sistema de empleados.
    """
    while True:
        print("\n--- Menú Empleados ---")
        print("1. Agregar empleado")
        print("2. Actualizar salario")
        print("3. Consultar empleado")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Solicita datos del nuevo empleado
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            departamento = input("Departamento: ")
            salario = input("Salario: ")
            agregar_empleado(nombre, int(edad), departamento, float(salario))

        elif opcion == '2':
            # Solicita datos para actualizar salario
            nombre = input("Nombre del empleado: ")
            nuevo_salario = input("Nuevo salario: ")
            actualizar_salario(nombre, float(nuevo_salario))

        elif opcion == '3':
            # Solicita el nombre para consultar un empleado
            nombre = input("Nombre del empleado: ")
            consultar_empleado(nombre)

        elif opcion == '4':
            print("Saliendo...")
            break  # Sale del ciclo y termina el programa
        else:
            print("Opción no válida, intenta de nuevo.")

# Punto de entrada principal del programa
if __name__ == "__main__":
    menu()
