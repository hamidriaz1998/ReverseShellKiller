from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="reverse-shell-killer",
    version="0.1.0",
    description="Tool to identify and terminate reverse shells",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ahmed",
    packages=find_packages() + ["revshell_detector"],
    py_modules=["main"],
    python_requires=">=3.13",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reverse-shell-killer=main:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
)