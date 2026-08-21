import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_media_success(client: AsyncClient):
    cat_res = await client.post("/category/", json={"name": "Elektronika"})
    assert cat_res.status_code == 201
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "iPhone 15",
        "description": "Yangi model",
        "price": 1200,
        "is_stock": True,
        "category_id": cat_id
    })
    assert prod_res.status_code == 201
    product_id = prod_res.json()["id"]

    media_payload = {
        "image": "https://example.com/iphone.jpg",
        "main": True,
        "product_id": product_id
    }
    response = await client.post("/media/", json=media_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["image"] == "https://example.com/iphone.jpg"
    assert data["main"] is True
    assert data["product_id"] == product_id
    assert "id" in data


@pytest.mark.asyncio
async def test_create_media_invalid_product_id(client: AsyncClient):
    invalid_payload = {
        "image": "https://example.com/test.jpg",
        "main": False,
        "product_id": 9999
    }
    response = await client.post("/media/", json=invalid_payload)

    assert response.status_code == 400
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_media_list(client: AsyncClient):
    response = await client.get("/media/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_media(client: AsyncClient):
    cat_res = await client.post("/category/", json={"name": "Aksessuarlar"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "AirPods",
        "description": "Simsiz quloqchin",
        "price": 200,
        "is_stock": True,
        "category_id": cat_id
    })
    product_id = prod_res.json()["id"]

    media_res = await client.post("/media/", json={
        "image": "https://example.com/old.jpg",
        "main": False,
        "product_id": product_id
    })
    media_id = media_res.json()["id"]

    update_payload = {
        "image": "https://example.com/new.jpg",
        "main": True
    }
    response = await client.put(f"/media/{media_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["image"] == "https://example.com/new.jpg"
    assert data["main"] is True


@pytest.mark.asyncio
async def test_delete_media(client: AsyncClient):
    cat_res = await client.post("/category/", json={"name": "Gadget"})
    cat_id = cat_res.json()["id"]

    prod_res = await client.post("/product/", json={
        "name": "Smart Watch",
        "description": "Aqlli soat",
        "price": 150,
        "is_stock": True,
        "category_id": cat_id
    })
    product_id = prod_res.json()["id"]

    media_res = await client.post("/media/", json={
        "image": "https://example.com/watch.jpg",
        "main": True,
        "product_id": product_id
    })
    media_id = media_res.json()["id"]

    delete_res = await client.delete(f"/media/{media_id}")
    assert delete_res.status_code == 204

    update_res = await client.put(f"/media/{media_id}", json={
        "image": "https://example.com/fail.jpg",
        "main": False
    })
    assert update_res.status_code == 404