import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product
from app.models.favourite import Favourite
from app.models.category import Category
from app.models.users import User


async def setup_test_data(db_session: AsyncSession, product_id: int = 1):
    category = await db_session.get(Category, 1)
    if not category:
        category = Category(id=1, name="Test Category")
        db_session.add(category)

    user = await db_session.get(User, 1)
    if not user:
        user = User(id=1, email="test@example.com", role="admin", auth_provider="local")
        db_session.add(user)

    product = await db_session.get(Product, product_id)
    if not product:
        product = Product(
            id=product_id,
            name=f"Test Product {product_id}",
            price=100.0,
            description="Test tavsifi",
            category_id=1
        )
        db_session.add(product)

    await db_session.commit()


@pytest.mark.asyncio
async def test_add_favorite_success(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=1)

    response = await client.post("/favorite/", json={"product_id": 1})
    assert response.status_code == 201
    assert response.json()["message"] == "Favourite item was successfully added"


@pytest.mark.asyncio
async def test_toggle_favorite_removes_item(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=1)

    fav = Favourite(user_id=1, product_id=1)
    db_session.add(fav)
    await db_session.commit()

    response = await client.post("/favorite/", json={"product_id": 1})
    assert response.status_code == 201
    assert response.json()["message"] == "Favourite item was successfully deleted"


@pytest.mark.asyncio
async def test_get_my_favorites_success(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=1)

    fav = Favourite(user_id=1, product_id=1)
    db_session.add(fav)
    await db_session.commit()

    response = await client.get("/favorite/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["product_id"] == 1


@pytest.mark.asyncio
async def test_add_favorite_product_not_found(client: AsyncClient, db_session: AsyncSession):
    user = await db_session.get(User, 1)
    if not user:
        user = User(id=1, email="test@example.com", role="admin", auth_provider="local")
        db_session.add(user)
        await db_session.commit()

    response = await client.post("/favorite/", json={"product_id": 999})
    assert response.status_code == 404