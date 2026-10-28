# GitOps candidate platform and adoption plan

## Safe relationship with the existing deployment

Argo CD currently watches **`kubernetes/` on main** and has automatic sync and pruning enabled. The new `releases/` tree is **not referenced** by that controller. Merging it does **not** change live Kubernetes desired state. It is a candidate promoted-environment model, not a declaration that three clusters are running.

## Environment boundaries

`releases/base` references the same application deployment and service. Overlays for dev, staging and production render distinct namespaces with strict pod security labels, resource metrics HPA, disruption budgets, narrow ingress policies and nonroot container hardening. The Argo CD AppProject example enumerates allowed namespaces and Kubernetes resource kinds. It does not grant permission to deploy arbitrary cluster-wide manifests.

## Operations before enablement

Use `kubectl kustomize releases/overlays/dev` to inspect the rendered output. CI validates all three overlays and detects security-control regressions. Test the image under non-root identity with a read-only root filesystem before enabling the overlay; `/tmp` uses an ephemeral volume. The example ingress NetworkPolicy expects an `ingress-nginx` namespace and a CNI that enforces policy. Update the allowlist for your actual ingress controller before applying.

Before creating Argo CD Applications for these paths, define a private artifact-promotion workflow, signed/digest-pinned images, environment-specific ownership/notifications, rollback procedures, human production approval and cluster integration tests. Do not point production at the overlays until those prerequisites pass.

## Rollback

Revert the Git commit containing the image or spec change. Confirm Argo CD sync/health and workload probes. For a bad release, halt further promotions, preserve rollout events, and evaluate PDB/HPA status before allowing additional changes. Do not `kubectl edit` live workloads as a normal rollback method.
