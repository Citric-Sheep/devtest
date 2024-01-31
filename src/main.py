from .factory import create_app
from .database import Base, engine


Base.metadata.create_all(bind=engine)
app = create_app()