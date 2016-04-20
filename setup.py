try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()

requirements = [
]

dependencies = [
]

test_requirements = [
]

setup(
    name='collabo',
    version='0.1.0',
    description='Collabo - Framework for Multi-task Workers',
    long_description=readme,
    author='Jinyong Lee',
    author_email='gullpong9@gmail.com',
    url='https://github.com/gullpong/collabo',
    packages=[
        'collabo',
    ],
    package_dir={
        'collabo': 'collabo',
    },
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependencies,
    # test_suite='tests',
    # tests_require=test_requirements
)
