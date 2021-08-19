import boto3


def _loader(**argv):
    return AWSECS(**argv)


class AWSECS():

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):

        self._ecs_client= boto3.client('ecs',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name)


    def get_service_first_task_private_ip(self, cluster, family):
        # ecs_client = boto3.client('ecs', region_name='ap-northeast-1')

        response = self._ecs_client.list_tasks(
            cluster=cluster,
            family=family,
            desiredStatus='RUNNING',
        )

        response = self._ecs_client.describe_tasks(
            cluster=cluster,
            tasks=[
                response['taskArns'][0]
            ]
        )

        private_ip = None
        for v in response['tasks'][0]['attachments'][0]['details']:
            if v['name'] == 'privateIPv4Address':
                private_ip = v['value']

        return private_ip
