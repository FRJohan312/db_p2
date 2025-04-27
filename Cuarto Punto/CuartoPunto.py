from lxml import etree

def validar_xml_con_xsd(xml_file, xsd_file):
    # Cargar el esquema XSD
    with open(xsd_file, 'rb') as f:  # Usamos 'rb' para leer como bytes
        schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)

    # Cargar el archivo XML
    with open(xml_file, 'rb') as f:  # Usamos 'rb' para leer como bytes
        xml_doc = etree.XML(f.read())

    # Validar el XML contra el XSD
    is_valid = schema.validate(xml_doc)
    if is_valid:
        print(f"El archivo {xml_file} es válido contra el esquema {xsd_file}.")
    else:
        print(f"El archivo {xml_file} NO es válido contra el esquema {xsd_file}.")
        # Mostrar errores de validación
        print(schema.error_log)

# Validar el archivo XML contra el XSD
validar_xml_con_xsd('empleados.xml', 'empleados.xsd')
