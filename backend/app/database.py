import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

# Database URL configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set, construct it from individual components
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "stock_rec")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔌 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'DATABASE_URL'}")

# Create engine with connection pooling and error handling
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        echo=False           # Set to True for SQL debugging
    )
    
    # Test the connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Database connection successful")
    
except OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    print("Please check your database configuration and ensure PostgreSQL is running")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        raise

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
