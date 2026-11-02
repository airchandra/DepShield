FROM python:3.12-slim

# Set working directory
WORKDIR /harness

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    lsb-release \
    openjdk-17-jdk \
    golang-1.21 \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Install Maven
RUN apt-get update && apt-get install -y --no-install-recommends \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Syft for SBOM generation
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Install Grype for vulnerability scanning
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Install osv-scanner
RUN curl -L https://github.com/google/osv-scanner/releases/download/v1.3.6/osv-scanner_linux_amd64 -o /usr/local/bin/osv-scanner && \
    chmod +x /usr/local/bin/osv-scanner

# Install Trivy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    apt-transport-https \
    gnupg \
    lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends trivy && \
    rm -rf /var/lib/apt/lists/*

# Install pip-audit for Python scanning
RUN pip install --no-cache-dir pip-audit

# Install govulncheck for Go
RUN go install golang.org/x/vuln/cmd/govulncheck@latest

# Install cargo-audit for Rust
RUN cargo install cargo-audit --locked

# Copy project files
COPY . /harness/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose default output volume
VOLUME ["/output"]

# Set default command
ENTRYPOINT ["depshield"]
CMD ["--help"]
