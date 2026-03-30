import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    webhook_url = "WEBHOOK_URL"

    # 메시지 추출
    raw_message = event['Records'][0]['Sns']['Message']

    # 타입에 따라 처리
    if isinstance(raw_message, str):
        try:
            parsed_message = json.loads(raw_message)
        except json.JSONDecodeError:
            parsed_message = raw_message # 그냥 문자열일 경우
    elif isinstance(raw_message, dict):
        parsed_message = raw_message
    else:
        raise TypeError(f'Unexpected type for Message: {str(type(raw_message))}')


    # account 필드를 affectedAccount 필드의 값으로 변경
    if 'affectedAccount' in parsed_message.get('detail', {}):
        parsed_message['account'] = parsed_message['detail']['affectedAccount']

    # webhook으로 전달할 payload 생성
    payload = {
        'Message': json.dumps(parsed_message)
    }

    headers = {'Content-Type': 'application/json'}
    response = http.request(
        'POST',
        webhook_url,
        body = json.dumps(payload),
        headers = headers
    )

    print('Status Code: ', response.status)
    print('Response Body: ', response.data.decode('utf-8'))
    print('Headers: ', response.headers)


    return {
        'statusCode': response.status,
        'body': response.data.decode('utf-8')
    }