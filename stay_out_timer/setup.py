from setuptools import setup

setup(
    name="StayOutTimer",
    version="1.0",
    description="Таймер для игры Stay Out от Harper_IDS",
    author="Harper_IDS",
    py_modules=["main"],
    install_requires=[
        # No external dependencies needed as we use only standard library
    ],
)