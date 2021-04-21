import uuid
import gzip
import time
import random
import os
import json
import datetime
import mimetypes
import boto3

def _loader(**argv):
    return AWSSSM(**argv)

class AWSSSM():
    def __init__(self, region_name):
        """
        SSM과 관련된 기능들을 사용할 수 있는 모듈입니다.

        **Examples**
        
        ```python
        import aws_glove
        ssm_glove = aws_glove.client('ssm')
        ```

        **Parameters**

        * **[REQUIRED] region_name** (*string*) --
            AWS Region Name
        
        """
        self._ssm_client = boto3.client('ssm', region_name)
    
    def get_parameter(self, name):
        """
        Parameter Store에 등록되어 있는 파라미터를 가져옵니다. 암호화되어있다면 풀어서 가져옵니다.
    
        **Examples**
        
        ```python
        import aws_glove
        ssm_glove = aws_glove.client('ssm')
        print(ssm_glove.get_parameter('/foo/bar'))
        ```

        **Syntax**

        ```python
        {
            'name': 'str'
        }
        ```
        
        **Parameters**

        * **[REQUIRED] name** (*string*) --
            Parameter Store에 등록되어있는 키 값 입니다.

        """
        return self._ssm_client.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']