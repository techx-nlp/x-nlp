import pathlib
from setuptools import setup, find_packages


PATH = pathlib.Path(__file__).parent
README = (PATH / 'README.md').read_text()

setup(
    name='x-nlp',
    version='0.1.2',
    description='Library of helper functions for Natural Language Processing '
                'related algorithms (designed for the TechX NLP course).',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/techx-nlp/x-nlp',
    author='David Ma',
    author_email='davidma@davidma.cn',
    license='MIT',
    packages=find_packages()
)