#base image
FROM python:3.9-slim

#set working directory
WORKDIR /app

#copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy app code
COPY . .

#run the flask app
CMD [ "python", "app.py" ]

