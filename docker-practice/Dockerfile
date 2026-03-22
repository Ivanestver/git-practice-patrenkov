FROM python:3.11-alpine

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
