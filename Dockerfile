FROM python:3.9

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements.txt
COPY requirements.txt /tmp/
RUN pip install --upgrade --requirement /tmp/requirements.txt && \
    pip cache purge

# Clear /tmp
RUN rm -rf /tmp/*

# Copy app
COPY aws-pricing /app

WORKDIR /app

CMD [ "streamlit", "run", "main.py" ]