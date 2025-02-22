from setuptools import setup, find_packages

setup(
    name="magnatronic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "jinja2",
        "pydantic"
    ],
    author="Magnatronic Team",
    description="Magnatronic Multi-Agent System",
    python_requires=">=3.8"
)