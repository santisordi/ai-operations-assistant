from .customer_repository import CustomerRepository

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository