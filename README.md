# Cannoli Reviews

A FastAPI application for reviewing cannoli from different pastry shops.

## Development

### Run locally in development mode:
```bash
$ export ADMIN_TOKEN=<make_up_a_token>
$ uvicorn app.main:app --reload
```

### Run with Docker Compose (recommended for development):
```bash
$ docker-compose up --build
```

The application will be available at http://localhost:8001

## Deployment

This application is deployed to EC2 using Docker containers and Ansible.

### Prerequisites

The following GitHub secrets must be configured:
- `EC2_USER`: SSH username for the EC2 instance
- `EC2_HOST`: IP address or hostname of the EC2 instance
- `EC2_SSH_PRIVATE_KEY`: Private SSH key for accessing the EC2 instance
- `EC2_SG_ID`: Security group ID for the EC2 instance
- `AWS_ACCESS_KEY_ID`: AWS access key for managing security groups
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region where the EC2 instance is located

### Deployment Process

1. **Docker Build**: The GitHub Actions workflow builds a Docker image and pushes it to GitHub Container Registry
2. **Ansible Deployment**: Ansible playbooks deploy the container to the EC2 instance
3. **Container Management**: The application runs in a Docker container with automatic restarts

### Manual Deployment

To deploy manually:

```bash
# Build and push Docker image
docker build -t ghcr.io/your-username/cannoli-reviews:latest .
docker push ghcr.io/your-username/cannoli-reviews:latest

# Deploy with Ansible
ansible-playbook -i ansible/inventory.yml ansible/deploy.yml
```

## Architecture

- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (can be configured for other databases)
- **Docker**: Containerization
- **Ansible**: Infrastructure automation
- **GitHub Actions**: CI/CD pipeline

### Some old notes

three.js for 3D cannoli viewer
- example here https://redstapler.co/add-3d-model-to-website-threejs/
- helpful post about hosting on S3 https://sosnowski.dev/post/static-serverless-site-with-nextjs
- might be helpful as well https://milli.is/blog/why-we-self-host-our-serverless-next-js-site-on-aws-with-terraform
- for image optimization and usage of next/image component, I might need https://github.com/cyrilwanner/next-optimized-images
