FROM python:3.7.9-buster

LABEL description="Temp monitor & fan controller"

WORKDIR /icebox

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./__main__.py .

CMD [ "python3", "-u", "__main__.py" ]