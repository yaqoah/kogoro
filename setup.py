import sys
import setuptools


setuptools.setup(
    name='Kogoro',
    packages=['bot'],
    url='https://github.com/yaqoah/Kogoro',
    license='MIT',
    author='Yaqoah',
    author_email='balotelli-7amood@hotmail.com',
    description='Telegram bot for Football predictions and statistics',
    entry_points={
        "console_scripts": ["kogoro=kogoro.__kogoro__:main"]
    },
    python_requires=">=3.9"
)
