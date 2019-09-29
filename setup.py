from setuptools import setup

from afmt import meta 

with open('README.md', 'r') as f:
  long_desc = f.read()

setup(
  name=meta.NAME,
  version=meta.VERSION,
  description=meta.DESC,
  long_description=long_desc,
  long_description_content_type='text/markdown',
  url='https://github.com/adzierzanowski/afmt',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['afmt'],
  zip_safe=False,
  python_requires='>=3.6',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Terminals',
    'Topic :: Text Processing :: General'
  ]
)
