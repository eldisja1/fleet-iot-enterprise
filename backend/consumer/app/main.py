from .database import engine
from .models import Base
from .mqtt_client import start_mqtt

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    start_mqtt()
