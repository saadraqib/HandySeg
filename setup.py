from setuptools import setup, find_packages

setup(
    name='HandySeg',  
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'scipy',
        'matplotlib',
    ],
    author='Saad Raqib',  
    author_email='saad.rqaziz@gmail.com', 
    description='A package for line and word segmentation of handwritten scanned text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/saadraqib/HandySeg',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
