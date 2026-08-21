import pytest
from httpx import AsyncClient


async def create_variant_helper(client: AsyncClient) -> int:
    cat_res = await client.post("/category/", json={"name": "Elektronika"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "iPhone 15",
        "description": "Yangi model",
        "price": 1200,
        "is_stock": True,
        "category_id": cat_id
    })
    product_id = prod_res.json()["id"]

    variant_res = await client.post("/variant/", json={
        "name": "Rang / Xotira",
        "product_id": product_id
    })
    return variant_res.json()["id"]


@pytest.mark.asyncio
async def test_create_option_success(client: AsyncClient):
    variant_id = await create_variant_helper(client)

    option_payload = {
        "name": "Qora 256GB",
        "image": "https://example.com/black.jpg",
        "variant_id": variant_id
    }
    response = await client.post("/option/", json=option_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Qora 256GB"
    assert data["image"] == "https://example.com/black.jpg"
    assert data["variant_id"] == variant_id
    assert "id" in data


@pytest.mark.asyncio
async def test_create_option_invalid_variant_id(client: AsyncClient):
    invalid_payload = {
        "name": "Oq 128GB",
        "image": "https://example.com/white.jpg",
        "variant_id": 99999
    }
    response = await client.post("/option/", json=invalid_payload)

    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_option_list(client: AsyncClient):
    response = await client.get("/option/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_option(client: AsyncClient):
    variant_id = await create_variant_helper(client)

    opt_res = await client.post("/option/", json={
        "name": "Eski nom",
        "image": "https://example.com/old.jpg",
        "variant_id": variant_id
    })
    option_id = opt_res.json()["id"]

    update_payload = {
        "name": "Yangi nom",
        "image": "https://example.com/new.jpg",
        "variant_id": variant_id
    }
    response = await client.put(f"/option/{option_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Yangi nom"
    assert data["image"] == "https://example.com/new.jpg"


@pytest.mark.asyncio
async def test_delete_option(client: AsyncClient):
    variant_id = await create_variant_helper(client)

    opt_res = await client.post("/option/", json={
        "name": "O'chiriladigan option",
        "image": "https://example.com/delete.jpg",
        "variant_id": variant_id
    })
    option_id = opt_res.json()["id"]

    delete_res = await client.delete(f"/option/{option_id}")
    assert delete_res.status_code == 204

    update_res = await client.put(f"/option/{option_id}", json={
        "name": "Test",
        "image": "https://example.com/test.jpg",
        "variant_id": variant_id
    })
    assert update_res.status_code == 404