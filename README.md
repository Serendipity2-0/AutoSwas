# Finance Tasks Application

A Next.js application for managing finance tasks with automated deployment using GitHub Actions.

## Deployment Setup

### GitHub Repository Configuration

1. Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

   - `DEPLOY_HOST`: Production server IP address/hostname
   - `DEPLOY_USER`: SSH username for deployment
   - `DEPLOY_KEY`: SSH private key for authentication
   
   Note: The `GITHUB_TOKEN` secret is automatically available and used for container registry authentication.

### Production Server Setup

1. Create the application directory:
   ```bash
   mkdir -p /opt/finance-tasks
   ```

2. Copy the docker-compose.yml to the server:
   ```bash
   scp docker-compose.yml user@your-server:/opt/finance-tasks/
   ```

3. Create environment file on the server:
   ```bash
   # /opt/finance-tasks/.env
   REGISTRY=ghcr.io
   IMAGE_NAME=your-username/repo-name
   TAG=latest
   ```

### Deployment Process

The application automatically deploys when changes are pushed to the `dev` branch:

1. GitHub Actions workflow:
   - Builds the Docker image
   - Pushes to GitHub Container Registry
   - Deploys to production server

2. The deployment:
   - Uses GitHub Container Registry for image storage
   - Implements zero-downtime deployment
   - Automatically restarts on failure

### Manual Deployment

If needed, you can manually deploy using:

```bash
cd /opt/finance-tasks
docker compose pull
docker compose up -d --force-recreate
```

### Monitoring

Monitor the application using:

```bash
# View logs
docker compose logs -f

# Check container status
docker compose ps
```
