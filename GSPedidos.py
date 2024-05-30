import requests

BASE_URL = "http://127.0.0.1:5000"

def consultar_disponibilidad(product_id):
    response = requests.get(f"{BASE_URL}/get_product/{product_id}")
    if response.status_code == 200:
        product = response.json()
        print(f"Producto: {product['nombre']}")
        print(f"Cantidad disponible: {product['cantidad']}")
        print(f"Precio unitario: {product['precio_unitario']}")
        return product
    else:
        print("Producto no encontrado.")
        return None

def actualizar_inventario(product_id, cantidad):
    data = {
        "id": product_id,
        "cantidad": cantidad
    }
    response = requests.post(f"{BASE_URL}/update_product", json=data)
    if response.status_code == 200:
        updated_product = response.json()
        print(f"Inventario actualizado. Nueva cantidad de {updated_product['nombre']}: {updated_product['cantidad']}")
        return updated_product
    else:
        print("Error al actualizar el inventario.")
        print(response.json())
        return None

def realizar_pedido():
    product_id = int(input("Ingrese el ID del producto: "))
    product = consultar_disponibilidad(product_id)
    if product:
        cantidad = int(input("Ingrese la cantidad a pedir: "))
        if cantidad <= product['cantidad']:
            total_precio = cantidad * product['precio_unitario']
            print(f"Precio total del pedido: {total_precio}")
            actualizar_inventario(product_id, cantidad)
        else:
            print("Cantidad solicitada excede la cantidad disponible.")
    else:
        print("No se puede realizar el pedido. Producto no encontrado.")

def menu():
    while True:
        print("\nSistema de Gestión de Pedidos")
        print("1. Consultar disponibilidad de producto")
        print("2. Realizar pedido")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            product_id = int(input("Ingrese el ID del producto: "))
            consultar_disponibilidad(product_id)
        elif opcion == "2":
            realizar_pedido()
        elif opcion == "3":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
