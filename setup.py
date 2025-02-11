from setuptools import setup, find_packages

setup(
    name="mcp",
    version="1.0.0",
    description="Modular Control Platform - An integrated AI and cognitive tools framework",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic>=0.10.0",
        "openai>=4.0.0",
        "streamlit>=1.0.0",
        "pandas>=1.0.0",
        "numpy>=1.20.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "networkx>=2.0",
        "beautifulsoup4>=4.9.0",
        "requests>=2.25.0",
        "google-api-python-client>=2.0.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "mypy>=0.900",
        ]
    },
    entry_points={
        "console_scripts": [
            "mcp=cli.mcp:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)