from setuptools import setup, find_packages

setup(
    name="port-view",
    version="0.1.0",
    description="...",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    package_data={
        "*": ["py.typed", "client/**"],
    },
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn[standard]>=0.22.0",
        "aiofiles>=0.8.0",
        "python-multipart"
    ],
    python_requires=">=3.12,<4",
    entry_points={
        "console_scripts": [
            "port-view=src.server.main:main",
        ],
    },
)
