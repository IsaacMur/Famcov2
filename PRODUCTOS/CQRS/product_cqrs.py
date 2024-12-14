class ProductCQRS:
    def __init__(self, product_dao):
        self.product_dao = product_dao
        
    # Metodo para INSERTAR productos
    def insert_product_command(self, nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id):
        return self.product_dao.insert_product(nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id)
    
     # Metodo para ACTUALIZAR productos
    def update_product_command(self, product_id, nombre, precio, descripcion, codigo, stock, info_adicional, imagen, oferta, categoria_id):
        return self.product_dao.update_product(product_id, nombre, precio, descripcion, codigo, stock, info_adicional, imagen, oferta, categoria_id)

    # Metodo para ELIMINAR los productos 
    def delete_product_command(self, product_id):
        return self.product_dao.delete_product(product_id)
    
    # Metodo para mostrar todas las categorias
    def get_all_categories_query(self):
        return self.product_dao.get_all_categories()

    # Metodo para mostarar todo los productos
    def get_all_products_query(self):
        return self.product_dao.get_all_products()
    
    # Metodo para mostrar el producto solo por ID
    def get_product_by_id_query(self, product_id):
        return self.product_dao.get_product_by_id(product_id)
    
    # Metodo para buscar productos
    def search_products_query(self, search_query):
        return self.product_dao.search_products(search_query)
    
    # Metodo para mostrar los productos destacados
    def get_products(self, limit=None):
        return self.product_dao.get_products(limit=limit)
    
    # Metodo para mostrar solo los productos que estan en oferta
    def get_products_in_offer(self):
        return self.product_dao.get_products_in_offer()
    
    # Metodo para el filtrado de productos
    def get_filtered_products(self, filtros, orden):
        return self.product_dao.get_filtered_products(
            nombre_producto=filtros.get('nombre_producto'),
            precio_min=filtros.get('precio_min'),
            precio_max=filtros.get('precio_max'),
            categoria=filtros.get('categoria'),
            orden=orden
        )

    def get_product_by_id(self, producto_id):
        return self.product_dao.get_product_by_id(producto_id)
