import base64

class ProductDAO:
    def __init__(self, mysql):
        self.mysql = mysql

    # Metodo para INSERTAR productos
    def insert_product(self, nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id):
        query = """
        INSERT INTO productos (nombre_producto, precio_producto, descripcion_producto, codigo_producto,
        stock_producto, informacion_adicional, imagen_producto, oferta_producto, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, (nombre, precio, descripcion, codigo, stock, info, imagen, oferta, categoria_id))
        self.mysql.connection.commit()
        cursor.close()
        return cursor.lastrowid
    
    
    # Metodo para ACTUALIZAR productos
    def update_product(self, product_id, nombre, precio, descripcion, codigo, stock, info_adicional, imagen, oferta, categoria_id):
        query = """
            UPDATE productos 
            SET nombre_producto = %s, precio_producto = %s, descripcion_producto = %s, 
            codigo_producto = %s, stock_producto = %s, informacion_adicional = %s, 
            oferta_producto = %s, id_categoria = %s
        """
        params = [nombre, precio, descripcion, codigo, stock, info_adicional, oferta, categoria_id]

        if imagen is not None:
            query += ", imagen_producto = %s"
            params.append(imagen)
        
        query += " WHERE id_producto = %s"
        params.append(product_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, params)
        self.mysql.connection.commit()
        cursor.close()
        
        
    # Metodo para ELIMINAR producto
    def delete_product(self, product_id):
        query = "DELETE FROM productos WHERE id_producto = %s"
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, (product_id,))
        self.mysql.connection.commit()
        cursor.close()


    # Metodo para mostrar todas las categorias
    def get_all_categories(self):
        query = "SELECT id_categoria, nombre_categoria FROM categoria"
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        categories = cursor.fetchall()
        cursor.close()
        return categories


    # Metodo para mostrar todos los productos
    def get_all_products(self):
        query = """
        SELECT p.id_producto, p.nombre_producto, p.precio_producto, p.descripcion_producto, p.codigo_producto,
        p.stock_producto, p.oferta_producto, c.nombre_categoria
        FROM productos p
        JOIN categoria c ON p.id_categoria = c.id_categoria
        """
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        return products


    # Metodo para traer productos por ID
    def get_product_by_id(self, product_id):
        cursor = self.mysql.connection.cursor()
        query = """
            SELECT id_producto, nombre_producto, precio_producto, descripcion_producto, codigo_producto,
            stock_producto, informacion_adicional, imagen_producto, oferta_producto, id_categoria
            FROM productos WHERE id_producto = %s
        """
        cursor.execute(query, (product_id,))
        producto = cursor.fetchone()
        cursor.close()
        return producto
        
        
    # Metodo para buscar productos
    def search_products(self, search_query):
        query = """
            SELECT p.id_producto, p.nombre_producto, p.precio_producto, p.descripcion_producto, p.codigo_producto,
            p.stock_producto, p.oferta_producto, c.nombre_categoria
            FROM productos p
            JOIN categoria c ON p.id_categoria = c.id_categoria
            WHERE p.nombre_producto LIKE %s OR p.descripcion_producto LIKE %s OR c.nombre_categoria LIKE %s
            """
        cursor = self.mysql.connection.cursor()
        search_term = f"%{search_query}%"
        cursor.execute(query, (search_term, search_term, search_term))
        products = cursor.fetchall()
        cursor.close()
        return products
    
    
    # Metodo para mostrar productos destacados
    def get_products(self, limit=None):
        query = "SELECT * FROM productos"
        if limit:
            query += " LIMIT %s"
            cursor = self.mysql.connection.cursor()
            cursor.execute(query, (limit,))
        else:
            cursor = self.mysql.connection.cursor()
            cursor.execute(query)
        return cursor.fetchall()
    
    
    # Metodo para mostrar los productos solamente que esten en oferta
    def get_products_in_offer(self):
        query = "SELECT * FROM productos WHERE oferta_producto = 1"
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        productos = cursor.fetchall()
        for producto in productos:
            producto['imagen_base64'] = base64.b64encode(producto['imagen_producto']).decode('utf-8') if producto['imagen_producto'] else None
        return productos
    
    
    # Metodo para filtrado de productos
    def get_filtered_products(self, nombre_producto=None, precio_min=None, precio_max=None, categoria=None, orden='nombre_producto'):
        # Lista de columnas válidas para ordenar
        columnas_validas = ['nombre_producto', 'precio_producto', 'nombre_categoria']

        # Validar que el campo de orden esté en la lista de columnas válidas
        if orden not in columnas_validas:
            orden = 'nombre_producto'  # Valor por defecto

        # Construir consulta dinámica
        query = """
        SELECT p.*, c.nombre_categoria
        FROM productos p
        JOIN categoria c ON p.id_categoria = c.id_categoria
        WHERE 1=1
        """
        params = []

        # Aplicar filtros dinámicamente
        if nombre_producto:
            query += " AND p.nombre_producto LIKE %s"
            params.append(f"%{nombre_producto}%")
        if precio_min is not None:
            query += " AND p.precio_producto >= %s"
            params.append(precio_min)
        if precio_max is not None:
            query += " AND p.precio_producto <= %s"
            params.append(precio_max)
        if categoria:
            query += " AND c.nombre_categoria = %s"
            params.append(categoria)

        # Añadir cláusula ORDER BY con una columna válida
        query += f" ORDER BY {orden}"

        # Ejecutar la consulta
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, params)
        productos = cursor.fetchall()
        cursor.close()
        return productos
    
    def get_product_by_id(self, producto_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM productos WHERE id_producto = %s"
        cursor.execute(query, (producto_id,))
        return cursor.fetchone()
