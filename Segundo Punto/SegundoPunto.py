import json
import xml.etree.ElementTree as ET

XML_FILE = 'catalogo.xml'
JSON_FILE = 'catalogo.json'

def inicializar_catalogo():
    """
    Permite al usuario crear manualmente el catálogo XML agregando productos.
    Si el archivo ya existe, no lo sobreescribe.
    """
    try:
        ET.parse(XML_FILE)  # Intenta abrir el archivo XML
        print("Ya hay un catalogo")
    except FileNotFoundError:
        root = ET.Element('catalogo')

        print("Crear nuevo catalogo")
        
        while True:
            # Solicitar datos al usuario
            id_producto = input("ID del producto: ")
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")
            precio = input("Precio: ")
            stock = input("Stock: ")

            # Crear el producto en XML
            producto = ET.SubElement(root, 'producto', id=id_producto)
            ET.SubElement(producto, 'nombre').text = nombre
            ET.SubElement(producto, 'descripcion').text = descripcion
            ET.SubElement(producto, 'precio').text = precio
            ET.SubElement(producto, 'stock').text = stock

            continuar = input("¿Deseas agregar otro producto? (s/n): ").lower()
            if continuar != 's':
                break
        
        # Guardar el archivo XML
        ET.ElementTree(root).write(XML_FILE, encoding="utf-8", xml_declaration=True)
        print("Catálogo creado correctamente.")

def modificar_stock(id_producto, nuevo_stock):
    inicializar_catalogo()

    try:
        nuevo_stock = int(nuevo_stock)
    except ValueError:
        print("Ingrese un numero entero.")
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
        print("1. Crear catálogo XML (agregar productos)")
        print("2. Modificar stock de producto")
        print("3. Exportar catálogo a JSON")
        print("4. Buscar producto en JSON")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            inicializar_catalogo()

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
