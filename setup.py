from setuptools import setup, find_packages

setup(
    name="reverse-shell-killer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil>=7.0.0",
        "python-dotenv>=1.1.0",
        "google-genai>=1.11.0",
        "pydantic>=2.11.3",
    ],
    entry_points={
        "console_scripts": [
            "reverse-shell-killer=main:main",
        ],
    },
)
