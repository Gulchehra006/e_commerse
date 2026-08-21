import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category_and_product(client: AsyncClient):
    category_res = await client.post("/category/", json={"name": "Elektronika"})
    assert category_res.status_code == 201
    category_id = category_res.json()["id"]

    product_data = {
        "name": "iPhone 15",
        "description": "Yangi va zo'r telefon",
        "price": 1200,
        "is_stock": True,
        "category_id": category_id
    }
    response = await client.post("/product/", json=product_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "iPhone 15"
    assert data["price"] == 1200
    assert data["category_id"] == category_id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_products_pagination(client: AsyncClient):
    response = await client.get("/product/")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    cat_res = await client.post("/category/", json={"name": "Texnika"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "Noutbuk",
        "description": "Eski model",
        "price": 500,
        "is_stock": True,
        "category_id": cat_id
    })
    product_id = prod_res.json()["id"]

    update_data = {
        "name": "Noutbuk Pro",
        "price": 800
    }
    response = await client.put(f"/product/{product_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Noutbuk Pro"
    assert response.json()["price"] == 800


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    cat_res = await client.post("/category/", json={"name": "Maishiy"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "Muzlatgich",
        "description": "Katta",
        "price": 300,
        "is_stock": True,
        "category_id": cat_id
    })
    product_id = prod_res.json()["id"]

    delete_res = await client.delete(f"/product/{product_id}")
    assert delete_res.status_code == 204

    update_res = await client.put(f"/product/{product_id}", json={"name": "Test"})
    assert update_res.status_code == 404