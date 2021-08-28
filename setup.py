from setuptools import setup, find_packages

setup(
  name = 'rotary-embedding-tensorflow',
  packages = find_packages(),
  version = '0.1.0',
  license='MIT',
  description = 'Rotary Embedding - Tensorflow',
  author = 'Arya Aftab',
  author_email = 'arya.aftab@gmail.com',
  url = 'https://github.com/AryaAftab/rotary-embedding-tensorflow',
  keywords = [
    'deep learning',
    'tensorflow',
    'positional embedding'    
  ],
  install_requires=[
    'numpy>=1.18.5',
    'tensorflow>=2.3'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
