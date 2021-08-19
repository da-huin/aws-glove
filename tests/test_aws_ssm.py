import aws_glove

ssm = aws_glove.client('ssm', region_name='ap-northeast-2')
def test_get_parameter():
    print(ssm.get_parameter('/google/api_key'))
