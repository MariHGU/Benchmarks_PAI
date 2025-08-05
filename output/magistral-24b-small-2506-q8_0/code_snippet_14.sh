ls -l /var/run/docker.sock  # Should be srw-rw---- root:docker
   ls -Z /var/run/docker.sock # Check SELinux context
   sudo restorecon -Rv /var/run/docker.sock # Restore if incorrect