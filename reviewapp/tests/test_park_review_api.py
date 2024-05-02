from httpx import AsyncClient
import pytest
from main import app  # make sure this import aligns with your project structure

# Assuming your jwt_handler has a function to create access tokens
from auth.jwt_handler import create_access_token
from models.reviews import Reviews


@pytest.fixture
async def access_token_admin() -> str:
    # Replace 'admin@example.com' with a real admin email used in your setup
    return create_access_token("admin@example.com")

@pytest.fixture
async def access_token_user() -> str:
    # Replace 'user@example.com' with a real user email used in your setup
    return create_access_token("user@example.com")

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def create_review(client, access_token_user):
    review_data = {
        "park_name": "Yellowstone",
        "content": "Beautiful scenery and lots of wildlife.",
        "rating": 5
    }
    headers = {"Authorization": f"Bearer {access_token_user}"}
    response = await client.post("/reviews/post/", json=review_data, headers=headers)
    return response.json()

@pytest.mark.asyncio
async def test_get_all_reviews(client):
    response = await client.get("/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_single_review(client, create_review):
    review_id = create_review['_id']
    response = await client.get(f"/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()['content'] == "Beautiful scenery and lots of wildlife."

@pytest.mark.asyncio
async def test_post_review(client, access_token_user):
    review_data = {
        "park_name": "Zion",
        "content": "Great trails and not too crowded.",
        "rating": 4
    }
    headers = {"Authorization": f"Bearer {access_token_user}"}
    response = await client.post("/reviews/post/", json=review_data, headers=headers)
    assert response.status_code == 201
    assert response.json()['content'] == "Great trails and not too crowded."

@pytest.mark.asyncio
async def test_unauthorized_access_to_post_review(client):
    review_data = {
        "park_name": "Zion",
        "content": "Great trails and not too crowded.",
        "rating": 4
    }
    response = await client.post("/reviews/post/", json=review_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_review(client, access_token_user, create_review):
    review_id = create_review['_id']
    update_data = {"content": "Updated content", "rating": 5}
    headers = {"Authorization": f"Bearer {access_token_user}"}
    response = await client.put(f"/reviews/update/{review_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()['content'] == "Updated content"

@pytest.mark.asyncio
async def test_delete_review(client, access_token_user, create_review):
    review_id = create_review['_id']
    headers = {"Authorization": f"Bearer {access_token_user}"}
    response = await client.delete(f"/reviews/delete/{review_id}", headers=headers)
    assert response.status_code == 202
    # Test to ensure that the review is actually deleted
    get_response = await client.get(f"/reviews/{review_id}")
    assert get_response.status_code == 404

# Additional tests for unauthorized deletes, invalid inputs, etc., should also be included.
