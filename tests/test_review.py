import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import Product
from app.models.review import Review
from app.models.category import Category
from app.models.users import User


async def setup_test_data(db_session: AsyncSession, product_id: int = 1):

    category = await db_session.get(Category, 1)
    if not category:
        category = Category(id=1, name="Test Category")
        db_session.add(category)


    user = await db_session.get(User, 1)
    if not user:
        user = User(
            id=1,
            email="test@example.com",
            role="admin",
            auth_provider="local"
        )
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
async def test_add_review_success(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=1)

    payload = {"text": "Ajoyib mahsulot!", "rate": 5, "product_id": 1}
    response = await client.post("/review/", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["text"] == payload["text"]


@pytest.mark.asyncio
async def test_add_review_product_not_found(client: AsyncClient, db_session: AsyncSession):

    user = User(id=1, email="test@example.com", role="admin", auth_provider="local")
    db_session.add(user)
    await db_session.commit()

    payload = {"text": "Yomon emas", "rate": 4, "product_id": 999}
    response = await client.post("/review/", json=payload)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=2)

    review1 = Review(text="Zo'r", rate=5, user_id=1, product_id=2)
    review2 = Review(text="Yomon", rate=2, user_id=1, product_id=2)
    db_session.add_all([review1, review2])
    await db_session.commit()

    response = await client.get("/review/2")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_review_success(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=3)

    review = Review(text="Eski matn", rate=3, user_id=1, product_id=3)
    db_session.add(review)
    await db_session.commit()

    response = await client.put(f"/review/{review.id}", json={"text": "Yangi matn", "rate": 5})
    assert response.status_code == 200
    assert response.json()["text"] == "Yangi matn"


@pytest.mark.asyncio
async def test_delete_review_success(client: AsyncClient, db_session: AsyncSession):
    await setup_test_data(db_session, product_id=4)

    review = Review(text="O'chiriladigan sharh", rate=1, user_id=1, product_id=4)
    db_session.add(review)
    await db_session.commit()

    response = await client.delete(f"/review/{review.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Deleted successfully"