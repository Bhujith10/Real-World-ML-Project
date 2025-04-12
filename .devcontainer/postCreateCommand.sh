#!/bin/bash
set -e

echo "📦 Setting up project environment..."

cd /workspaces/real-time-ml-system-cohort-4

# Setup Python virtualenv
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
fi

# Setup mise
mise trust
mise install
echo 'eval "$(/usr/local/bin/mise activate bash)"' >> ~/.bashrc

echo "✅ Python venv & mise tools setup done"

# Install latest kubectl
echo "📦 Installing kubectl..."
tmp_dir=$(mktemp -d)
cd "$tmp_dir"
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin/
cd -
rm -rf "$tmp_dir"

echo "✅ kubectl installed"

# Configure Docker to use systemd cgroup driver (required by kind)
echo "🔧 Configuring Docker to use systemd cgroup driver..."
mkdir -p /etc/docker
cat <<EOF > /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF

echo "🔄 Restarting Docker daemon..."
systemctl restart docker

# Wait for Docker to be ready
until docker info > /dev/null 2>&1; do
  echo "⏳ Waiting for Docker daemon to start..."
  sleep 2
done
echo "✅ Docker is ready"

# Create a kind cluster
echo "🚀 Creating Kind cluster..."
kind create cluster --name devcluster

echo "✅ Kind cluster created"
echo "🎉 postCreateCommand.sh completed successfully!"
