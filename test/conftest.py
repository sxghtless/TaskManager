import os
from pathlib import Path
from unittest.mock import patch

from dotenv import load_dotenv

from utils import include_routers

load_dotenv(Path(__file__).parent.parent / ".env")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import Base, get_session
from main import app

settings = get_settings()

include_routers(app, os.path.join(os.path.abspath(settings.project_path), "src"))

default_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:{settings.POSTGRES_PORT}/postgres"
default_engine = create_engine(default_url, isolation_level="AUTOCOMMIT")
with default_engine.connect() as conn:
    exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='taskmanager_test'")).fetchone()
    if not exists:
        conn.execute(text("CREATE DATABASE taskmanager_test"))
default_engine.dispose()

TEST_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:{settings.POSTGRES_PORT}/taskmanager_test"
engine_test = create_engine(TEST_DATABASE_URL)

engine_test = create_engine(TEST_DATABASE_URL)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db():
    with SessionTest() as session:
        yield session
        session.rollback()


@pytest.fixture
def client(db):
    def override_get_session():
        yield db

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_redis():
    with patch("utils.redis.redis_client") as mock:
        mock.get.return_value = None
        mock.setex.return_value = True
        mock.delete.return_value = True
        yield mock