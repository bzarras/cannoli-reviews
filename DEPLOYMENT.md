# Deployment Guide

This document describes the deployment process for the Cannoli Reviews application using Docker containers and Ansible.

## Overview

The application is deployed to an EC2 instance using:
- **Docker**: Containerization of the application
- **Ansible**: Application deployment automation
- **GitHub Actions**: CI/CD pipeline
- **GitHub Container Registry**: Docker image storage
- **Infrastructure Repo**: Manages nginx, SSL certificates, and system setup

## Architecture

```
GitHub Actions → Build Docker Image → Push to GHCR → Ansible → EC2 → Docker Container
```

## Prerequisites

### EC2 Instance Setup

1. Launch an EC2 instance with Ubuntu 20.04 or later
2. Configure security groups to allow:
   - SSH (port 22) from GitHub Actions runners
   - HTTP (port 80) for web traffic
   - HTTPS (port 443) if using SSL

### GitHub Repository Secrets

Configure the following secrets in your GitHub repository:

- `EC2_USER`: SSH username (usually `ubuntu`)
- `EC2_HOST`: EC2 instance public IP or domain
- `EC2_SSH_PRIVATE_KEY`: Private SSH key for EC2 access
- `EC2_SG_ID`: Security group ID for managing access
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region (e.g., `us-east-1`)

## Deployment Process

### 1. Automatic Deployment (GitHub Actions)

When you push to the `main` branch, the following happens:

1. **Build Docker Image**: Creates a Docker image with your application
2. **Push to Registry**: Uploads the image to GitHub Container Registry
3. **Deploy with Ansible**: Runs Ansible playbooks to deploy to EC2
4. **Container Management**: Starts/updates the Docker container

### 2. Manual Deployment

If you need to deploy manually:

```bash
# Build and push Docker image
docker build -t ghcr.io/your-username/cannoli-reviews:latest .
docker push ghcr.io/your-username/cannoli-reviews:latest

# Deploy with Ansible
ansible-playbook -i ansible/inventory.yml ansible/deploy.yml
```

## File Structure

```
cannoli-reviews/
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Local development
├── .dockerignore             # Files to exclude from Docker build
├── ansible/
│   ├── deploy.yml            # Main deployment playbook
│   ├── inventory.yml         # EC2 host configuration
│   ├── ansible.cfg           # Ansible configuration
│   └── nginx.conf            # Nginx reverse proxy config
├── .github/workflows/
│   └── main.yml              # CI/CD pipeline
└── scripts/
    └── docker-test.sh        # Local Docker testing
```

## Configuration

### Environment Variables

The application can be configured with these environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `ADMIN_TOKEN`: Admin authentication token

### Docker Configuration

The Docker container:
- Runs on port 8001
- Uses Amazon Linux 2023 with Python 3.11
- ARM-compatible for AWS Graviton processors
- Runs as non-root user
- Includes SQLite database file
- Mounts data volume for persistence

### Infrastructure Management

The infrastructure repo handles:
- Nginx installation and configuration
- SSL certificate management (Let's Encrypt)
- Docker installation and setup
- System-level security and updates
- Application-specific nginx configurations

## Troubleshooting

### Common Issues

1. **Container won't start**: Check logs with `docker logs cannoli-reviews`
2. **Nginx not working**: Check infrastructure repo for nginx configuration
3. **Permission issues**: Ensure SSH key has correct permissions (600)
4. **Port conflicts**: Make sure port 8000 is available on EC2

### Debugging Commands

```bash
# Check container status
docker ps -a

# View container logs
docker logs cannoli-reviews

# Check nginx status (managed by infrastructure repo)
sudo systemctl status nginx

# Test application directly
curl http://localhost:8001/

# Check Ansible connectivity
ansible webserver -i ansible/inventory.yml -m ping
```

## Security Considerations

- SSH keys are managed securely through GitHub secrets
- Docker containers run as non-root user
- Nginx provides an additional security layer
- Security groups control network access
- Regular security updates are applied

## Monitoring

- Docker health checks monitor container status
- Nginx logs provide access information
- Application logs are available in the container
- Consider setting up monitoring for the EC2 instance

## Backup and Recovery

- Database files are stored in Docker volumes
- Consider regular backups of the data volume
- Docker images are versioned for rollback capability
- Ansible playbooks enable quick redeployment 
