
import shutil
import glob
import re
from pprint import pprint
import json
import time
import os
import yaml
import sys
import importlib
import boto3
from pyfolder import PyFolder
from pyzip import PyZip
import platform
import subprocess
import threading

def _loader(**argv):
    return AWSLambda(**argv)

class Utils():    
    def get_set_environ_command(self):

        if self.is_windows():
            set_environ_command = "SET"
        else:
            set_environ_command = "export"        
        return set_environ_command


    def get_os(self):
        return platform.system()


    def is_windows(self):
        return self.get_os() == "Windows"


    def get_unique_service_path(self, service_base_path, service_name):
        service_path = ""
        for dirpath, dirnames, _ in os.walk(service_base_path):
            if service_name in dirnames:
                service_path = os.path.abspath(dirpath + "/" + service_name)
                break

        if service_path == "":
            raise ValueError(f"service Could be found in {service_base_path}/{service_name}")

        result = service_path.replace("\\", "/")
        if len(result.split("/")) == 1:
            raise ValueError(f"Invalid service {service_name}")

        return result


    def rmtree(self, path):
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass


    def check_output(self, command):
        if isinstance(command, list):
            command = "&&".join(command)

        result = ""
        # print("[Command] " + command)

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self._print_output,
                         args=(process.stdout, )).start()

        for b_line in iter(process.stderr.readline, b''):
            try:
                line = b_line.decode("utf-8")
            except:
                try:
                    line = b_line.decode("cp949")
                except:
                    line = str(b_line)

            print(line, end="")
            result += line

        return result

    def _print_output(self, out):
        for b_line in iter(out.readline, b''):

            try:
                line = b_line.decode("cp949")
            except:
                try:
                    line = b_line.decode("utf-8")
                except:
                    line = str(b_line)

            print(line, end="")


    def copy_directory(self, from_path, to_path):
        from_base_dir = os.path.abspath(from_path).replace("\\", "/")
        to_base_dir = os.path.abspath(to_path).replace("\\", "/")
        copyed_file_paths = []
        for dirpath, _, filenames in os.walk(from_base_dir):
            for filename in filenames:
                from_file_path = (dirpath + "/" + filename).replace("\\", "/")
                append_file_path = from_file_path.replace(from_base_dir, "")
                to_file_path = to_base_dir + append_file_path
                while True:
                    try:
                        with open(from_file_path, "rb") as fp:
                            readed = fp.read()

                        to_path_dir = os.path.dirname(to_file_path)
                        if not os.path.isdir(to_path_dir):
                            os.makedirs(to_path_dir)

                        with open(to_file_path, "wb") as fp:
                            fp.write(readed)

                    except:
                        time.sleep(1)
                    else:
                        break
                copyed_file_paths.append(to_file_path)
        
        all_to_file_path = []
        for dirpath, _, filenames in os.walk(to_base_dir):
            for filename in filenames:
                to_file_path = (dirpath + "/" + filename).replace("\\", "/")
                all_to_file_path.append(to_file_path)

        for file_path in list(set(all_to_file_path) - set(copyed_file_paths)):

            while True:
                try:
                    os.unlink(file_path)
                except:
                    time.sleep(1)
                else:
                    break


