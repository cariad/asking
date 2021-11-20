from pathlib import Path

from setuptools import setup  # pyright: reportMissingTypeStubs=false

from asking import __version__

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Typing :: Typed",
]

if "a" in __version__:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in __version__:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="Ask questions and get answers",
    entry_points={
        "console_scripts": [
            "startifact=startifact.__main__:entry",
        ],
    },
    include_package_data=True,
    install_requires=[
        "ruamel.yaml~=0.17",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="asking",
    packages=[
        "asking",
    ],
    package_data={
        "asking": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/asking",
    version=__version__,
)
