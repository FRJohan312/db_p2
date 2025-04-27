import json
import xml.etree.ElementTree as ET

XML_FILE = 'empleados.xml'
JSON_FILE = 'empleados.json'

def inicializar():
    # Verificar si el archivo XML existe usando un bloque try-except
    try:
        tree = ET.parse(XML_FILE)
    except FileNotFoundError:
        root = ET.Element('empleados')
        ET.ElementTree(root).write(XML_FILE, encoding="utf-8", xml_declaration=True)
    
    # Verificar si el archivo JSON existe
    try:
        with open(JSON_FILE, 'r') as f:
            json.load(f)
    except FileNotFoundError:
        with open(JSON_FILE, 'w') as f:
            json.dump([], f)

def agregar_empleado(nombre, edad, departamento, salario):
    inicializar()

    # XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    empleado = ET.Element('empleado')
    ET.SubElement(empleado, 'nombre').text = nombre
    ET.SubElement(empleado, 'edad').text = str(edad)
    ET.SubElement(empleado, 'departamento').text = departamento
    ET.SubElement(empleado, 'salario').text = str(salario)
    root.append(empleado)
    tree.write(XML_FILE)

    # JSON
    with open(JSON_FILE, 'r') as f:
        empleados = json.load(f)
    empleados.append({
        'nombre': nombre,
        'edad': edad,
        'departamento': departamento,
        'salario': salario
    })
    with open(JSON_FILE, 'w') as f:
        json.dump(empleados, f, indent=2)

def actualizar_salario(nombre, nuevo_salario):
    inicializar()

    # XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for emp in root.findall('empleado'):
        if emp.find('nombre').text == nombre:
            emp.find('salario').text = str(nuevo_salario)
            break
    tree.write(XML_FILE)

    # JSON
    with open(JSON_FILE, 'r') as f:
        empleados = json.load(f)
    for emp in empleados:
        if emp['nombre'] == nombre:
            emp['salario'] = nuevo_salario
            break
    with open(JSON_FILE, 'w') as f:
        json.dump(empleados, f, indent=2)

def consultar_empleado(nombre):
    inicializar()

    encontrado = False

    # XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for emp in root.findall('empleado'):
        if emp.find('nombre').text == nombre:
            print("\nDesde XML:")
            print(f"Nombre: {emp.find('nombre').text}")
            print(f"Edad: {emp.find('edad').text}")
            print(f"Departamento: {emp.find('departamento').text}")
            print(f"Salario: {emp.find('salario').text}")
            encontrado = True
            break

    # JSON
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

    if not encontrado:
        print(f"\nEmpleado '{nombre}' no encontrado.")

# Menú sencillo
def menu():
    while True:
        print("\n--- Menú Empleados ---")
        print("1. Agregar empleado")
        print("2. Actualizar salario")
        print("3. Consultar empleado")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            departamento = input("Departamento: ")
            salario = input("Salario: ")
            agregar_empleado(nombre, int(edad), departamento, float(salario))

        elif opcion == '2':
            nombre = input("Nombre del empleado: ")
            nuevo_salario = input("Nuevo salario: ")
            actualizar_salario(nombre, float(nuevo_salario))

        elif opcion == '3':
            nombre = input("Nombre del empleado: ")
            consultar_empleado(nombre)

        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
