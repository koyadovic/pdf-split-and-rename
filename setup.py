from distutils.core import setup


setup(
    name='PDF Split and rename',
    version='0.1',
    description='PDF Split and rename',
    author='Miguel Collado',
    author_email='m.collado.gomez@gmail.com',
    url='https://www.python.org/',
    packages=['distutils', 'distutils.command'],
    install_requires=[
        'Pillow',
        'PyPDF2',
        'pytesseract'
    ]
)
