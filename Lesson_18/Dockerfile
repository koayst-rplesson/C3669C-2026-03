# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY mcp_server_01.py /app/

# Expose the port the FastMCP server will run on
EXPOSE 8000

# Command to run the FastMCP server
CMD ["python", "mcp_server_01.py"]
