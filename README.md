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

## Prerequisites

Before running the MVP, make sure your workstation or CI agent satisfies the following requirements:

### Tooling

1. **Python 3.11 or newer** – required for running the sample service and executing its unit tests.
   ```bash
   python3 --version
   ```
   Install via [python.org downloads](https://www.python.org/downloads/) or your package manager (`brew install python@3.11`, `sudo apt install python3.11`, etc.).

2. **Docker** – used to build and run the container image locally and inside the Jenkins pipeline.
   ```bash
   docker --version
   ```
   Follow the instructions for your platform in the [Docker Engine installation guide](https://docs.docker.com/engine/install/).

3. **kubectl** – required to interact with Kubernetes clusters and for the deployment script.
   ```bash
   kubectl version --client
   ```
   Install using the [official Kubernetes instructions](https://kubernetes.io/docs/tasks/tools/).

4. **Terraform** – provisions the AWS networking and EKS cluster defined under `terraform/`.
   ```bash
   terraform -version
   ```
   Download from [terraform.io](https://www.terraform.io/downloads) or use a package manager (`brew tap hashicorp/tap && brew install hashicorp/tap/terraform`, `choco install terraform`, etc.).

### Credentials and access

* **AWS credentials** with permissions to create VPC, IAM, EKS, and supporting resources. Export them as environment variables or configure them via the AWS CLI before running Terraform:
  ```bash
  export AWS_ACCESS_KEY_ID=...
  export AWS_SECRET_ACCESS_KEY=...
  export AWS_DEFAULT_REGION=us-east-1
  ```

* **Container registry access** where Docker can push/pull the image tag you want to use (for example Amazon ECR, Docker Hub, or a private registry). Update the image references in `scripts/deploy.sh` and the Jenkinsfile if you need a fully qualified registry path.

* **Kubernetes cluster credentials** (`kubeconfig`) for the environment where you will deploy the workload. You can supply these manually or generate them after provisioning the EKS cluster with Terraform.

* **Jenkins credentials** (optional) to run the provided pipeline: create a Docker registry credential named `docker-registry-credentials` and a Kubernetes config file credential named `kubeconfig-eks-cluster`.

Once the prerequisites are satisfied, follow the walkthrough below.

## Getting started

1. **Run unit tests locally**
   ```bash
   python -m unittest discover -s app/tests
   ```
   This confirms the HTTP handlers respond correctly before you build or deploy the service.

2. **Build and run the container**
   ```bash
   docker build -t parameta/devops-mvp:local .
   docker run --rm -p 8000:8000 parameta/devops-mvp:local
   ```
   Access the application at `http://localhost:8000/` and the health endpoint at `http://localhost:8000/healthz` to validate the container.

3. **Deploy to Kubernetes**
   ```bash
   ./scripts/deploy.sh parameta/devops-mvp:local
   ```
   The script applies the manifests in `k8s/` and waits for the rollout to finish so you can immediately check pod status with `kubectl get pods`.

4. **Provision AWS infrastructure (optional)**
  ```bash
  cd terraform
  terraform init
  terraform apply
  ```
  Set variables (e.g., `-var="cluster_name=parameta-devops-mvp"`) as needed. Terraform creates an EKS cluster and networking; afterwards run `aws eks update-kubeconfig --name <cluster>` to target the new cluster.
  > **Note:** The configuration pins the AWS provider to the 5.x series because the upstream EKS module has not yet adopted provider 6.x. If you already initialized this directory with an older lock file, rerun `terraform init -upgrade` (or delete `.terraform.lock.hcl`) so Terraform downloads a compatible provider version before planning or applying.

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
