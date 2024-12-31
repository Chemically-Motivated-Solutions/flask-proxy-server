import requests
from flask import Flask, request, Response

app = Flask(__name__)

TARGET_URL = 'https://example.com'  # Replace with the target server's URL

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"{TARGET_URL}/{path}"
    method = request.method
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_data()

    response = requests.request(
        method,
        url,
        headers=headers,
        data=data,
        params=request.args,
        cookies=request.cookies,
        allow_redirects=False
    )

    return Response(
        response.content,
        response.status_code,
        response.headers.items()
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
