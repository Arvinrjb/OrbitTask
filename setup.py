from pathlib import Path

from setuptools import find_packages, setup


ROOT_DIR = Path(__file__).parent


setup(
    name="orbittask",
    version="1.0.0",
    description="This is a Django app for managing processes and executing I/O bound and CPU bound tasks at various times.",
    long_description=(ROOT_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/Arvinrjb/OrbitTask",
    author="arvinrjb",
    packages=find_packages(where="demo", include=["orbittask*"]),
    package_dir={"": "demo"},
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.2",
        "djangorestframework>=3.14",
        "redis>=5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
            "pytest-django>=4.8",
            "pytest-cov>=5.0",
            "ruff>=0.6",
        ],
    },
    include_package_data=True,
    license="MIT",
)
