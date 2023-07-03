from setuptools import setup

setup(
    name='AuthorsNet',
    url='https://github.com/Nadav-Katz/arxiv-authors-net',
    author="Nadav Katz",
    author_email='nadav.katz3@mail.huji.ac.il',
    packages=['authors_net'],
    # Needed for dependencies
    install_requires=['pandas', 'networkx', 'tqdm'],
    version='0.4',
    description='A code for creating a authors collaboration network from the arxiv dataset',
    # Readme
    long_description=open('README.md').read(),
)
