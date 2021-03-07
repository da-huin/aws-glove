<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="./static/icon.png" alt="Project logo" ></a>
 <br>

</p>

<h3 align="center">AWS Glove</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/da-huin/aws_glove.svg)](https://github.com/jaden-git/aws_glove/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/da-huin/aws_glove.svg)](https://github.com/jaden-git/aws_glove/pulls)
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
{{usage['__init__.py']}}

---

## 🍀 S3 <a name = "usage-s3"></a>

{{usage['aws_s3.py']}}


## 🍀 Athena <a name = "usage-athena"></a>
{{usage['aws_athena.py']}}

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

{{usage['aws_scheduler.py']}}

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

{{usage['aws_lambda.py']}}


---

## 🍀 Glue <a name = "usage-glue"></a>
{{usage['aws_glue.py']}}

---

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Title icon made by [Freepik](https://www.flaticon.com/kr/authors/freepik).

- If you have a problem. please make [issue](https://github.com/jaden-git/aws-glove/issues).

- Please help develop this project 😀

- Thanks for reading 😄
