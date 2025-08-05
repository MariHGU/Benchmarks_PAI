# Remove existing Docker installation
sudo dnf remove docker podman-docker

# Clean up any remaining configuration
sudo rm -rf /etc/docker

# Reinstall Docker (adjust version as needed)
sudo dnf install docker docker-compose-plugin