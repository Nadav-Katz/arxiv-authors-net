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
    version='0.2',
    description='An python package for craeting Arxiv Co-Authorship network',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)