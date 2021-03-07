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
    return AWSAthena(**argv)

class AWSAthena():
    """
    AWS Athena를 쉽게 사용할 수 있게 만들어줍니다.
    
    **Examples**

    ```python
    import aws_glove
    athena = aws_glove.client('athena', 
        output_bucket_name='your_output_bucket_name', 
        output_prefix='your_output_prefix', 
        region_name='ap-northeast-1')
    ```

    **Syntax**

    ```python
    {
        'output_bucket_name': 'string',
        'output_prefix': 'string',
        'region_name': 'string'
    }
    ```

    **Parameters**

    * **[REQUIRED] output_bucket_name** (*string*)  --

        쿼리 결과를 저장할 버킷 이름입니다.

    * **[REQUIRED] output_prefix** (*string*) --

        쿼리 결과를 저장할 버킷의 Prefix 입니다.

    * **aws_access_key_id** (*string*) --

        *Default: None*

        AWS ACCESS KEY ID

    * **aws_secret_access_key** (*string*) --

        *Default: None*

        AWS SECRET ACCESS KEY

    * **region_name** (*string*) --

        *Default: None*

        AWS REGION NAME
    """

    def __init__(self, output_bucket_name, output_prefix, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):

        self._athena_client= boto3.client('athena',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name)

        self._output_prefix = output_prefix
        self._output_bucket_name = output_bucket_name

    def query(self, query_string, format_type="auto", request_limit=10000):
        
        """
        AWS Athen에 쿼리를 보냅니다.
        쿼리 결과에 대해서 NextToken을 설정할 필요가 없고, 복잡한 형식의 반환값을 json 형식으로 간단한게 변환해줍니다.
        
        **Examples**

        ```python
        data = athena.query('SELECT * FROM "db_name"."table_name" LIMIT 10')
        ```

        **Syntax**

        ```python
        {
            'query': 'string',
            'format_type': 'auto' | 'raw'
        }
        ```

        **Parameters**

        * **[REQUIRED] query_string** (*string*) --

            요청을 보낼 쿼리 스트링입니다.

        * **format_type** (*string*) --

            *Default: auto*

            format_type을 'auto'로 지정할 시 쿼리 스트링이 SELECT로 시작하면 보기 쉽게 변환해서 돌려줍니다.
            'raw'로 지정할 시 athena 쿼리 결과 그대로 돌려줍니다.

        * **request_limit** (*int*) --

            *Default: 10000*

            요청 결과값이 1000줄이 넘을 때 NextToken을 사용하여 얼마나 더 가져올 것인지 정할 수 있습니다.
            예를 들어 request_limit가 7 이라면 (1000 * 7)줄을 불러올 수 있습니다.

        """
        def get_format_type(query_string):
            if query_string.lower().startswith('select'):
                return "select"
            else:
                return "raw"

        def get_varchar_value(row):
            result = []
            for piece in row["Data"]:
                result.append(piece.get('VarCharValue', None))

            return result
            # return [piece["VarCharValue"] for piece in row["Data"]]

        def merge_with_columns(columns, data):
            result = {}
            for index, piece in enumerate(data):
                result[columns[index]] = piece
            return result

        def get_var_char_values(d):
            return [obj.get('VarCharValue', None) for obj in d['Data']]

        def parse(header, rows):
            header = get_var_char_values(header)
            return [dict(zip(header, get_var_char_values(row))) for row in rows]


        if format_type == "auto":
            format_type = get_format_type(query_string)

        result = []

        query_id = self._athena_client.start_query_execution(**{
            "QueryString": query_string,
            "ResultConfiguration": {
                "OutputLocation": f"s3://{self._output_bucket_name}/{self._output_prefix[1:] if self._output_prefix.startswith('/') else self._output_prefix}"
            }
        })["QueryExecutionId"]

        while True:
            status = self._athena_client.get_query_execution(QueryExecutionId=query_id)[
                "QueryExecution"]["Status"]["State"]
            time.sleep(1)
            if status == "CANCELLED":
                raise ValueError(f"[{query_string}] is cancelled.")

            elif status == "FAILED":
                raise ValueError(f"[{query_string}] is failed.")

            elif status == "SUCCEEDED":
                break
            else:
                continue

        next_tokens = []
        header = []
        for index in range(request_limit):
            
            request_data = {
                "QueryExecutionId":query_id
            }

            if len(next_tokens):
                request_data["NextToken"] = next_tokens[-1]

            query_raw_result = self._athena_client.get_query_results(**request_data)

            if format_type == "raw":
                result.append(query_raw_result)
                break

            elif format_type == "select":
                if index == 0:
                    header, *rows = query_raw_result['ResultSet']['Rows']
                else:
                    rows = query_raw_result['ResultSet']['Rows']

                result.extend(parse(header, rows))
                
                if "NextToken" in query_raw_result:
                    new_next_token = query_raw_result["NextToken"]
                    if new_next_token not in next_tokens:
                        next_tokens.append(new_next_token)
                    else:
                        break
                else:
                    break

        return result

