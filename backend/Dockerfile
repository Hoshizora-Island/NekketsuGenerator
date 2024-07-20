FROM python:3.10

WORKDIR /backend
ENV PYTHONBUFFERED 1

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 3030
CMD python main.py