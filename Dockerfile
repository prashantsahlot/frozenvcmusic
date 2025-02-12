FROM nikolaik/python-nodejs:python3.10-nodejs19

# Install ffmpeg
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files to /app
COPY . /app/
WORKDIR /app/

# Upgrade pip and setuptools, install dependencies
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Run both BrandrdXMusic and renderportfix.py
CMD bash -c "python3 -m BrandrdXMusic & python3 frozen.py"
