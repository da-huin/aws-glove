import aws_glove

scheduler = aws_glove.client('scheduler', 
template_dir='assets/scheduler/template',
legacy_template_dir='/tmp/scheduler/template/legacy')

# def test_deploy():
#     print(scheduler.deploy())

