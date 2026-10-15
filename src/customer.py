class Customer:
    def __init__(self, id: int, name: str, email: str):

        if type(id) is not int or id <= 0:
            raise ValueError("El ID debe ser un entero positivo")
        
        self.id = id
        self.name = name
        self.email = email

if __name__ == "__main__":
    customer = Customer(245, "Ana Demo", "ana@example.com")
    print(customer.id)
    print(customer.name)
    print(customer.email)