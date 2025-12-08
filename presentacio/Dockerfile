FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6 8.9 9.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3.9 \
    python3.9-dev \
    python3-pip \
    build-essential \
    ninja-build \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.9 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Set working directory
WORKDIR /workspace/iVR-GS

# Copy project files
COPY requirements.txt .
COPY submodules ./submodules

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r requirements.txt

# Build CUDA extensions
RUN pip install -e ./submodules/diff-gaussian-rasterization && \
    pip install -e ./submodules/simple-knn

# Copy the rest of the project
COPY . .

# Set display for GUI (optional)
ENV DISPLAY=:0

CMD ["/bin/bash"]