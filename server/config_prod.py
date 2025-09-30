DEBUG = False
DATABASE_URL = "postgresql://user:password@host:port/dbname"
API_KEY = os.environ.get('PROD_API_KEY') # Securely from env var