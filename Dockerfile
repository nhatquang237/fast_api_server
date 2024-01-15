FROM python:3.10.6-slim

# Set the working directory
WORKDIR /app

# Set variable for environment checking
ENV IN_CONTAINER=true

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY src /app

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
