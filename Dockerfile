FROM python:3.11.9

# Install uv
RUN pip install uv


# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Copy uv.lock
COPY uv.lock ./
COPY pyproject.toml ./

# Copy the rest of the application
COPY . .

# Install project dependencies
RUN uv pip install . --system 

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "src/poc_crewai_developers/main.py"]
