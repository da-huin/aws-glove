import aws_glove

athena = aws_glove.client('athena', output_bucket_name='kmong-data-lake', output_prefix='97.trash/athena/query_output', region_name='ap-northeast-1')

# def test_help():
#     help(aws_glove.aws_athena.AWSAthena)

def test_query():
    data = athena.query('SELECT * FROM "history"."kcp_ads_20201201" LIMIT 5')
    assert len(data) == 5
