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
    return EasyS3(**argv)


class EasyS3():
    """
    이 모듈은 S3를 쉽게 사용할 수 있도록 도와줍니다.

    Parameters

    * **[REQUIRED] bucket_name** (*string*) --

        사용할 버킷 이름입니다.

    * **service_name** (*string*) --

        서비스 이름은 버킷 내에서 분류 역할을 합니다. 이 상황에서 account과 orders 및 items는 서비스 이름입니다.

        1. accounts/Your File Path
        2. orders/Your File Path
        3. items/Your File Path        

        만약 서비스 이름을 입력하지 않으면 경로는 아래와 같습니다.

        1. Your File Path

    * **region_name** (*string*) --

        AWS Region Name

    * **aws_access_key_id** (*string*) --

        AWS ACCESS KEY ID

    * **aws_secret_access_key** (*string*) --

        AWS SECRET ACCESS KEY
    """

    def __init__(self, bucket_name: str, service_name: str='', tmp_path='/tmp/aws_glove/s3', region_name: str=None, aws_access_key_id: str=None, aws_secret_access_key: str=None):

        self.bucket_name = bucket_name
        self.service_name = service_name
        self.region_name = region_name

        self._s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self._tmp_path = tmp_path
        if not os.path.isdir(self._tmp_path):
            os.makedirs(self._tmp_path, exist_ok=True)

    @property
    def client(self):
        return self._s3_client


    def save(self, path: str, value, options: dict={}):
        """
        이 기능을 사용하여 데이터를 S3에 저장합니다.
        
        저장 경로는 다음과 같습니다. %Y-%m-%d를 사용하지 않을 수 있습니다.

        `Your Service Name/%Y-%m-%d/Your File Path`

        **Examples**
        
        ```python
        data = {"name": "apple", "price": "120"}
        options = {
                "public": True,
                "ymd": False,
                "compress_type": "gzip"
            }
        url = es.save("food/apple.json", data,
            options=options)

        print(url)
        ```
        
        **Parameters**
        
        * **[REQUIRED] path** (*string*) --
            
            저장시킬 파일의 S3 경로입니다.

            ```
            foo/bar/hello.json
            ```

        * **[REQUIRED] value** (*dict | list | str | bytes | int | float | ...*) --

            여러가지 형식으로 입력할 수 있습니다. 저장할 파일의 내용 입니다.

            ```python
            {"hello": "world", "yellow", "banana"}
            ```

        * **options** (*dict*) --

            *Default: {}*

            옵션을 지정할 수 있습니다.
            
            **Parameters**
            
            * **public** (*bool*) --

                *Default: False*
                
                만약 이 값이 True라면 모든 사람이 볼 수 있습니다.

            * **ymd** (*bool*) --

                *Default: False*

                만약 이 값이 True라면 %Y-%m-%d형식으로 날짜가 입력됩니다.

                ```
                Your Service Name/2020-08-24/Your File Path
                ```

            * **compress_type** (*string*) --

                *Default: ''*

                gzip

                파일을 압축할 수 있습니다. 현재는 gzip만 사용할 수 있습니다.
            
            ```python
            {
                "public": True,
                "ymd": True,
                "compress_type": "gzip"
            }
            ```

        **Returns**

        * **저장된 파일의 URL** (*string*)

            ```
            https://test-bucket-725.s3.ap-northeast-2.amazonaws.com/items/food/apple.json
            ```

        """

        public = options.get("public", False)
        ymd = bool(options.get("ymd", False))
        random = options.get("random", False)
        compress_type = options.get("compress_type", None)
        full_path = self._get_full_path(path, ymd)

        return self._put_file_with_transform(full_path, value, public, random, compress_type=compress_type)

    def load(self, path: str):
        """
        
        S3에 저장된 파일을 불러옵니다.
        
        파일 경로는 아래와 같습니다.
        
        `Your Service Name/Your File Path`

        **Examples**

        ```python
        >>> data = es.load("food/apple.json")
        >>> print(data)
        {'name': 'apple', 'price': '120'}
        ```

        **Parameters**

            * **[REQUIRED] path** (*string*) --

            불러올 파일의 경로입니다.

            ```
            foo/bar/hello.json
            ```

        **Returns**

        * **loaded data**(*dict | list | str*)
        
            S3에서 가져온 값이 반환됩니다.

        """

        full_path = self._get_full_path(path, False)

        return self._load_file(full_path)

    def save_cache(self, path: str, value, cache_time: int):
        """

        이 기능을 사용하여 캐시를 사용하는 데이터를 저장하십시오.

        처리 비용이 S3에 저장 및 로드하는 비용보다 클 때 사용하세요.

        저장 캐시 경로는 다음과 같습니다.

        ```
        Your Service Name/Your File Path
        ```

        **Parameters**

            * **[REQUIRED] path** (*string*) --

            저장할 파일의 경로입니다.
            
            ```
            foo/bar/hello.json
            ```

            * **[REQUIRED] value** (*dict | list | str | bytes | int | float | ...*) --

            저장할 파일의 값 입니다.

            ```python
            {"hello": "world", "yellow", "banana"}
            ```

            * **[REQUIRED] cache_time** (*int*) --
            
            캐시로 사용할 시간 입니다.

        **Returns**

        * **저장된 파일의 URL** (*string*)

            ```
            https://test-bucket-725.s3.ap-northeast-2.amazonaws.com/items/food/apple.json
            ```

            **Example**        

            ```python
            {
                "value": {
                    "name": "apple",
                    "price": "120"
                },
                "cache_time": 10,
                "put_time": 1596727712.0505128
            }
            ```

        """        
        full_path = self._get_cache_full_path(path)
        data = self._make_cache_file(value, float(cache_time))

        return self._put_file_with_transform(full_path, data, False, False)

    def load_cache(self, path: str):
        """
        이 함수를 사용하여 S3에서 캐시 데이터를 로드합니다.

        처리 비용이 S3에 저장 및로드하는 비용보다 클 때 사용하세요.

        로드 된 경로는 다음과 같습니다.

        `Your Service Name/Your File Path`

        **Examples**

        ```python

        import time
        import random

        while True:
            print("=== Press any key to get started. ===")
            input()
            path = "food/apple.json"
            data = es.load_cache(path)

            if data == None:
                working_time = random.randint(0, 4)

                print(f"working for {working_time} seconds ...")

                time.sleep(working_time)

                data = {"name": "apple", "price": "120"}
                es.save_cache(path, data, cache_time=5)

                print("working complete!")
            else:
                print("cached!")

            print(data)
        ```

        ```bash
        === Press any key to get started. ===

        working for 2 seconds ...
        working complete!
        {'name': 'apple', 'price': '120'}

        === Press any key to get started. ===

        cached!
        {'name': 'apple', 'price': '120'}

        === Press any key to get started. ===

        cached!
        {'name': 'apple', 'price': '120'}

        === Press any key to get started. ===

        working for 1 seconds ...
        working complete!
        {'name': 'apple', 'price': '120'}

        ```
      
        **Parameters**

        * **[REQUIRED] path** (*string*) --

            불러올 파일의 경로입니다.

            ```
            foo/bar/hello.json
            ```

        **Returns**

        * **loaded data** (*dict | list | str | None*)

            불러온 데이터입니다.

        """
        full_path = self._get_cache_full_path(path)

        try:
            data = self._load_file(full_path)
        except:
            return None

        if self._is_expired(data):
            return None

        return data["value"]

    def list_by(self, key, **base_kwargs):
        """

        이 기능을 사용하여 S3 버킷 안의 리스트를 가져올 수 있습니다.


        **Example**

        ```
        handler.list_by('CommonPrefixes', Prefix='foo/bar/', Delimiter='/')
        ```
        
        **Parameters**

            * **[REQUIRED] key** (*string*) --

            list_objects_v2의 결과값인 response에서 가져올 key 값 입니다.

            예: CommonPrefixes, Contents

            * **[REQUIRED] base_kwargs** (*argv*) --

            list_objects_v2에 들어갈 추가 매개변수입니다.

            예: Prefix, Delimiter

        **Returns**

        * **boto3 list_objects_v2의 결과값** (*list*)

        """
        continuation_token = None
        base_kwargs["Bucket"] = self.bucket_name
        while True:
            list_kwargs = dict(MaxKeys=1000, **base_kwargs)
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token
            response = self._s3_client.list_objects_v2(**list_kwargs)
            yield from response.get(key, [])
            if not response.get('IsTruncated'):
                break

            continuation_token = response.get('NextContinuationToken')

    def list_dirs(self, **base_kwargs):
        """
        이 기능을 사용하여 S3 버킷 안의 디렉토리 리스트를 가져올 수 있습니다.


        **Example**

        ```
        handler.list_dirs(Prefix='foo/bar/', Delimiter='/')
        ```
        
        **Parameters**

            * **[REQUIRED] base_kwargs** (*argv*) --

            list_objects_v2에 들어갈 추가 매개변수입니다.

            예: Prefix, Delimiter

        **Returns**

        * **boto3 list_objects_v2의 결과값** (*list*)

        """
        return [p['Prefix'] for p in self.list_by('CommonPrefixes', **base_kwargs)]
            
    def list_objects(self, **base_kwargs):
        """
        이 기능을 사용하여 S3 버킷 안의 디렉토리 오브젝트 리스트를 가져올 수 있습니다.

        **Example**

        ```
        handler.list_objects(Prefix='foo/bar')
        ```
        
        **Parameters**

            * **[REQUIRED] base_kwargs** (*argv*) --

            list_objects_v2에 들어갈 추가 매개변수입니다.

            예: Prefix, Delimiter

        **Returns**

        * **boto3 list_objects_v2의 결과값** (*list*)

        """        
        return self.list_by('Contents', **base_kwargs)
        
    def _get_random_string(self, length: int=10):
        random_box = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        random_box_length = len(random_box)
        result = ""
        for _ in range(length):
            result += random_box[int(random.random()*random_box_length)]

        return result
        
    def _make_cache_file(self, value, cache_time: int):
        return {
            "value": value,
            "cache_time": cache_time,
            "put_time": time.time()
        }

    def _is_expired(self, data):
        cache_time = data["cache_time"]
        put_time = data["put_time"]
        if cache_time == -1:
            return False

        if (time.time() - put_time) > cache_time:
            return True

        return False


    def _put_file(self, full_path, data, public, random, binary_content_type=False, compress_type=None):

        if random:
            _, ext = os.path.splitext(full_path)
            dirname = os.path.dirname(full_path)
            filename = self._get_random_string() + ext
            full_path = dirname + "/" + filename

        if full_path == "":
            raise ValueError("full path is empty.")

        if public:
            ACL = "public-read"
        else:
            ACL = "private"
        binary = self._to_binary(data)
        content_type = ""
        if binary_content_type == False:
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type == None:
                content_type = "binary/octet-stream"

        if compress_type:
            if compress_type == "gzip":
                binary = gzip.compress(binary)
            else:
                raise ValueError((f'invalid compress type {compress_type}'))

        self._s3_client.put_object(Bucket=self.bucket_name,
                            Body=binary, Key=full_path, ACL=ACL, ContentType=content_type)

        object_uri = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{full_path}"

        return object_uri


    def _load_file(self, full_path):
        print(full_path)
        """
        If the extention is .parquet, you need the Fastparquet package.
        """
        readed = self._s3_client.get_object(
            Bucket=self.bucket_name, Key=full_path)["Body"].read()
    
        _, ext = os.path.splitext(full_path)

        if ext == ".gz":
            readed = gzip.decompress(readed)

            _, ext = os.path.splitext(full_path[:-len('.gz')])

        if ext == ".parquet":
            import pandas as pd
            from fastparquet import ParquetFile
            
            filename = f"{self._tmp_path}/{uuid.uuid4()}.parquet"
            with open(filename, "wb") as fp:
                fp.write(readed)
            readed = ParquetFile(filename).to_pandas()

            os.unlink(filename)
        else:
            try:
                encoded = readed.decode("utf-8")
                try:
                    readed = json.loads(encoded)
                except:
                    readed = encoded
            except:
                pass

        return readed

    def _to_binary(self, value):
        binary = b""
        if isinstance(value, bytes):
            binary = value
        elif isinstance(value, str):
            binary = value.encode("utf-8")
        else:
            binary = json.dumps(value, ensure_ascii=False,
                                default=str).encode("utf-8")

        return binary


    def _make_valid_path(self, path):
        if not isinstance(path, str):
            raise ValueError(f"path is not str. path type is {type(path)}")
        if len(path) == 0:
            raise ValueError("path's length is zero.")

        path = path.replace("\\", "/")
        path = path.replace("//", "/")

        if path == "/":
            raise ValueError("invalid path '/'")

        if path[0] == "/":
            path = path[1:]

        return path

    def _get_full_path(self, path, ymd=False, kind="file"):

        ymd_str = ""
        if ymd:
            ymd_str = "%s/" % datetime.datetime.now().strftime("%Y-%m-%d")

        if kind == "file":
            if len(path) == 0:
                raise ValueError("path's length is zero.")

            if path == "/":
                raise ValueError("path is slash.")

            if path[0] == "/":
                path = path[1:]

        elif kind == "dir":
            pass
        
        service_name_str = self.service_name + '/' if self.service_name else self.service_name
        return self._make_valid_path(f"{service_name_str}/{ymd_str}{path}")

    def _get_cache_full_path(self, path):

        service_name_str = self.service_name + '/' if self.service_name else self.service_name
        return self._make_valid_path(f"{service_name_str}/{path}")

    def _make_parquet(self, data):
        import pandas as pd
        from fastparquet import write
        filename = f"{self._tmp_path}/{uuid.uuid4()}.parquet"

        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data, index=range(len(data)))

        write(filename, df, compression="GZIP")

        with open(filename, "rb") as fp:
            parquet = fp.read()

        os.unlink(filename)

        return parquet

    def _put_file_with_transform(self, full_path, value, public, random, binary_content_type=False, compress_type=None):
        _, ext = os.path.splitext(full_path)

        if ext in ['.gz']:
            _, ext = os.path.splitext(full_path[:-len(ext)])
        
        if ext == ".parquet":
            import pandas as pd
            if isinstance(value, dict):
                value = [value]

            if not isinstance(value, list) and not isinstance(value, pd.DataFrame):
                raise ValueError(f"parquet value's instance must be list. value type is {type(value)}")
            
            value = self._make_parquet(value)

        return self._put_file(full_path, value, public, random, binary_content_type=binary_content_type, compress_type=compress_type)
