# Cloud App GitOps

This repository stores the Kubernetes deployment configuration for the `cloud-app` application and is monitored by Argo CD.

## Repository Structure

```text
cloud-app-gitops/
├── argocd-application.yaml
├── kubernetes/
│   ├── deployment.yaml
│   ├── namespace.yaml
│   └── service.yaml
└── README.md
```

## GitOps Workflow

```text
Jenkins CI
   ↓
Build and test application
   ↓
Build Docker image
   ↓
Push image to container registry
   ↓
Update image tag in this repository
   ↓
Argo CD detects Git change
   ↓
Argo CD synchronizes Kubernetes
```

## Argo CD

The `argocd-application.yaml` manifest configures Argo CD to monitor the `kubernetes` directory on the `main` branch and deploy the desired state to the `devops-demo` namespace.

Automated synchronization, pruning, and self-healing are enabled for this demonstration project.

## Kubernetes Resources

- Namespace: `devops-demo`
- Deployment: `cloud-app`
- Service: `cloud-app`
- Application port: `5000`
- Service port: `80`

## Security

Sensitive credentials and secrets are not stored in this repository.
