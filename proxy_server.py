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

    try:
        # Forward the request to the target server
        response = requests.request(
            method,
            url,
            headers=headers,
            data=data,
            params=request.args,
            cookies=request.cookies,
            allow_redirects=False  # Handle redirects manually
        )

        # Prepare the response headers
        response_headers = [
            (key, value) for key, value in response.headers.items()
            if key.lower() not in ['content-encoding', 'transfer-encoding', 'connection']
        ]

        # Handle redirects
        if response.is_redirect:
            # Forward the redirect response to the client
            return Response(
                response.content,
                response.status_code,
                response_headers
            )

        # Return the response from the target server
        return Response(
            response.content,
            response.status_code,
            response_headers
        )

    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., network errors)
        return Response(
            f"An error occurred: {e}",
            status=500
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
