class Cart:
    def __init__(self):
        # Cuando se crea la clase, inicializamos su diccionario interno
        self.items = {}
        
    def add_item(self, product, quantity, available_stock):
        # La misma validación de antes
        if quantity > available_stock:
            raise ValueError("No hay suficiente stock")
            
        # Lo guardamos en su diccionario interno
        self.items[product] = quantity
        
    def clear(self):
        # Vaciamos su diccionario interno
        self.items.clear()
