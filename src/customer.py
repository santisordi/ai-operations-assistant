class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

customer = Customer(245, "Ana Demo", "ana@example.com")

print(customer.id)
print(customer.name)
print(customer.email)