from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_by_id(self, client_id: str) -> Client | None:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_by_email(self, email: str) -> Client | None:
        return self.db.query(Client).filter(Client.email == email).first()

    def update(self, client: Client) -> Client:
        self.db.commit()
        self.db.refresh(client)
        return client
