import base64

class ProductViewModel:
    def __init__(self, product_cqrs):
        self.product_cqrs = product_cqrs
        
    # Metodo para INSERTAR productos
    def insert_product(self, nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id):
        return self.product_cqrs.insert_product_command(nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id)
    
    # Metodo para ACTUALIZAR productos
    def update_product(self, product_id, nombre, precio, descripcion, codigo, stock, info_adicional, imagen, oferta, categoria_id):
        return self.product_cqrs.update_product_command(product_id, nombre, precio, descripcion, codigo, stock, info_adicional, imagen, oferta, categoria_id)

    # Metodo para ELIMINAR productos
    def delete_product(self, product_id):
        return self.product_cqrs.delete_product_command(product_id)
    
    # Metodo para mostrar todas las categorias
    def get_all_categories(self):
        return self.product_cqrs.get_all_categories_query()

    # Metodo para mostrar todos los productos
    def get_all_products(self):
        return self.product_cqrs.get_all_products_query()
    
    # Metodo para buscar productos 
    def search_products(self, search_query):
        return self.product_cqrs.search_products_query(search_query)
    
    # Metodo para mostrar productos por ID
    def get_product_by_id(self, product_id):
        return self.product_cqrs.get_product_by_id_query(product_id)
    
    # Metodo para mostrar los productos destacados
    def get_featured_products(self, limit=6):
        productos = self.product_cqrs.get_products(limit=limit)
        for producto in productos:
            if producto["imagen_producto"]: 
                producto["imagen_base64"] = base64.b64encode(producto["imagen_producto"]).decode('utf-8')
            else:
                producto["imagen_base64"] = None
        return productos
    
    #Metodo para mostrar solo los productos que estan en oferta
    def get_products_in_offer(self):
        productos = self.product_cqrs.get_products_in_offer()
        
        # Convertir las imágenes a Base64 para mostrarlas en la página
        for producto in productos:
            if 'imagen_producto' in producto and producto['imagen_producto']:
                producto['imagen_base64'] = base64.b64encode(producto['imagen_producto']).decode('utf-8')
            else:
                producto['imagen_base64'] = None
        return productos
    
    
    # Metodo para filtrado de productos
    def get_filtered_products(self, filtros, orden):
        # Mapear el filtro de 'nombre' a 'nombre_producto'
        filtros_mapeados = {
            'nombre_producto': filtros.get('nombre'),
            'precio_min': filtros.get('precio_min'),
            'precio_max': filtros.get('precio_max'),
            'categoria': filtros.get('categoria')
        }
        return self.product_cqrs.get_filtered_products(filtros_mapeados, orden)
   
    def get_product_by_id(self, producto_id):
        return self.product_cqrs.get_product_by_id(producto_id)