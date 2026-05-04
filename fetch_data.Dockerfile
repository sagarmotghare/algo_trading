FROM python:3.12-alpine
WORKDIR /fetch_data

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY fetch_data.py main.py
COPY ./sql/ ./sql/

# Running application
CMD [ "python", "main.py" ]