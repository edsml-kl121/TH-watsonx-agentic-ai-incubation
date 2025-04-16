FROM python:3.11-slim


# Copy your application code
COPY . /src
WORKDIR /src

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

# Run your startup script
CMD ["uvicorn", "app:app","--host","0.0.0.0","--port","8000"]