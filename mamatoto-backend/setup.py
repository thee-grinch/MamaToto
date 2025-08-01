from setuptools import setup, find_packages

setup(
    name="mamatoto-backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose",
        "passlib",
        "python-dateutil",
        "alembic",
        "gunicorn",
        "httpx",
        "pytest",
        "pytest-asyncio",
        "pydantic-settings",
        "python-multipart",
    ],
)