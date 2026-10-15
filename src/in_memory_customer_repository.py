from .customer_repository import CustomerRepository
from .customer import Customer

class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers = {
            245: Customer(245, "Ana Demo", "ana@example.com")
        }

    def get_by_id(self, customer_id: int) -> Customer | None:

        if customer_id in self.customers:
            return self.customers[customer_id]
        else: 
            return None
if __name__ == "__main__":
    repositorio = InMemoryCustomerRepository()
    cliente = repositorio.get_by_id(245)

    if cliente is not None:
        print(cliente.id)
        print(cliente.name)
        print(cliente.email)

    print(repositorio.get_by_id(999))