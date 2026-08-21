import pytest
from httpx import AsyncClient


async def create_product_helper(client: AsyncClient) -> int:
    cat_res = await client.post("/category/", json={"name": "Elektronika"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "iPhone 15 Pro",
        "description": "Yangi model",
        "price": 1300,
        "is_stock": True,
        "category_id": cat_id
    })
    return prod_res.json()["id"]


@pytest.mark.asyncio
async def test_create_variant_success(client: AsyncClient):
    product_id = await create_product_helper(client)

    variant_payload = {
        "name": "Rang / Xotira",
        "product_id": product_id
    }
    response = await client.post("/variant/", json=variant_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Rang / Xotira"
    assert data["product_id"] == product_id
    assert "id" in data


@pytest.mark.asyncio
async def test_create_variant_invalid_product_id(client: AsyncClient):
    invalid_payload = {
        "name": "O'lcham",
        "product_id": 99999
    }
    response = await client.post("/variant/", json=invalid_payload)

    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_variant_list(client: AsyncClient):
    response = await client.get("/variant/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_variant(client: AsyncClient):
    product_id = await create_product_helper(client)

    var_res = await client.post("/variant/", json={
        "name": "Eski Variant",
        "product_id": product_id
    })
    variant_id = var_res.json()["id"]

    update_payload = {
        "name": "Yangi Variant"
    }
    response = await client.put(f"/variant/{variant_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Yangi Variant"
    assert data["product_id"] == product_id


@pytest.mark.asyncio
async def test_delete_variant(client: AsyncClient):
    product_id = await create_product_helper(client)

    var_res = await client.post("/variant/", json={
        "name": "O'chiriladigan Variant",
        "product_id": product_id
    })
    variant_id = var_res.json()["id"]

    delete_res = await client.delete(f"/variant/{variant_id}")
    assert delete_res.status_code == 204

    update_res = await client.put(f"/variant/{variant_id}", json={
        "name": "Test"
    })
    assert update_res.status_code == 404