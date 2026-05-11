FROM python:3.11-slim

WORKDIR /app

# パッケージのインストール
COPY requirements.txt .
# dotenvがrequirements.txtにないため追加でインストール
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

# ソースコードのコピー
COPY . .

# 起動コマンド
CMD ["python", "main.py"]
