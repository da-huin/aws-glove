import re
import os
import time
import json
import boto3

def _loader(**argv):
    return AWSGlue(**argv)
    
class AWSGlue():
    """
    
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
    """

    def __init__(self, bucket_name, jobs_base_dir: str="", aws_access_key_id: str = None, aws_secret_access_key: str = None, region_name: str = None):
        self._bucket_name = bucket_name
        self._jobs_base_dir = jobs_base_dir
        self._glue_client = boto3.client("glue",
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key,
                                         region_name=region_name)

        self._s3_client = boto3.client("s3",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name)

        self._iam_client = boto3.client("iam",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name)

    def deploy(self, job_name: str, max_capacity: int = 3, timeout: int = 7200, default_arguments: dict={}):
        """
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
        """

        role_name = "easy_glue_role"
        self._create_glue_role(role_name)
        job_dir = self._get_unique_service_path(self._jobs_base_dir, job_name)

        dest_path = f"easy_glue/jobs/{job_name}/index.py"
        index_path = f"{job_dir}/index.py"

        self._s3_client.upload_file(
            index_path, self._bucket_name, dest_path)


        base_default_arguments = {
            '--bucket_name': self._bucket_name,
            '--job-bookmark-option': 'job-bookmark-enable',
            "--enable-continuous-cloudwatch-log": "true",
            "--enable-continuous-log-filter": "true",
            "--TempDir": f"s3://{self._bucket_name}/easy_glue/temp"
        }


        base_default_arguments.update(default_arguments)


        job_args = {
            "Name": job_name,
            "Role": role_name,
            "DefaultArguments": base_default_arguments,
            "GlueVersion": '1.0',
            "MaxRetries": 0,
            "MaxCapacity": max_capacity,
            "Timeout": timeout,
            "Command": {
                'Name': 'glueetl', 'ScriptLocation': f's3://{self._bucket_name}/{dest_path}', 'PythonVersion': '3'}
        }
        try:
            self._glue_client.delete_job(JobName=job_name)
        except:
            pass

        return self._glue_client.create_job(**job_args)

    def run_crawler(self, crawler_name: str):
        """
        Glue Crawler를 실행합니다.

        **Parameters**

        * **[REQUIRED]crawler_name** (*string*) --

            크롤러 이름입니다.

        """

        return self._glue_client.start_crawler(Name=crawler_name)

    def _create_glue_role(self, glue_role_name: str):
        
        try:
            self._iam_client.get_role(RoleName=glue_role_name)
        except:

            self._iam_client.create_role(RoleName=glue_role_name, AssumeRolePolicyDocument=json.dumps(
                {'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow', 'Principal': {'Service': 'glue.amazonaws.com'}, 'Action': 'sts:AssumeRole'}]}))

            self._iam_client.attach_role_policy(
                RoleName=glue_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
            )

        return glue_role_name

    def _get_unique_service_path(self, service_base_path: str, service_name: str):
        service_path = ""
        for dirpath, dirnames, _ in os.walk(service_base_path):
            if service_name in dirnames:
                service_path = os.path.abspath(dirpath + "/" + service_name)
                break

        if service_path == "":
            raise ValueError(
                f"{service_name} could not found in {service_base_path}")

        result = service_path.replace("\\", "/")
        if len(result.split("/")) == 1:
            raise ValueError(f"invalid service {service_name}")

        return result
