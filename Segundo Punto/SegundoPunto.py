import json
import xml.etree.ElementTree as ET

XML_FILE = 'catalogo.xml'
JSON_FILE = 'catalogo.json'

def inicializar_catalogo():
    try:
        ET.parse(XML_FILE)
    except FileNotFoundError:
        root = ET.Element('catalogo')

        productos = [
            {'id': 'P001', 'nombre': 'Laptop', 'descripcion': 'Laptop de 14 pulgadas', 'precio': '1500', 'stock': '10'},
            {'id': 'P002', 'nombre': 'Mouse', 'descripcion': 'Mouse inalámbrico', 'precio': '20', 'stock': '100'},
            {'id': 'P003', 'nombre': 'Teclado', 'descripcion': 'Teclado mecánico', 'precio': '70', 'stock': '50'},
            {'id': 'P004', 'nombre': 'Monitor', 'descripcion': 'Monitor 24 pulgadas', 'precio': '200', 'stock': '30'},
            {'id': 'P005', 'nombre': 'Auriculares', 'descripcion': 'Auriculares Bluetooth', 'precio': '80', 'stock': '40'},
        ]

        for prod in productos:
            producto = ET.SubElement(root, 'producto', id=prod['id'])
            ET.SubElement(producto, 'nombre').text = prod['nombre']
            ET.SubElement(producto, 'descripcion').text = prod['descripcion']
            ET.SubElement(producto, 'precio').text = prod['precio']
            ET.SubElement(producto, 'stock').text = prod['stock']

        ET.ElementTree(root).write(XML_FILE)

def modificar_stock(id_producto, nuevo_stock):
    inicializar_catalogo()

    try:
        nuevo_stock = int(nuevo_stock)  # Aseguramos que el nuevo stock sea un número entero
    except ValueError:
        print("Error: el stock debe ser un número entero.")
        return

    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    encontrado = False

    for producto in root.findall('producto'):
        if producto.get('id') == id_producto:
            producto.find('stock').text = str(nuevo_stock)
            encontrado = True
            break

    if encontrado:
        tree.write(XML_FILE)
        print(f"Stock del producto {id_producto} actualizado a {nuevo_stock}.")
    else:
        print(f"No se encontró el producto con ID {id_producto}.")

def exportar_a_json():
    inicializar_catalogo()

    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    productos = []
    for producto in root.findall('producto'):
        try:
            productos.append({
                'id': producto.get('id'),
                'nombre': producto.find('nombre').text,
                'descripcion': producto.find('descripcion').text,
                'precio': float(producto.find('precio').text),
                'stock': int(producto.find('stock').text)
            })
        except (ValueError, AttributeError):
            print(f"Error al exportar producto ID {producto.get('id')}. Verifica los datos.")
    
    if productos:
        with open(JSON_FILE, 'w') as f:
            json.dump(productos, f, indent=2)
        print("Catálogo exportado correctamente.")
    else:
        print("No se exportó ningún producto válido.")

def buscar_producto(id_producto):
    try:
        with open(JSON_FILE, 'r') as f:
            productos = json.load(f)
    except FileNotFoundError:
        print("Primero debes exportar a JSON.")
        return

    encontrado = False
    for prod in productos:
        if prod['id'] == id_producto:
            print("\nProducto encontrado:")
            print(f"ID: {prod['id']}")
            print(f"Nombre: {prod['nombre']}")
            print(f"Descripción: {prod['descripcion']}")
            print(f"Precio: ${prod['precio']}")
            print(f"Stock: {prod['stock']} unidades")
            encontrado = True
            break

    if not encontrado:
        print(f"\nProducto con ID '{id_producto}' no encontrado.")

def menu():
    while True:
        print("\n--- Menú Catálogo ---")
        print("1. Crear catálogo XML")
        print("2. Modificar stock de producto")
        print("3. Exportar catálogo a JSON")
        print("4. Buscar producto en JSON")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            inicializar_catalogo()
            print("Catálogo creado o verificado.")

        elif opcion == '2':
            id_producto = input("ID del producto: ")
            nuevo_stock = input("Nuevo stock: ")
            modificar_stock(id_producto, nuevo_stock)

        elif opcion == '3':
            exportar_a_json()

        elif opcion == '4':
            id_producto = input("ID del producto a buscar: ")
            buscar_producto(id_producto)

        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
