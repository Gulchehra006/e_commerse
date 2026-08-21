import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    response = await client.post("/category/", json={"name": "Elektronika"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Elektronika"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_category_missing_field(client: AsyncClient):
    response = await client.post("/category/", json={})

    assert response.status_code == 422



@pytest.mark.asyncio
async def test_get_categories_empty(client: AsyncClient):
    response = await client.get("/category/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    await client.post("/category/", json={"name": "Kiyim"})
    await client.post("/category/", json={"name": "Oziq-ovqat"})

    response = await client.get("/category/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [item["name"] for item in data]
    assert "Kiyim" in names
    assert "Oziq-ovqat" in names


@pytest.mark.asyncio
async def test_update_category(client: AsyncClient):

    create = await client.post("/category/", json={"name": "Eski nom"})
    category_id = create.json()["id"]

    response = await client.put(f"/category/{category_id}", json={"name": "Yangi nom"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Yangi nom"


@pytest.mark.asyncio
async def test_update_category_not_found(client: AsyncClient):
    response = await client.put("/category/9999", json={"name": "Yangi nom"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Kategoriya topilmadi"


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient):

    create = await client.post("/category/", json={"name": "O'chiriladigan"})
    category_id = create.json()["id"]

    response = await client.delete(f"/category/{category_id}")
    assert response.status_code == 204

    get_all = await client.get("/category/")
    ids = [item["id"] for item in get_all.json()]
    assert category_id not in ids


@pytest.mark.asyncio
async def test_delete_category_not_found(client: AsyncClient):
    response = await client.delete("/category/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Kategoriya topilmadi"


@pytest.mark.asyncio
async def test_delete_category_then_get(client: AsyncClient):

    r1 = await client.post("/category/", json={"name": "Birinchi"})
    r2 = await client.post("/category/", json={"name": "Ikkinchi"})

    await client.delete(f"/category/{r1.json()['id']}")

    get_all = await client.get("/category/")
    data = get_all.json()
    assert len(data) == 1
    assert data[0]["name"] == "Ikkinchi"