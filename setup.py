from setuptools import setup, find_packages

setup(
    name="mcp",
    version="1.0.0",
    description="Modular Control Platform - An integrated AI and cognitive tools framework",
    author="Ryan Oates",
    author_email="ryanfullstack@icloud.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic>=0.45.2,<0.46",
        "openai>=1.61.0,<2",
        "typer>=0.9.0,<0.10",
        "rich>=13.7.0,<14",
        "requests>=2.31.0,<3",
        "numpy>=1.24.0",
        "pandas>=2.1.0",
        "plotly>=5.18.0",
        "google-generativeai>=0.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "ruff>=0.1.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp=mcp.cli.main:app",
            "mcp-server=mcp.server.main:run",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)