# Software Deployment Lifecycle

![CI/CD Pipeline](https://github.com/zeltmanis/software-deployment-lifecycle/actions/workflows/ci-cd.yml/badge.svg)

Capstone project demonstrating a modern software deployment lifecycle using Docker, GitHub Actions, and automated testing.
Capstone project demonstrating a modern software deployment lifecycle using Docker, GitHub Actions, and automated testing.

## Project Overview

This project showcases how a Python application moves through development and testing environments using containerization and CI/CD practices.

### Key Features
- 🐳 Docker-based development and test environments
- 🔄 Automated testing with GitHub Actions
- 📊 Grafana monitoring dashboard in test environment
- 🗄️ MariaDB database with environment-specific data management
- ⚡ FastAPI backend with automatic API documentation

## Technology Stack

- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **Database**: MariaDB 11.2
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: pytest
- **Monitoring**: Grafana
- **Frontend**: HTML/CSS/JavaScript (Bootstrap for test env)

## Project Structure
```
software-deployment-lifecycle/
├── backend/          # FastAPI application
├── frontend/         # UI for dev and test environments
├── database/         # Database initialization scripts
├── grafana/          # Monitoring dashboard configuration
├── .github/          # GitHub Actions workflows
└── docker-compose.*.yml  # Environment configurations
```

## Environments

### Development Environment
- Simple frontend for quick testing
- Persistent MariaDB data for developers
- Hot-reload for rapid development

### Test Environment
- Styled frontend with better UX
- Clean, seeded test data (reset on startup)
- Automated testing suite
- Grafana metrics dashboard

## Getting Started

*Coming soon - setup instructions will be added as the project develops*

## Project Progress

This project is structured into epics tracked through GitHub commits and issues.

- [x] Epic 1: Project Setup
- [x] Epic 2: FastAPI Backend
- [x] Epic 3: MariaDB Integration
- [x] Epic 4: Dev Environment
- [x] Epic 5: Test Environment
- [x] Epic 6: Automated Testing
- [x] Epic 7: GitHub Actions CI/CD
- [ ] Epic 8: Grafana Dashboard

## Author

Created as part of Software Application Capstone Project
University Project - January 2026

## License

MIT License - See LICENSE file for details
