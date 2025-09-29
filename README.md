# Parameta DevOps MVP Platform

This repository contains a minimum viable platform that demonstrates the operational capabilities requested in the Parameta job description. The codebase is intentionally lightweight while covering continuous delivery, AWS infrastructure automation, container orchestration, observability, and operational tooling.

## Repository structure

| Path | Description |
| --- | --- |
| `app/` | Sample HTTP microservice used as the workload under management. |
| `Dockerfile` & `.dockerignore` | Container definition for local builds and CI/CD. |
| `Jenkinsfile` | Declarative pipeline that performs tests, container build, push, and Kubernetes deployment stages. |
| `k8s/` | Kubernetes deployment and service manifests for the workload. |
| `monitoring/` | Prometheus scrape configuration, alert rules, and a Grafana dashboard for system visibility. |
| `scripts/` | Helper scripts for operating the platform (e.g., deployment). |
| `terraform/` | Infrastructure-as-Code that provisions an AWS EKS environment suitable for the MVP. |

## Getting started

1. **Run unit tests locally**
   ```bash
   python -m unittest discover -s app/tests
   ```

2. **Build and run the container**
   ```bash
   docker build -t parameta/devops-mvp:local .
   docker run --rm -p 8000:8000 parameta/devops-mvp:local
   ```
   Access the application at `http://localhost:8000/` and the health endpoint at `http://localhost:8000/healthz`.

3. **Deploy to Kubernetes**
   ```bash
   ./scripts/deploy.sh parameta/devops-mvp:local
   ```
   The script applies the manifests in `k8s/` and waits for the rollout to finish.

4. **Provision AWS infrastructure**
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```
   This creates an EKS cluster with supporting networking suitable for staging and production workloads.

5. **Configure monitoring**
   - Deploy the Prometheus stack with the provided configuration to collect metrics from Kubernetes and the sample service.
   - Import the Grafana dashboard located at `monitoring/grafana/dashboard.json` to visualize replica counts, error rates, and resource usage.

## Continuous Delivery workflow

The Jenkins pipeline performs the following actions:

1. Checks out the repository source.
2. Runs the Python unit test suite.
3. Builds and pushes the workload container image to the configured registry.
4. Deploys the latest image to the Kubernetes cluster using `kubectl` with stored credentials.

This workflow can be extended with environment-specific deployment stages, security scanning, or integration test gates.

## Observability and operations

- **Prometheus** scrapes the Kubernetes control plane and the application pods, storing time-series metrics and firing alerts through Alertmanager when replica availability or error rate thresholds are exceeded.
- **Grafana** surfaces those metrics via a prebuilt dashboard to aid troubleshooting and capacity planning.
- **scripts/deploy.sh** provides a repeatable mechanism to update workloads while waiting for rollout completion, ensuring stability across Linux-based environments.

The combination of automation, infrastructure provisioning, monitoring, and operational scripts delivers a functional MVP that aligns with the Parameta role requirements.
