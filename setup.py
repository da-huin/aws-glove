# Use this command for deploy.
#   python3 setup.py sdist bdist_wheel
#   python3 -m twine upload --skip-existing dist/*

import io
from setuptools import find_packages, setup

setup(name='aws_glove',
      version='1.0.18',
      description='AWS를 쉽게 사용할 수 있게 도와줍니다.',
      long_description="Please refer to the https://github.com/da-huin/aws_glove",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/aws_glove',
      download_url= 'https://github.com/da-huin/simple_utils/archive/master.zip',
      author='JunYeong Park',
      author_email='dahuin000@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['boto3', 'pyfolder', 'pyzip', 'template_manager'],
      classifiers=[
          'Programming Language :: Python :: 3',
    ]
)
