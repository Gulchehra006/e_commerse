# 1. Python asosini olish
FROM python:3.14

# 2. Ishchi papkani belgilash
WORKDIR /app

# 3. Kutubxonalar ro'yxatini nusxalash
COPY requirements.txt .

# 4. Kutubxonalarni o'rnatish
RUN pip install -r requirements.txt

# 5. Kodni nusxalash
COPY . .

# 6. Ilovani ishga tushirish
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]