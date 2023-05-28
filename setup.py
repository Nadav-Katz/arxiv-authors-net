from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AuthorsNet',
    url='https://github.com/Nadav-Katz/arxiv-authors-net',
    author="Nadav Katz",
    author_email='nadav.katz3@mail.huji.ac.il',
    # Needed to actually package something
    packages=['authors_net'],
    # Needed for dependencies
    install_requires=['pandas', 'networkx', 'tqdm'],
    # *strongly* suggested for sharing
    version='0.1',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)