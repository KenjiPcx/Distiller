# Use a base image with Python installed
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt .

# Install required dependencies (this step will be cached unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files (e.g., the generated code and test files)
COPY . .

# Set the default environment variable for the run profile
ENV RUN_PROFILE="code_check"

# Define the entrypoint script to decide what to run based on the profile
ENTRYPOINT ["sh", "-c", "if [ \"$RUN_PROFILE\" = 'code_check' ]; then \
                            python generated/generated_code.py; \
                         elif [ \"$RUN_PROFILE\" = 'full_check' ]; then \
                            pytest --maxfail=1 --disable-warnings -v; \
                         else \
                            echo 'Invalid RUN_PROFILE specified'; \
                         fi"]