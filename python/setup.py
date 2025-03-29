from setuptools import setup, find_packages

setup(
    name="llamaquest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pyxel>=1.9.0",
        "pydantic>=2.0.0",
        "maturin>=1.0.0",
    ],
    python_requires=">=3.8",
    author="LlamaSearch AI",
    author_email="info@llamasearch.ai",
    description="A modern, retro-style adventure game with AI-driven NPCs",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/llamasearch/llamaquest",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
    ],
    entry_points={
        "console_scripts": [
            "llamaquest=llamaquest.__main__:main",
        ],
    },
) 