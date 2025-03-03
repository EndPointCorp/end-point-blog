---
author: "Kannan Ponnusamy"
date: 2025-03-03
title: "How to run DeepSeek R1 on AWS: Optimizing Performance and Cost with Instance Store Diskse"
github_issue_number: 2095
featured:
  image_url: /blog/2025/02/case-of-the-mistimed-script/clock-tower.webp
description: "How to - Ansible role testing with Molecule and Docker, including setup, scenario creation, and GitLab CI/CD integration for automated, reliable automation testing"
tags:
- sysadmin
- aws
- ai
- deepseek
---

![A low-angle view of an old European church clock tower. The square tower with rounded corners is ornamented with gothic styling, and topped with a golden eagle.](/blog/2025/02/case-of-the-mistimed-script/clock-tower.webp)

![the letters A and I are made up of different shapes](/blog/2025/02/testing-ansible-with-molecule/photo-of-optical-disc-drive.jpg)<br>
[Photo](https://unsplash.com/photos/the-letters-are-made-up-of-different-shapes-qbId5TLFG2s) by [Neeqolah Creative Works](https://unsplash.com/@neeqolah)


# How to run DeepSeek R1 on AWS: Optimizing Performance and Cost with Instance Store Disks

## What is Deepseek R1 model?
DeepSeek R1 is a groundbreaking AI model that combines advanced reasoning capabilities with an open-source framework, making it accessible for both personal and commercial use. DeepSeek R1 models have been trained to think step-by-step before responding with an answer. As a result, they excel at complex reasoning tasks such as coding, mathematics, planning, puzzles, and agent workflows.

## Experiments to find the best instance type and storage configuration

In this post, we'll explore how to deploy DeepSeek R1 on AWS with instance store disks while keeping launch times minimal and costs optimized. We will see

- Which AWS instances provide fastest instance store disk performance
- How to launch DeepSeek R1 in minutes

We've tested various storage options to determine the optimal setup for different use cases. The table below summarizes our findings, comparing model load times, total startup times and other pros and cons:

| Configuration | Model download & Load Time | Total Startup Time | Pros | Cons |
|---------------|----------------|-------------------|------|------|
| EBS gp3 | ~15 minutes | ~20 minutes | Persistent storage | Slow (250 MB/s), costly for high IOPS |
| S3 with s4cmd → NVMe | 4 minutes | 5 minutes | **Fastest option**, cost-effective | Ephemeral storage (lost on shutdown) |
| S3 with aws cli | ~8 minutes | ~8 minutes | | Slower than s4cmd (~300-400 MB/s) |
| Mountpoint for S3 | 3 minutes | ~4 minutes | Very fast | Potential high costs due to per-request charges |
| io2 EBS volume | ~15 minutes | ~20 minutes | Persistent storage | Expensive, charged per GB and IOPS |

## ⚡ How Instance store disks matter for High-Speed Deployment

When running these large models, disk I/O becomes a critical bottleneck. As we mentioned in the above tests, instance store disks (also called ephemeral storage) provide several advantages:

- Higher throughput: Up to 3x faster than EBS volumes in many cases
- Lower latency: Physically attached to the host server
- No additional cost: Included in the instance price

The only downside is that instance store disks are ephemeral, which means that the disk is lost when the instance is stopped or terminated.

Now that we've defined what kind of instances settings are best for DeepSeek R1, let's look at how to deploy them.

## 1. Deployment Steps

### Step 1. Create a Base AMI with dependencies pre-installed with systemd service and a startup script

Install CUDA, nvidia drivers and other dependencies. 

```bash
sudo apt-get update
sudo apt-get install build-essential cmake curl libcurl4-openssl-dev s4cmd -y
sudo apt install -y cuda-drivers nvidia-cuda-toolkit nvidia-utils-550 nvidia-utils-550-server nvidia-driver-550
```

Download and Compile llama.cpp with CUDA support:

```bash
git clone https://github.com/ggerganov/llama.cpp
cmake llama.cpp -B llama.cpp/build -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-server
cp llama.cpp/build/bin/llama-* llama.cpp
```

Step 2: Download and Start the Llama.cpp server to serve the model 

Here is the systemd service:

Create file at `/etc/systemd/system/llama.service`:

```ini
[Unit]
Description=Setup FS + LLama.cpp Server
After=network.target local-fs.target

[Service]
User=root
WorkingDirectory=/home/ubuntu/
ExecStart=/home/ubuntu/startup.sh
Restart=always
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Here is the startup script, which:

- Creates an ext4 filesystem on the instance storage NVMe device
- Downloads model files to the newly mounted filesystem at `/mnt/nvme` using s4cmd
- Starts the llama.cpp server with optimized parameters for DeepSeek R1

```bash
#!/bin/bash
set -e

echo "🚀 Startup script running..."

NVME_DISK="/dev/nvme1n1"
MOUNT_POINT="/mnt/nvme"
S3_BUCKET="ep-ai-us-east-1"
MODEL_DIR="/mnt/nvme/models"
MODEL_PATH="/mnt/nvme/models/DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf"
LOG_FILE="/var/log/llama_server.log"

# Check if the disk is already mounted
if mount | grep -q "$MOUNT_POINT"; then
    echo "✅ NVMe disk is already mounted. Skipping format & mount steps."
else
    echo "🔹 NVMe disk not found or not mounted. Setting it up..."

    # Format and mount only if the disk is detected but not mounted
    if lsblk | grep -q "nvme1n1"; then
        echo "🔹 Formatting NVMe disk: $NVME_DISK"
        mkfs.ext4 $NVME_DISK
        mkdir -p $MOUNT_POINT
        mount $NVME_DISK $MOUNT_POINT
        echo "$NVME_DISK $MOUNT_POINT ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
    else
        echo "❌ NVMe disk not found. Exiting script."
        exit 1
    fi
fi

# Download models only if directory is empty
mkdir -p $MODEL_DIR
if [ -z "$(ls -A $MODEL_DIR)" ]; then
    echo "🔹 Downloading model files from S3..."
    /usr/bin/s4cmd get -r s3://$S3_BUCKET/ $MODEL_DIR/
    chown -R ubuntu:ubuntu $MODEL_DIR
    echo "✅ Model download complete!"
else
    echo "✅ Model directory is not empty, skipping download."
fi

echo "Starting llama server.."

/home/ubuntu/llama.cpp/build/bin/llama-server \
    --model ${MODEL_PATH} \
    --host 0.0.0.0 \
    --port 10000 \
    --cache-type-k q4_0 \
    --n-gpu-layers 15 \
    --threads 16 \
    --ctx-size 2048 \
    --seed 3407 \
    --log-file ${LOG_FILE} --log-prefix --log-timestamps

echo "✅ Startup script completed!"
```

### 2. Instance Configuration Notes

We're deploying on an AWS `g6e.4xlarge` instance for this setup. If you're using an instance with higher vRAM capacity, you may need to adjust the llama.cpp parameters in the startup script to take full advantage of the additional resources. Remember to create an IAM Role with S3 read-only permissions and assign it to the EC2 instances to ensure secure access to the model files in the S3 bucket.

With the current configuration, we achieve approximately 3 tokens/second inference speed.
For improved performance, consider:

- Upgrading to an instance with more vRAM
- Adjusting the `--n-gpu-layers` parameter accordingly
- Potentially increasing `--threads` based on CPU core availability
- Using Spot instances to reduce costs by up to 70-90% compared to On-Demand pricing

The deployment process remains the same regardless of instance type, with automatic model loading and server initialization.




### 3. Llama Server API is ready. 

Once the systemd service is up, the llama server hosts a local OpenAI-compatible API endpoint at:

```
http://127.0.0.1:10000
```



### 4. Connect it to the Frontend. 

Once the llama server API is running, you can connect various open-source frontend interfaces to provide a user-friendly experience:

- **Open WebUI**: A comprehensive chat interface with conversation history and model switching
- **Vercel AI SDK**: For building custom React/Next.js applications with streaming responses
- **HuggingFace Chat UI**: For creating more complex AI workflows and applications

Point these frontends to the local API endpoint (http://127.0.0.1:10000) and configure them to use the OpenAI-compatible API format.
