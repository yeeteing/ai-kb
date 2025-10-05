from sqlalchemy import create_engine #makes a connection “engine” to your database.
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

#Creates a database engine using the connection string
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True) #pool_pre_ping=True makes sure SQLAlchemy checks if a DB connection is still alive before reusing it
#SessionLocal is a factory for creating new DB Session objects that are bound to the engine.
#autocommit=False => you control when to commit changes.
#autoflush=False => SQLAlchemy won’t automatically flush changes before queries (gives you more control).
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base() #Base class for your ORM models to inherit from.
