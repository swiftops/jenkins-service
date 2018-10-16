FROM python:3-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8098

CMD [ "python", "services.py" ]
