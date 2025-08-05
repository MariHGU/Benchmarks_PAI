# Remove existing installations
sudo dnf remove docker docker-ce docker-engine docker.io

# Add Docker's official repository
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker and Compose
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker version
docker compose version