<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./static/icon.png" alt="Project logo" ></a>
 <br>

</p>

<h3 align="center">AWS Glove</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/da-huin/aws_glove.svg)](https://github.com/da-huin/aws_glove/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/da-huin/aws_glove.svg)](https://github.com/da-huin/aws_glove/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> AWS를 사용할 때 항상 추가로 코드를 작성해주어야 하는 부분들을 쉽게 사용할 수 있게 해주는 패키지입니다.
    <br> 
</p>

## 📝 Table of Contents

- [Usage-Basic](#usage-basic)
- [Usage-S3](#usage-s3)
- [Usage-Athena](#usage-athena)
- [Usage-Scheduler](#usage-scheduler)
- [Usage-Lambda](#usage-lambda)
- [Usage-Glue](#usage-glue)
- [Acknowledgments](#acknowledgement)

# 🦊 Usage


## 🍀 Basic <a name = "usage-basic"></a>


### 🌱 *(method)* `client`

AWS를 사용할 때 항상 추가로 코드를 작성해주어야 하는 부분들을 쉽게 사용할 수 있게 해주는 패키지입니다.

각 서비스 핸들러를 가져옵니다.

**Example**

```python
import aws_glove
athena = aws_glove.client(
    'athena', 
    output_bucket_name='your_output_bucket_name', 
    output_prefix='your_output_prefix', 
    region_name='ap-northeast-1')
```

**Syntax**

```python
{
    'glove_service_name': 'string',
    'argv': 'arguments'
}
```

**Parameters**
* **[REQUIRED] glove_service_name** (*string*) --

    사용할 서비스 이름입니다.
    
* **argv** (*arguments*) --

    각 서비스에서 사용되는 매개변수들입니다.



---

## 🍀 S3 <a name = "usage-s3"></a>



### 🌱 *(class)* `EasyS3`

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

### 🌱 *(method)* `EasyS3 - save`

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

### 🌱 *(method)* `EasyS3 - load`

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

### 🌱 *(method)* `EasyS3 - save_cache`

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

### 🌱 *(method)* `EasyS3 - load_cache`

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

### 🌱 *(method)* `EasyS3 - list_by`

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

### 🌱 *(method)* `EasyS3 - list_dirs`

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

### 🌱 *(method)* `EasyS3 - list_objects`

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




## 🍀 Athena <a name = "usage-athena"></a>


### 🌱 *(class)* `AWSAthena`

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

### 🌱 *(method)* `AWSAthena - query`

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



---

## 🍀 Scheduler <a name = "usage-scheduler"></a>

### 🚀 템플릿 생성하는 방법

1. 템플릿 폴더를 생성합니다.

2. `yaml` 파일을 생성합니다.
    ```
    templates/
    - hello.yaml
    ```

3. `yaml` 파일을 에디터로 엽니다.

4. 아래와 같이 템플릿을 작성할 수 있습니다.

    1. 기본 사용법

        ```yaml
        kind: cloudwatch
        name: cloudwatch-helloworld
        spec:
            Schedule: cron(0 4 * * ? *)
            FunctionName: HelloWorld
        ---
        kind: glue
        name: glue-helloworld
        spec:
            S3TargetPath: s3://YOUR_BUCKET_NAME/helloworld
            Schedule: cron(0 4 * * ? *)
            name: HelloWorld
        ```

    2. 추가 사용법

        ```yaml
        kind: cloudwatch
        name: cloudwatch-helloworld
        spec:
            Schedule: cron(0 4 * * ? *)
            name: HelloWorld
            # if omit FunctionName, default value is used be [name] value.
            FunctionName: HelloWorld
            # The value you pass to the lambda. Can be omitted.
            Input:
                - hello
                - world
            # you can use EventPattern. Can be omitted.
            EventPattern:
                source:
                    - aws.glue
                detail-type:
                - Detail Type
                detail:
                    state:
                    - Succeeded
                    crawlerName:
                    - YourCrawelrName
        ---
        kind: glue
        name: glue-helloworld
        spec:
            S3TargetPath: s3://YOUR_BUCKET_NAME/helloworld
            # aws Schedule
            Schedule: cron(0 4 * * ? *)
            name: HelloWorld
            # if omit DatabaseNamm, default value is used be [name] value.
            DatabaseName: HelloWorld
        ```
5. 스케줄 포맷은 다음 링크를 참조하세요.

    https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html



### 🌱 *(class)* `SchedulerSchema`

Scheduler 템플릿 규칙입니다.

**Glue Crawler Template Schema**

* **[REQUIRED] kind** (*string*) --
    
    cloudwatch | glue
    
* **[REQUIRED] name** (*string*) --

    스케줄 이름입니다.

* **[REQUIRED] Schedule** (*string*) --

    Cloudwatchevents expressions

* **[REQUIRED] S3TargetPath** (*string*) --

    Glue Crawler가 읽을 S3 경로 입니다.

* **Description** (*string*) --

    스케줄 설명입니다.

**Glue CloudWatch Schema**

* **[REQUIRED] kind** (*string*) --
    
    cloudwatch | glue
    
* **[REQUIRED] name** (*string*) --

    스케줄 이름입니다.

    FunctionName을 입력하지 않으면 자동으로 FunctionName으로도 사용됩니다.

* **Description** (*string*) --

    스케줄 설명입니다.

* **Schedule** (*string*) --

    Cloudwatchevents expressions

* **Input** (*string*) --

* **EventPattern** (*string*) --

### 🌱 *(class)* `Scheduler`

AWS CloudWatch Event와 AWS Glue Crawler를 쉽게 사용할 수 있게 만들어줍니다.

**Example**

```python
import aws_glove
scheduler = aws_glove.client(
    'scheduler',
    template_dir='scheduler/template',
    legacy_template_dir='/tmp/aws_glove/scheduler/template/legacy')
```

**Syntax**

```python
{
    'template_dir': 'string',
    'legacy_template_dir': 'string',
    'aws_access_key_id': 'string',
    'aws_secret_access_key': 'string',
    'region_name': 'string'
}
```

**Parameters**
* **[REQUIRED] template_dir** (*string*) --

    템플릿 파일들이 저장되어있는 폴더 경로입니다. 순회하며 템플릿 파일들을 찾습니다.
    
* **[REQUIRED] legacy_template_dir** (*string*) --

    템플릿 파일을 읽고 배포를 할 때 배포된 후 마지막 상태를 저장하는 폴더 경로입니다. 

    이 경로에 있는 파일을 보고 예전에 배포했던 것과 같다면 중복해서 배포하지 않습니다.

* **aws_access_key_id** (string) --

    *Default: None*
    
    AWS ACCESS KEY ID

* **aws_secret_access_key**(string) --

    *Default: None*

    AWS SECRET ACCESS KEY

* **region_name** (string) --

    *Default: None*

    AWS REGION NAME

### 🌱 *(method)* `Scheduler - deploy`

템플릿 폴더에서 템플릿을 읽고 AWS에 배포합니다.

**Examples**

```python
scheduler.deploy()
```

**Syntax**

```python
{
    'no_cache': 'bool'
}
```

**Parameters**

* **no_cache** (*string*) --
    *Default: False*

    마지막으로 배포된 템플릿과 비교하지 않고 전부 배포합니다.

* **[DEPRECATED] delete_unmanaged** (*bool*) --
    *Default: False*

    이 값을 True로 설정하면이 패키지에서 관리되지 않는 스케줄러가 자동으로 삭제됩니다. 위험하기 때문에 삭제되었습니다.



---

## 🍀 Lambda

Lambda 코드를 작성 할 때 Lambda Console 에서 작성하면 환경도 좋지 않고, 버전 관리가 되지 않는 등 여러가지 문제가 있습니다. 

그래서 AWS SAM 을 사용하는데 이 툴은 template 과 package 를 만들어야 하는 등 여러가지 복잡한 것들이 많습니다.

이 패키지는 AWS SAM 을 내부에 두고, Lambda 와 Lambda Layer 를 쉽게 배포하고 테스트 할 수 있게 도와줍니다.

### 🏁 Getting Started

### Prerequisites 

1. AWS CLI 와 SAM 을 설치합니다. Lambda 등 AWS 를 사용하는 작업에는 이 기능이 필요합니다.

    * https://aws.amazon.com/ko/cli/
    * https://aws.amazon.com/ko/serverless/sam/
    * 설치 후 아래의 명령어를 이용해 인증을 설정합니다.
    ```bash
    aws configure
    ```

### 🚀 Tutorial

#### 1. 람다 함수들을 저장 할 폴더 만들기

    람다 함수들을 저장 할 폴더를 원하는 곳에 만들어주세요.

#### 2. 핸들러 만들기

아래의 코드에 주석을 보고 값을 넣고 실행해주세요.

```python
import easy_lambda

# 람다 함수를 저장할 버킷명입니다.
bucket_name = "YOUR BUCKET NAME"
region_name = "YOUR AWS REGION"

# ~/.aws/config. 에 인증파일이 있다면 None 값으로 두면 됩니다.
# S3, Lambda, IAM (Role Related Policies) 권한이 필요합니다.
aws_access_key_id = "YOUR AWS ACCESS KEY ID"
aws_secret_access_key = "YOUR AWS SECRET ACCESS KEY"

# 람다 함수들을 저장 할 디렉토리입니다.
# 저장하고 싶은 곳에 디렉토리를 만들고 그 경로로 값을 바꿔주세요.
services_dir = "WHERE TO STORE LAMBDA FUNCTIONS"

# (람다 레이어가 아닙니다!) 람다 함수들에 공통적으로 배포 할 코드의 경로입니다.
# 테스트, 배포 할 때마다 이 경로에 있는 폴더가 람다 함수 폴더에 복사됩니다.
# 사용하지 않으려면 `빈 스트링` 으로 설정하세요.
app_layers_dir = "APP LAYERS DIRECTORY"
print(handler)

# SLACK WEBHOOK API URL 입니다. 
# Exception 이 발생하면 슬랙으로 오류 메시지를 보냅니다.
# 사용하지 않으려면 `빈 스트링` 으로 설정하세요.
slack_url = "YOUR SLACK API URL"

# 람다 함수에 넣을 환경변수입니다. 
environ = {"fruit": "apple"}

handler = easy_lambda.AWSLambda(bucket_name, services_dir, app_layers_dir, environ=environ,
                                slack_url=slack_url,
                                aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
```

실행결과:
```
<easy_lambda.AWSLambda object at 0x00DCE7F0>
```

#### 2. 람다 함수 만들기

1. 아래의 코드를 실행하여 람다 함수를 만들어주세요.

    ```python
    >>> handler.create("TestLambda")
    ```

    실행결과: 
    ```python
    Creating TestLambda service ...
    Deploying App layer ...
    App layer deployed.
    TestLambda created.
    ```

1. `아까_만든_람다함수_폴더_경로/`TestLambda 로 들어가서 잘 만들어졌는지 확인합니다.

#### 3. 람다 함수 작업하기

1. `아까_만든_람다함수_폴더_경로/`TestLambda/app.py 를 편집기로 엽니다.

1. `def work(args):` 에 아래의 코드 또는 원하는 코드를 입력합니다.

    ```python
    def work(args):
        result = {}
        print("hello", os.environ["fruit"])
        return result
    ```

#### 4. 람다 함수 테스트하기

* (참고) `아까_만든_람다함수_폴더_경로/`TestLambda/test.py 가 실행됩니다.

```python
>>> handler.test("TestLambda")
```

실행결과:
```python
Deploying App layer ...
App layer deployed.
=== TestLambda Test Started ===


hello apple

Test Result:
{'body': {}, 'statusCode': 200}


=== TestLambda Test Completed ===
Running Time:  0.2759997844696045
```

#### 5. 람다 레이어 배포하기

1. 람다 레이어는 패키지들을 람다 함수에서 사용 할 수 있게 도와줍니다.

1. 아래의 코드로 requests 패키지가 있는 common 이라는 이름의 람다 레이어를 배포합니다.

    ```python
    >>> handler.deploy_layer("common", ["requests"])
    ```

    실행결과:
    ```bash
    Deploying lambda layer ...
    Collecting requests
    Using cached requests-2.24.0-py2.py3-none-any.whl (61 kB)
    Collecting chardet<4,>=3.0.2
    Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
    Collecting certifi>=2017.4.17
    Using cached certifi-2020.6.20-py2.py3-none-any.whl (156 kB)
    Collecting idna<3,>=2.5
    Using cached idna-2.10-py2.py3-none-any.whl (58 kB)
    Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
    Using cached urllib3-1.25.10-py2.py3-none-any.whl (127 kB)
    Installing collected packages: chardet, certifi, idna, urllib3, requests
    Successfully installed certifi-2020.6.20 chardet-3.0.4 idna-2.10 requests-2.24.0 urllib3-1.25.10
    ```

#### 6. 람다 함수 배포하기

```python
>>> handler.deploy("TestLambda", "common")
```

실행결과:
```bash
Deploying App layer ...
App layer deployed.
Starting Build inside a container
Building function 'TestLambda'

...

CREATE_COMPLETE          AWS::Lambda::Function    TestLambda               -
CREATE_COMPLETE          AWS::CloudFormation::S   E-TestLambda             -
                         tack
-------------------------------------------------------------------------------------------------

Successfully created/updated stack - E-TestLambda in ap-northeast-2

52.96790814399719
```

#### 7. 배포된 람다 함수 확인하기

* 람다 콘솔에서 배포가 잘 되었는지 확인합니다.



### 🌱 *(class)* `AWSLambda`

AWS Lambda와 Lambda Layer를 쉽게 배포하고 테스트 할 수 있게 도와줍니다.

**Example**

```python
import aws_glove
handler = aws_glove.client('lambda',
    bucket_name='YOUR_BUCKET_NAME',
    services_dir='SERVICE_NAME'
)
```

**Parameters**

* **[REQUIRED]bucket_name** (*string*) --

    람다 함수들을 저장될 버킷 이름입니다.

* **[REQUIRED]services_dir** (*string*) --

    람다 함수들을 저장 할 디렉토리 경로입니다.

* **app_layers_path** (*string*) --

    *Default: 'lambda'*

    람다 레이어와 다릅니다.

    만약 이 모듈로 배포하는 람다가 같은 함수들을 사용해야한다면 이 경로를 사용할 수 있습니다.
    
    이 매개변수에 입력된 경로에 있는 폴더를 람다 함수의 layers 경로로 복사해줍니다.

* **temp_path** (*string*) --
    
    *Default: '/tmp/aws_glove/lambda'*
    
    람다 레이어와 SAM에서 사용되는 임시 파일 경로입니다.

* **s3_prefix** (*string*) --

    *Default: ''*
    
    람다 관련 파일이 저장될 S3 위치입니다.

* **environ** (*dict*) --

    *Default: {}*

    람다 함수에 배포할 환경변수 입니다.

* **slack_url** (*string*) --

    *Default: ''*

    오류가 발생했을 때 슬랙으로 보낼 URL 입니다.

* **aws_access_key_id** (string) --

    *Default: None*
    
    AWS ACCESS KEY ID

* **aws_secret_access_key**(string) --

    *Default: None*

    AWS SECRET ACCESS KEY

* **region_name** (string) --

    *Default: None*

    AWS REGION NAME    

* **stack_prefix** (string) --

    *Default: ''*

    AWS CloudFormation Stack의 Prefix입니다.

### 🌱 *(method)* `AWSLambda - deploy`

람다 함수를 AWS Lambda에 배포합니다.

**Example**

```
handler.deploy('ExampleLambda', 'example_layer')
```

* **[REQUIRED]service_name** (*string*) --

    배포 할 람다 함수의 이름입니다.

* **[REQUIRED]layer_name** (*string*) --

    람다 함수에 적용 할 람다 레이어의 이름입니다.

### 🌱 *(method)* `AWSLambda - create`

람다 함수를 로컬에 생성합니다.

**Example**

```
handler.create('ExampleLambda')
```

**Parameters**

* **[REQUIRED]service_name** (*string*) --

    람다 함수의 이름입니다.

* **service_name** (*string*) --

    *Default: ''*

    람다 함수의 기본 경로입니다. 아래와 같이 적용됩니다.

    ```
    services_dir/base_dir/service_name
    ```

### 🌱 *(method)* `AWSLambda - test`

람다를 로컬에서 테스트합니다.

**Example**

```
handler.test('ExampleLambda')
```

**Parameters**

* **[REQUIRED]service_name** (*string*) --

    람다 함수의 이름입니다.

* **pytest** (*bool*) --

    *Default: False*

    pytest 로 테스트 할 것인지 여부입니다.

### 🌱 *(method)* `AWSLambda - deploy_layer`

requirements에 있는 리스트로 람다 레이어를 배포합니다.

Lambda와 같은 환경인 EC2에서 사용하는 것이 정확합니다.

**Example**

```
handler.deploy_layer('example_layer', ['requests', 'numpy'])
```

* **[REQUIRED]layer_name** (*string*) --

    배포 할 람다 레이어의 이름입니다.

* **[REQUIRED]requirements** (*list*) --

    레이어에 사용 할 패키지 이름들입니다.




---

## 🍀 Glue <a name = "usage-glue"></a>


### 🌱 *(class)* `AWSGlue`

Glue Job을 쉽게 배포하고 사용할 수 있게 해줍니다.

**Example**

```python
import aws_glove
glue = aws_glove.client('glue', bucket_name='YOUR_BUCKET_NAME')
```

**Syntax**

```python
{
    'bucket_name': 'string',
    'jobs_base_dir': 'string', 
    'aws_access_key_id': 'string', 
    'aws_secret_access_key': 'string',
    'region_name': 'string'
}
```

**Parameters**
* **[REQUIRED] bucket_name** (*string*) --

    Glue 작업이 저장될 버킷 이름입니다.
    
* **jobs_base_dir** (*string*) --

    *Default: ''*

    버킷 안에 Glue 작업이 저장될 위치 Prefix입니다.

* **aws_access_key_id** (string) --

    *Default: None*
    
    AWS ACCESS KEY ID

* **aws_secret_access_key**(string) --

    *Default: None*

    AWS SECRET ACCESS KEY

* **region_name** (string) --

    *Default: None*

    AWS REGION NAME

### 🌱 *(method)* `AWSGlue - deploy`

Glue Job으로 배포할 수 있습니다.

**Example**

```python
glue.deploy('sample_job')
```

**Parameters**

* **[REQUIRED]job_name** (*string*) --

    배포할 glue job 이름입니다.

* **max_capacity** (*int*) --

    *Default: 3*

    Glue Workers의 Max Capactiy입니다.
    
* **timeout** (*int*) --

    *Default: 7200*
    
    Glue Job의 제한 시간입니다.

* **default_arguments** (*dict*) --

    *Default: {}*

    Glue Job의 기본 매개변수입니다. 자세한 내용은 아래를 참조하세요.

    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html

### 🌱 *(method)* `AWSGlue - run_crawler`

Glue Crawler를 실행합니다.

**Parameters**

* **[REQUIRED]crawler_name** (*string*) --

    크롤러 이름입니다.



---

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Title icon made by [Freepik](https://www.flaticon.com/kr/authors/freepik).

- If you have a problem. please make [issue](https://github.com/da-huin/aws-glove/issues).

- Please help develop this project 😀

- Thanks for reading 😄