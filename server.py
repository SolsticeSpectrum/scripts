from flask import Flask, send_file, make_response

app = Flask(__name__)

@app.route('/')
def download_file():
    file_path = 'sample-zip-file.zip'
    response = make_response(send_file(file_path))
    response.headers['Content-Disposition'] = f'attachment; filename={file_path.split("/")[-1]}'
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1698)
