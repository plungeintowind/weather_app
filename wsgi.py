from app import create_app
from flask import Flask
import os

app = Flask(__name__)
print(f"模板路径: {os.path.join(app.root_path, 'templates')}")  # 检查路径是否正确

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)