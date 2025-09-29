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



The following tools are free to install and provide everything you need to exercise the MVP locally without consuming paid cloud resources:

1. **Python 3.11 or newer** – required for running the sample service and executing its unit tests.
   ```bash
   python3 --version
   ```
   Install via [python.org downloads](https://www.python.org/downloads/) or your package manager (`brew install python@3.11`, `sudo apt install python3.11`, etc.).

2. **Docker** – builds and runs the container image locally, powers the optional Jenkins instance, and hosts monitoring tooling in containers.
   ```bash
   docker --version
   ```
   Follow the instructions for your platform in the [Docker Engine installation guide](https://docs.docker.com/engine/install/). Docker Desktop includes a lightweight Kubernetes distribution you can use instead of KIND.

3. **kubectl** – required by the deployment script and for inspecting workloads.
   ```bash
   kubectl version --client
   ```
   Install using the [official Kubernetes instructions](https://kubernetes.io/docs/tasks/tools/).

4. **Kubernetes in Docker (KIND)** – provisions a free, local Kubernetes cluster for end-to-end testing. Install via Homebrew, Chocolatey, or the project’s release tarballs:
   ```bash
   kind version
   ```
   <https://kind.sigs.k8s.io/docs/user/quick-start/>

5. **(Optional) Jenkins** – the open-source controller can run locally in Docker when you want to demonstrate the CI/CD pipeline:
   ```bash
   docker run --rm -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts-jdk17
   ```

Once the tooling is in place, follow the zero-cost walkthrough below.

## Zero-cost end-to-end walkthrough

1. **Clone the repository and install Python dependencies**
   ```bash
   git clone https://github.com/parameta/General-DevOps-Practice-Artifacts.git
   cd General-DevOps-Practice-Artifacts
   python -m pip install -r requirements.txt
   ```

2. **Run unit tests locally**
   ```bash
   python -m unittest discover -s app/tests
   ```
   This confirms the HTTP handlers respond correctly before you build or deploy the service.

3. **Build the Docker image**
   ```bash
   docker build -t parameta/devops-mvp:local .


4. **Create a free Kubernetes cluster with KIND**
   ```bash
   kind create cluster --name parameta-mvp
   kind get clusters
   ```
   KIND automatically configures your kubeconfig so `kubectl` targets the new cluster.

5. **Load the image into KIND and deploy the workload**
   ```bash
   kind load docker-image parameta/devops-mvp:local --name parameta-mvp
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
   Set variables (e.g., `-var="cluster_name=parameta-devops-mvp"`) as needed. Terraform creates an EKS cluster and networking; afterwards run `aws eks update-kubeconfig --name <cluster>` to target the new cluster.


When you are ready to present a managed-cloud deployment, use the Terraform module under `terraform/` to create the AWS networking and EKS resources. This step is not required for a free demonstration and will incur charges in your AWS account. Review the [Terraform README](terraform/README.md) for full instructions.

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
