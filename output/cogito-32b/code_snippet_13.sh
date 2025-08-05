# Stop Docker
sudo systemctl stop docker

# Remove the PID file if it exists
sudo rm -f /var/run/docker.pid

# Start Docker again
sudo systemctl start docker

# Verify status
sudo systemctl status docker