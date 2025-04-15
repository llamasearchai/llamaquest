FROM python:3.10-slim AS builder

# Install Rust
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install dependencies for Pyxel
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsdl2-dev \
    libsdl2-image-dev \
    libglew-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Rust code first to leverage caching
COPY rust_core/ /app/rust_core/

# Build Rust core
WORKDIR /app/rust_core
RUN cargo build --release

# Copy Python code
WORKDIR /app
COPY python/ /app/python/
COPY assets/ /app/assets/

# Install Python dependencies and build package
WORKDIR /app/python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy config and other files
COPY config.json /app/
COPY README.md /app/

# Runtime image
FROM python:3.10-slim

# Install runtime dependencies for Pyxel
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libglew2.1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy built Python package and Rust library
COPY --from=builder /app/ /app/
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create volume for save files
VOLUME /app/saves

# Expose port for potential web server
EXPOSE 8000

# Run the game
ENTRYPOINT ["python", "-m", "llamaquest"] 