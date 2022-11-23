FROM python:3.8

ENV PYTHONDONTWRYTEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/unrealchayka/blog/

COPY /requarements.txt /home/unrealchayka/blog/
RUN pip install -r /home/unrealchayka/blog/requarements.txt

COPY . /home/unrealchayka/blog/

EXPOSE 8000

CMD ["python", "manage.py", "migrate"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
