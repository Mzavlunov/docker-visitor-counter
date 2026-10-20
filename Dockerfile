# Start with an image that already contains Python.
FROM python:3.12-slim

# Create a working folder inside the image.
WORKDIR /app

# Put our Python file into the image.
COPY app.py .

# Document the port the app listens on.
EXPOSE 5000

# Launch the program when a container starts.
CMD ["python", "app.py"]
