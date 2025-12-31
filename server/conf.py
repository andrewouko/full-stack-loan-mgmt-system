import os

from models import Config


def get_config() -> Config:
    datastore_type = os.getenv("DATASTORE_TYPE", "in_memory")
    database_url = os.getenv("DATABASE_URL", None)
    
    if datastore_type not in ("in_memory", "database"):
        raise ValueError(
            f"Invalid DATASTORE_TYPE: {datastore_type}. Must be 'in_memory' or 'database'."
        )
    
    if datastore_type == "database" and not database_url:
        raise ValueError(
            "DATABASE_URL must be set when DATASTORE_TYPE is 'database'."
        )
    
    return Config(
        datastore_type=datastore_type,
        database_url=database_url
    )