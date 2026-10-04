# CI/CD Pipeline for AI-Enabled Application

Production-grade CI/CD pipeline using GitHub Actions with automated testing, regression checks, Docker deployment, and automatic rollback on failures.

## Architecture

```
Push → GitHub Actions Workflow
         ├─ Run Tests
         ├─ Model Output Regression Check
         ├─ Build Docker Image
         ├─ Deploy to K8s
         └─ Health Check + Automatic Rollback
```

## Stack

- **GitHub Actions**: CI/CD orchestration
- **Python**: Application code
- **Docker**: Container packaging
- **Kubernetes**: Deployment orchestration
- **pytest**: Test framework
- **Claude API**: AI workload

## Pipeline Stages

### 1. **Test & Validation**
- Unit tests with pytest
- Model output regression detection
- Code quality checks

### 2. **Build**
- Docker image creation
- Multi-stage builds for optimization
- Container registry push

### 3. **Deploy**
- Kubernetes rolling deployment
- Blue-green deployment support
- Health checks before marking as ready

### 4. **Monitoring & Rollback**
- Post-deployment health verification
- Automatic rollback on failures
- Metrics collection

## Project Structure

```
ci-cd-pipeline/
├── .github/workflows/
│   └── ci-cd.yml              # Main GitHub Actions workflow
├── app/
│   ├── main.py                # AI application entry point
│   ├── model.py               # AI model inference
│   └── requirements.txt        # Python dependencies
├── tests/
│   ├── test_model.py          # Model unit tests
│   ├── test_regression.py      # Regression tests
│   └── fixtures/              # Test data
├── k8s/
│   ├── deployment.yaml        # Kubernetes deployment
│   ├── service.yaml           # K8s service
│   └── hpa.yaml               # Horizontal Pod Autoscaler
├── .docker/
│   ├── Dockerfile             # Production Dockerfile
│   └── Dockerfile.test        # Testing Dockerfile
└── README.md
```

## CI/CD Workflow

### Trigger Events
- Push to main branch
- Pull requests
- Manual workflow dispatch
- Scheduled (nightly tests)

### Job Stages

1. **Unit Tests**
   - Python test suite
   - Coverage report
   - Fail on <80% coverage

2. **Regression Tests**
   - Compare model outputs
   - Semantic similarity check
   - Fails if regression detected

3. **Build**
   - Docker multi-stage build
   - Push to registry
   - Tag with git SHA

4. **Deploy**
   - Apply K8s manifests
   - Wait for pod readiness
   - Run smoke tests

5. **Health Check**
   - POST to health endpoint
   - Verify model inference
   - Automatic rollback on failure

### Rollback Strategy

**Automatic Rollback Triggers**:
- Health check failure
- Timeout >5 minutes
- Error rate >5%

**Rollback Process**:
1. Detect failure condition
2. Revert to previous deployment
3. Alert on Slack
4. Log incident

## Configuration

### Environment Variables

```yaml
REGISTRY_URL: ghcr.io
REGISTRY_USERNAME: ${{ github.actor }}
REGISTRY_PASSWORD: ${{ secrets.GITHUB_TOKEN }}
DEPLOYMENT_TIMEOUT: 300
HEALTH_CHECK_RETRIES: 5
```

### Kubernetes Secrets

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<username> \
  --docker-password=<token>
```

## Usage

### Triggering Manually

```bash
gh workflow run ci-cd.yml --ref main
```

### Monitoring Deployment

```bash
# Watch pod rollout
kubectl rollout status deployment/ai-app -n production

# View logs
kubectl logs -f deployment/ai-app -n production

# Check health
curl https://api.example.com/health
```

### Rolling Back

```bash
# Automatic (triggered by health checks)
# Manual:
kubectl rollout undo deployment/ai-app -n production
```

## Performance Considerations

**Build Optimization**:
- Multi-stage Docker builds
- Layer caching strategy
- Parallel test execution

**Deployment Efficiency**:
- Rolling updates (no downtime)
- Pod disruption budgets
- Resource requests/limits

**Rollback Speed**:
- Pod readiness probes
- Liveness checks
- Graceful shutdown (30s)

## Monitoring & Observability

### Metrics Collected
- Deployment duration
- Test pass rate
- Model output stability
- Health check latency
- Rollback count

### Alerts
- Failed workflows → Slack notification
- Rollbacks triggered → PagerDuty
- Regression detected → Email

### Logs
- GitHub Actions logs (30 days retention)
- Kubernetes pod logs (persistent volume)
- Application logs (structured JSON)

## Advanced Features

### Blue-Green Deployment

```yaml
- name: Deploy Blue
  run: kubectl apply -f k8s/deployment-blue.yaml

- name: Test Blue
  run: ./tests/smoke_test.sh blue

- name: Switch to Blue
  run: kubectl patch service ai-app -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Canary Deployment

```yaml
- name: Deploy Canary (10% traffic)
  run: kubectl apply -f k8s/canary.yaml

- name: Monitor Metrics (2 minutes)
  run: ./scripts/monitor_canary.sh

- name: Promote or Rollback
  run: ./scripts/canary_decision.sh
```

### Database Migrations

```yaml
- name: Run Migrations
  run: |
    kubectl run migration --image=ai-app:${{ github.sha }} \
      --command -- python -m alembic upgrade head
```

## Core Responsibilities Demonstrated

✓ **GitHub Actions**: Complete CI/CD pipeline automation
✓ **Docker**: Multi-stage containerization
✓ **Kubernetes**: Orchestration and rolling deployments
✓ **Regression Testing**: AI model output validation
✓ **Automated Rollback**: Health check-triggered recovery
✓ **Cloud-Native Design**: Scalable, resilient deployment

## Troubleshooting

### Workflow Won't Start
- Check branch protection rules
- Verify workflow syntax: `gh workflow view ci-cd.yml`
- Check secrets configuration

### Deployment Timeout
- Review pod readiness probe
- Check resource limits
- Increase timeout value

### Regression Test Failures
- Check baseline model outputs
- Verify test fixtures
- Review similarity threshold

### Rollback Not Triggered
- Verify health check endpoint
- Check webhook configuration
- Review logs

## Security Best Practices

✓ Use GITHUB_TOKEN instead of PAT
✓ Secrets stored in GitHub organization
✓ Registry authentication via tokens
✓ K8s RBAC for service account
✓ Network policies for pod communication
✓ Image scanning for vulnerabilities

## Cost Optimization

- Spot instances for non-prod environments
- Resource requests matching actual usage
- Automatic scaling with HPA
- Scheduled scaling (dev/prod environments)
- Docker layer caching for faster builds
