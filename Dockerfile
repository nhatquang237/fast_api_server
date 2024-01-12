FROM python:3.10.6-slim

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY src /app

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
