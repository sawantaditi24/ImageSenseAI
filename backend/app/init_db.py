from app.db import Base, engine
from app.models import Screenshot

if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.") 