import time
import aws_glove
import pandas as pd

bucket_name = 'kmong-data-lake'

def test_save_and_load():
    handler = aws_glove.client('s3', bucket_name=bucket_name, service_name='', region_name='ap-northeast-1')
    example_path = '97.trash/aws_glove/s3/example/example.parquet.gz'
    df = pd.DataFrame([{'hello': 'world', 'size': 1}, {'hello': 'banana', 'size': 2}])

    handler.save(example_path, df, options={
        'compress_type': 'gzip'
    })

    assert handler.load(example_path).iloc[1]['hello'] == df.iloc[1]['hello']

def test_cache():
    handler = aws_glove.client('s3', bucket_name=bucket_name, service_name='97.trash', region_name='ap-northeast-1')
    example_path = 'aws_glove/s3/cache_example/example.json'
    handler.save_cache(example_path, {'hello': 'world'}, 3)

    data = handler.load_cache(example_path)
    assert data == {'hello': 'world'}

    time.sleep(4)

    assert handler.load_cache(example_path) == None

def test_list():
    handler = aws_glove.client('s3', bucket_name=bucket_name, service_name='', region_name='ap-northeast-1')
    example_path = '97.trash/aws_glove/s3/list'
    keys = [p['Key'] for p in list(handler.list_by('Contents', Prefix=example_path))]
    assert keys[-1].split('/')[-1] == 'example.parquet'

    prefixes = [p['Prefix'] for p in handler.list_by('CommonPrefixes', Prefix=example_path + '/', Delimiter='/')]
    assert prefixes[0].split('/')[-2] == 'cache_example'
    assert prefixes[1].split('/')[-2] == 'example' 

