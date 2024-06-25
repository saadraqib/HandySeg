from setuptools import setup, find_packages

setup(
    name='HandySeg',  
    version='0.5.0', # [0.7.0 is used, so don't use it again]
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'scipy',
        'matplotlib',
    ],
    author='SaadRaqib',
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
