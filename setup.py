from setuptools import find_packages, setup

exec(open("doca/version.py").read())

setup(
    name="doca",
    version=__version__,
    url="git@github.com:peekwez/doca.git",
    author="Kwesi P Apponsah",
    author_email="kwesi@kwap-consulting.com",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "pydantic", "boto3", "moto", "faker", "devtools",
        "kombu", "sphinx", "rinohtype", "shortuuid", "pandas",
        "pillow", "pdf2image", "rich", "PyPDF2", "humanize",
        "PyCryptodome", "sphinx-rtd-theme", "python-dotenv[cli]",
        "google-cloud-storage", "google-cloud-pubsub", "google-cloud-documentai",
        "google-cloud-bigquery", "google-cloud-logging", "azure-core",
        "azure-storage-blob", "azure-storage-queue", "azure-ai-formrecognizer",
        "functions-framework", "pyarrow", "textdistance", "fuzzywuzzy",
        "python-Levenshtein", "scikit-learn", "googlemaps", "sqlalchemy",
        "openpyxl", "tqdm", "pyodbc"
    ],
    entry_points={
        "console_scripts": [
            "doca=doca.cmd:cli"
        ]
    },
    extras_require={
        "dev": ["pytest", "flake8", "coverage", "devtools", "rich"]
    },
    description="Document Analysis Pipeline"
)
