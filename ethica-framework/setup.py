from setuptools import setup, find_packages

setup(
    name="ethica-framework",
    version="1.0.0",
    description="Enterprise-Grade Ethical AI Decision System",
    author="Ethica.AI",
    author_email="hello@ethica.ai",
    url="https://ethica.ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "mistralai>=0.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
