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
    description="Asking questions and getting answers",
    entry_points={
        "console_scripts": [
            "asking=asking.__main__:entry",
        ],
    },
    include_package_data=True,
    install_requires=[
        "ansiscape~=1.0.0",
        "ansiwrap~=0.8",
        "cline~=1.1",
        "pyyaml~=6.0",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="asking",
    packages=[
        "asking",
        "asking.actions",
        "asking.loaders",
        "asking.models",
        "asking.prompts",
        "asking.protocols",
        "asking.tasks",
    ],
    package_data={
        "asking": ["py.typed"],
        "asking.actions": ["py.typed"],
        "asking.loaders": ["py.typed"],
        "asking.models": ["py.typed"],
        "asking.prompts": ["py.typed"],
        "asking.protocols": ["py.typed"],
        "asking.tasks": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/asking",
    version=__version__,
)