class AWSLambda():
    """
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

    """
    def __init__(self, bucket_name, services_dir, temp_path="/tmp/aws_glove/lambda", s3_prefix = 'lambda', app_layers_path="", environ={}, 
                    slack_url="", aws_access_key_id=None, aws_secret_access_key=None, region_name=None, stack_prefix="E"):

        self._stack_prefix = stack_prefix
        self._bucket_name = bucket_name
        self._services_dir = os.path.abspath(services_dir)
        self._app_layers_path = app_layers_path
        self._region_name = region_name

        self._lambda_client = boto3.client("lambda",
                                           aws_access_key_id=aws_access_key_id,
                                           aws_secret_access_key=aws_secret_access_key,
                                           region_name=self._region_name)

        self._s3_client = boto3.client("s3",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=self._region_name)


        self._iam_client = boto3.client("iam",
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=self._region_name)
        self._s3_prefix = s3_prefix
        self._utils = Utils()
        self._temp_path = temp_path
        os.makedirs(self._temp_path, exist_ok=True)

        self._environ = environ

        if slack_url:
            self._environ["SLACK_URL"] = slack_url

    def deploy(self, service_name, layer_name):
        """

        람다 함수를 AWS Lambda에 배포합니다.

        **Example**

        ```
        handler.deploy('ExampleLambda', 'example_layer')
        ```

        * **[REQUIRED]service_name** (*string*) --

            배포 할 람다 함수의 이름입니다.

        * **[REQUIRED]layer_name** (*string*) --

            람다 함수에 적용 할 람다 레이어의 이름입니다.

        """

        self._deploy_app_layers(service_name)

        self._compile_template(service_name, layer_name)

        start = time.time()


        commands = ["cd " + self._temp_path, "sam build --use-container",
                    f"sam package --output-template-file packaged.yaml --s3-bucket {self._bucket_name}",
                    f"sam deploy --template-file packaged.yaml --region {self._region_name} --capabilities CAPABILITY_IAM --stack-name {self._stack_prefix}-{service_name} "]

        self._utils.check_output("&&".join(commands))
        print(time.time() - start)

    def create(self, service_name, base_dir=""):
        """
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

        """
        print(f"Creating {service_name} service ...")

        try:
            self._is_valid_service(service_name)
        except:
            pass
        else:
            raise ValueError(f"The {service_name} service is already exists.")

        if base_dir:
            to_path = f"{self._services_dir}/{base_dir}/{service_name}"
        else:
            to_path = f"{self._services_dir}/{service_name}"

        self._utils.copy_directory(
            self._get_assets_dir() + "/create", to_path)

        self._deploy_app_layers(service_name)

        print(f"{service_name} created.")


    def test(self, service_name, pytest=False):
        """
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
        
        """
        self._deploy_app_layers(service_name)

        start = time.time()
        print(f"=== {service_name} Test Started ===\n\n")

        if pytest:
            command = "python3 -m pytest -s test.py"
        else:
            command = "python3 test.py"

        self._utils.check_output([f"cd {self._get_service_path(service_name)}"] +
                                 self._get_export_env_string_list() + [command])

        print(f"\n\n=== {service_name} Test Completed ===")
        print("Running Time: ", time.time() - start)

    def deploy_layer(self, layer_name: str, requirements: list):
        """
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

        """
        print("Deploying lambda layer ...")

        requirements.append("requests")
        lambda_layers_path = self._temp_path + "/lambda_layers"
        self._utils.rmtree(lambda_layers_path + "/space/python")
        os.makedirs(lambda_layers_path + "/space/python", exist_ok=True)

        for package_name in list(set(requirements)):
            self._utils.check_output(
                [f"cd {lambda_layers_path}", f"python3 -m pip install -t ./space/python/ {package_name}"])

        trashnames = ["*.pyc", "*.egg-info", "pyc/**"]
        deleted_dirs = []
        deleted_files = []
        for trash in trashnames:
            paths = glob.glob(lambda_layers_path +
                                "/space/**/" + trash, recursive=True)
            for path in paths:
                if os.path.isdir(path):

                    deleted_dirs.append(self._utils.rmtree(path))
                if os.path.isfile(path):
                    deleted_files.append(os.unlink(path))

        time.sleep(2)

        path_to_compress = f"{lambda_layers_path}/space"
        pyzip = PyZip(PyFolder(path_to_compress, interpret=False))
        pyzip.save(f"{path_to_compress}/../{layer_name}.zip")

        self._deploy_lambda_layer(
            layer_name, lambda_layers_path + f"/{layer_name}.zip")


    def _deploy_app_layers(self, service_name):
        if self._app_layers_path != "":
            print("Deploying App layer ...")
            self._is_valid_service(service_name)

            self._utils.copy_directory(
                self._app_layers_path, self._get_service_path(service_name) + "/layers")

            print("App layer deployed.")

    def _get_service_path(self, service_name):
        return self._utils.get_unique_service_path(self._services_dir, service_name)

    def _compile_template(self, service_name, layer_name="common"):
        service_path = self._get_service_path(service_name)

        result = self._lambda_client.list_layer_versions(LayerName=layer_name)
        common_layer_arn = result["LayerVersions"][0]["LayerVersionArn"]

        service_template_path = service_path + "/template.yaml"
        template_path = f"{self._get_assets_dir()}/others/template.yaml"

        with open(template_path, "r", encoding="utf-8") as fp:
            readed = fp.read()
            readed = readed.replace("{{Description}}", service_name)
            readed = readed.replace("{{FunctionName}}", service_name)
            readed = readed.replace("{{CodeUri}}", service_path)
            readed = readed.replace("{{CommonLayerArn}}", common_layer_arn)

            parsed_readed = yaml.full_load(readed)
            parsed_readed["Resources"][service_name]["Properties"]["Environment"]["Variables"] = self._environ

        if os.path.isfile(service_template_path):
            with open(service_template_path, "r", encoding="utf-8") as fp:
                readed = fp.read()
                readed = readed.replace("{{FunctionName}}", service_name)
                readed = readed.replace("{{BucketName}}", self._bucket_name)
                user_template = yaml.full_load(readed)
                for key in user_template:
                    value = user_template[key]
                    last = parsed_readed
                    splited = key.split(".")
                    for splited_key in splited[:-1]:
                        if splited_key not in last:
                            last[splited_key] = {}

                        last = last[splited_key]

                    last[splited[-1]] = value

        with open(self._temp_path + "/template.yaml", "w", encoding="utf-8") as fp:
            dumped = yaml.dump(parsed_readed)
            for raw_ref_str in re.findall(r"'!Ref.*?'", dumped):
                dumped = dumped.replace(raw_ref_str, raw_ref_str[1:-1])
            fp.write(dumped)

    def _is_valid_service(self, service_name):
        service_path = self._get_service_path(service_name)
        if not os.path.isdir(service_path):
            raise ValueError(f"{service_name} is not exists.")

    def _get_assets_dir(self):
        return os.path.dirname(os.path.abspath(__file__)) + '/lambda'

    def _deploy_lambda_layer(self, LayerName, zip_path):
        s3_key = self._s3_prefix + f'/layers/{LayerName}/{LayerName}.zip'

        self._s3_client.upload_file(zip_path, self._bucket_name, s3_key)
        lambda_layer_published = self._lambda_client.publish_layer_version(LayerName=f'{LayerName}', Description=f'{LayerName}', Content={
            'S3Bucket': self._bucket_name, 'S3Key': s3_key}, CompatibleRuntimes=['python3.6', 'python3.7'], LicenseInfo='')

        return lambda_layer_published

    def _get_export_env_string_list(self):
        result = []

        set_env_command = self._utils.get_set_environ_command()

        for env_name in self._environ:
            env_value = self._environ[env_name]
            result.append(f"{set_env_command} {env_name}={env_value}")

        return result
