# Cloud App GitOps

This repository contains the Kubernetes deployment configuration for the `cloud-app` application. I use it as the GitOps source of truth monitored by Argo CD.

The CI pipeline is kept in a separate application repository. After Jenkins builds and publishes a new container image, it updates the image version in this repository. Argo CD detects the Git change and automatically synchronizes the desired state to Kubernetes.

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
Application Source
       ↓
Jenkins CI
       ↓
Run Automated Tests
       ↓
Build Docker Image
       ↓
Push Image to Container Registry
       ↓
Update Image Tag in GitOps Repository
       ↓
Argo CD Detects Git Change
       ↓
Automatic Synchronization
       ↓
Kubernetes Deployment
```

## Argo CD

I configured `argocd-application.yaml` to monitor the `kubernetes` directory on the `main` branch and deploy the desired state to the `devops-demo` namespace.

For this project, Argo CD is configured with automated synchronization, pruning, and self-healing.

This keeps Kubernetes delivery separate from the Jenkins CI process. Jenkins updates Git, while Argo CD is responsible for reconciling the Kubernetes environment with the desired state stored in this repository.

## Kubernetes Deployment

I configured the application as a Kubernetes Deployment with two replicas.

The deployment includes:

- Two application replicas
- RollingUpdate deployment strategy
- `maxUnavailable: 0`
- `maxSurge: 1`
- Readiness probe using `/health`
- Liveness probe using `/health`
- CPU and memory requests
- CPU and memory limits
- Versioned Docker images

## Kubernetes Resources

- Namespace: `devops-demo`
- Deployment: `cloud-app`
- Service: `cloud-app`
- Application port: `5000`
- Service port: `80`
- Service type: `ClusterIP`

## GitOps Rollback Test

I tested the rollback workflow by changing the deployment from:

```text
alexcgodwin/cloud-app:6
```

to the previous image:

```text
alexcgodwin/cloud-app:5
```

After committing the change to Git, Argo CD detected the previous desired state and automatically synchronized it to Kubernetes.

I verified the running deployment directly from Kubernetes:

```bash
kubectl get deployment cloud-app -n devops-demo -o=jsonpath="{.spec.template.spec.containers[0].image}"
```

The deployment returned:

```text
alexcgodwin/cloud-app:5
```

After verifying the rollback, I restored the GitOps configuration to image `6`. Argo CD synchronized the change and returned the application to a Healthy and Synced state.

## Security

Sensitive credentials and access tokens are not stored in this repository. Jenkins credentials are used by the CI pipeline when authentication is required.

## Related Repository

The application source code, automated tests, Dockerfile, and Jenkins CI pipeline are maintained separately in the `jenkins-ci-pipeline` repository.
