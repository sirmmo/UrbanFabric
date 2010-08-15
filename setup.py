from distutils.core import setup

setup(name='UrbanFabric',
    version='1.0',
    description='Urban Utilities Inventory',
    author='Marco Montanari',
    author_email='sirmmo@gmail.com',
    package_dir={'': 'uf'},
    install_requires=[
        'django',
        'GDAL',
        'PIL',
        'psycopg2'
    ]
)
