from sqlmodel import SQLModel, create_engine, Session, text
from typing import Generator

class DatabaseService:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)

    def test_connection(self) -> bool:
        try:
            with Session(self.engine) as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    
    def create_tables(self)-> None:
        SQLModel.metadata.create_all(self.engine)

    
    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session