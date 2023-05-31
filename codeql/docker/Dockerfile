# We need to pull the best image possible (lightest for quick response)
FROM python:3

RUN pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the saved model and vectorizer to the container (still have to think of that)
COPY lr_model.pkl .
COPY vectorizer.pkl .

#Copy the script to run the predicition
COPY predict.py .
