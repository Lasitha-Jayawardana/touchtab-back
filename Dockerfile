FROM python:3.8

# Create workDir
RUN mkdir code
WORKDIR code
ENV PYTHONPATH = /code

# Install requirements
RUN pip install --upgrade pip==21.1.1
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copy Code
COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]