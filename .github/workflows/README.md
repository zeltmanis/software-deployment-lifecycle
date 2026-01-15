# CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## ci-cd.yml

Main CI/CD pipeline that runs on every push to `main` or `develop` branches.

### Workflow Steps

#### 1. Test Job
- **Trigger**: Push or pull request to main/develop
- **Services**: MariaDB 11.2 container
- **Steps**:
  1. Checkout code
  2. Set up Python 3.12
  3. Cache dependencies for faster builds
  4. Install Python packages
  5. Wait for MariaDB to be healthy
  6. Run pytest test suite
  7. Generate test summary

#### 2. Build and Push Job
- **Trigger**: Only on successful tests + push to main branch
- **Registry**: GitHub Container Registry (ghcr.io)
- **Steps**:
  1. Checkout code
  2. Set up Docker Buildx
  3. Login to GHCR
  4. Extract image metadata (tags, labels)
  5. Build and push backend Docker image
  6. Generate build summary

### Image Tagging Strategy

Images are tagged with:
- `latest` - Latest build from main branch
- `main-<git-sha>` - Specific commit SHA
- `main` - Branch name

Example:
```
ghcr.io/username/software-deployment-lifecycle-backend:latest
ghcr.io/username/software-deployment-lifecycle-backend:main-a1b2c3d
ghcr.io/username/software-deployment-lifecycle-backend:main
```

### Viewing Results

1. Go to repository → Actions tab
2. Click on latest workflow run
3. View test results and build logs
4. Check test/build summaries

### Local Testing Before Push

Test the workflow locally before pushing:
```bash
# Run tests
docker-compose -f docker-compose.test.yml up -d
docker exec ledger_test_backend pytest

# Build image
docker build -t test-backend ./backend
```

### Workflow Badges

Add status badge to your README:
```markdown
![CI/CD Pipeline](https://github.com/USERNAME/REPO/actions/workflows/ci-cd.yml/badge.svg)
```

### Troubleshooting

**Tests fail in CI but pass locally:**
- Check environment variables
- Verify database connection settings
- Review CI logs for specific errors

**Docker build fails:**
- Check Dockerfile syntax
- Verify all files are committed
- Review build logs in Actions tab

**Image push fails:**
- Ensure GITHUB_TOKEN has write permissions
- Check repository settings → Actions → General → Workflow permissions