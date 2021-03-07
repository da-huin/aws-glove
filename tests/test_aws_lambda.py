import aws_glove
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

lambda_handler = aws_glove.client('lambda', 
    bucket_name='kmong-data-lake', 
    services_dir=f'{current_dir}/lambda/services',
    app_layers_path=f'{current_dir}/lambda/layers',
    environ = {
        'hello': 'world'
    },
    stack_prefix = 'Example',
    s3_prefix='97.trash/lambda',
    region_name='ap-northeast-1'
)


# def test_lambda_create():
#     print(lambda_handler.create('Example'))

# def test_lambda_test():
#     lambda_handler.test('Example')

# def test_lambda_deploy_layer():
#     print(lambda_handler.deploy_layer('example_layer', ['requests']))

# def test_lambda_deploy():
#     print(lambda_handler.deploy('Example', layer_name='example_layer'))

