"""AWS를 사용할 때 항상 추가로 코드를 작성해주어야 하는 부분들을 쉽게 사용할 수 있게 해주는 패키지입니다."""

from importlib import import_module

def client(glove_service_name, **argv):
    """
    각 서비스 핸들러를 가져옵니다.

    **Example**

    ```python
    import aws_glove
    athena = aws_glove.client(
        'athena', 
        output_bucket_name='your_output_bucket_name', 
        output_prefix='your_output_prefix', 
        region_name='ap-northeast-1')
    ```

    **Syntax**
    
    ```python
    {
        'glove_service_name': 'string',
        'argv': 'arguments'
    }
    ```

    **Parameters**
    * **[REQUIRED] glove_service_name** (*string*) --

        사용할 서비스 이름입니다.
        
    * **argv** (*arguments*) --

        각 서비스에서 사용되는 매개변수들입니다.

    """
    
    return import_module(f'.aws_{glove_service_name}', package='aws_glove')._loader(**argv)
