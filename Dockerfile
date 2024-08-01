FROM python:3
# Set the working directory in the container
WORKDIR /app
COPY . /app
COPY /bcd /app/files
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
