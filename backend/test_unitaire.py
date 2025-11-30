import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import AsyncMock, patch, Mock

# On importe l'application et les composants de base depuis main.py
from main import app, get_db, Base

# --- CONFIGURATION DE LA BASE DE TEST (SQLite en mémoire) ---
# Cela permet de tester sans toucher à votre PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# On crée les tables vides pour le test
Base.metadata.create_all(bind=engine)

# On remplace la dépendance de base de données par celle de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- VARIABLES GLOBALES DE TEST ---
TEST_USER = "testuser"
TEST_PASSWORD = "testpassword123"
tokens = {} # Pour stocker le token entre les tests

# --- LES TESTS ---

def test_1_register():
    """Teste l'inscription d'un nouvel utilisateur"""
    response = client.post(
        "/register",
        json={"username": TEST_USER, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created"}

def test_2_register_duplicate():
    """Teste qu'on ne peut pas créer deux fois le même user"""
    response = client.post(
        "/register",
        json={"username": TEST_USER, "password": TEST_PASSWORD},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_3_login():
    """Teste le login et récupère le Token JWT"""
    response = client.post(
        "/login",
        data={"username": TEST_USER, "password": TEST_PASSWORD}, # Note: form-data, pas json
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # On sauvegarde le token pour les tests suivants
    tokens["jwt"] = data["access_token"]

def test_4_login_bad_credentials():
    """Teste un mauvais mot de passe"""
    response = client.post(
        "/login",
        data={"username": TEST_USER, "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_5_translate_unauthorized():
    """Teste l'accès à /translate SANS token"""
    response = client.post(
        "/translate",
        json={"text": "Hello", "direction": "en-fr"}
    )
    # Doit retourner 401 Unauthorized
    assert response.status_code == 401

@patch("httpx.AsyncClient.post")
def test_6_translate_success(mock_post):
    """
    Teste la traduction AVEC token.
    On 'Mock' (simule) Hugging Face pour ne pas faire de vrai appel réseau.
    """
    # 1. On configure le simulateur pour qu'il réponde comme Hugging Face
    # mock_response = AsyncMock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"translation_text": "Bonjour tout le monde"}]
    mock_post.return_value = mock_response

    # 2. On fait l'appel à notre API
    response = client.post(
        "/translate",
        json={"text": "Hello world", "direction": "en-fr"},
        headers={"Authorization": f"Bearer {tokens['jwt']}"} # On utilise le token récupéré
    )

    # 3. Vérifications
    assert response.status_code == 200
    assert response.json() == {"translation": "Bonjour tout le monde"}