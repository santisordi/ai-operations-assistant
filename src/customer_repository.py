from .customer import Customer

class CustomerRepository:
    def get_by_id(self, customer_id: int) -> Customer | None:
        raise NotImplementedError
