import boto3

def _loader(**argv):
    return AWSEC2(**argv)


class AWSEC2():
    def __init__(self, region_name):
        self._ec2_client = boto3.client('ec2', region_name=region_name)

    def replace_inbound_sg(self, group_name, services, sources):
        '''
        **Examples**
        ```python
        group_name= 'sample-sg'
        services = {
            'service a': 7170,
            'service b': 7172
        }

        sources = {
            'source a': '11.111.11.1',
            'source b': '22.222.22.2'
        }

        AWSEC2().replace_inbound_sg(group_name, services, sources)   
        ```     

        **Parameters**

        * **[REQUIRED] group_name** (*string*) --
            
            보안 그룹 이름입니다.

        * **[REQUIRED] services** (*dict*) --

            서비스 이름과 포트 딕셔너리입니다.

        * **[REQUIRED] sources** (*dict*) --

            소스 이름과 아이피 딕셔너리입니다.

        '''
        inpermissions = []
        for service_name, service_port in services.items():
            inranges = []
            for source_name, source_ip in sources.items():
                inranges.append({
                    'CidrIp': f'{source_ip}/32',
                    'Description': f'[{source_name}] {service_name}'
                })
            inpermissions.append({
                'IpProtocol': 'tcp',
                'FromPort': service_port,
                'ToPort': service_port,
                'IpRanges': inranges,
            })

        existing_inpermissions = self._ec2_client.describe_security_groups(GroupNames=[group_name])['SecurityGroups'][0]['IpPermissions']
        if existing_inpermissions:
            self._ec2_client.revoke_security_group_ingress(GroupName=group_name, IpPermissions=existing_inpermissions)
            

        return self._ec2_client.authorize_security_group_ingress(
            GroupName=group_name,
            IpPermissions=inpermissions
        )
