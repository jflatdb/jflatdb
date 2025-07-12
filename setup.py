from setuptools import setup, find_packages

setup(
    name="jflatdb",
    version="0.0.3",
    author="Akki",
    author_email="akki.jflatdb@gmail.com",
    description="A lightweight JSON-based flat file database system.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jflatdb/jflatdb",  # Update this to your repo
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "jflatdb = jflatdb.main:main",  # Adjust if your main.py is elsewhere
        ],
    },
)
