import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pylint_enums',
    version='0.0.5',
    author='Christopher Cordero',
    author_email='ccordero@protonmail.com',
    description=('A Pylint plugin that checks for a specific implementation of'
                 ' Enum subclasses.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cs-cordero/pylint_enums',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    install_requires=[
        'pylint'
    ]
)
