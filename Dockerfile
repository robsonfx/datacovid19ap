FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    &&  pip install --upgrade pip && pip install python-magic && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
