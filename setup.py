from setuptools import setup, find_packages

setup(
    name="reverse-shell-killer",
    version="0.1.0",
    description="Tool to identify and terminate reverse shells",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ahmed", 
    py_modules=["main"], 
    python_requires=">=3.13",
    install_requires=[
        "psutil>=7.0.0",
    ],
    entry_points={
        "console_scripts": [
            "reverse-shell-killer=main:main",  # Creates a command-line executable
        ],
    },
)