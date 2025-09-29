# AWS Infrastructure Automation

This Terraform module provisions the core infrastructure required to run the Parameta DevOps MVP in AWS:

- A dedicated VPC with public and private subnets across three Availability Zones.
- An EKS cluster with a managed node group sized for test and production workloads.
- A Kubernetes provider configuration ready to apply platform add-ons (e.g., monitoring stack).

> **Cost notice:** Running `terraform apply` will create chargeable AWS resources. The main walkthrough in the repository shows how to exercise the MVP entirely for free using KIND; only invoke this module when you intentionally want to demo the managed-cloud footprint.

## Usage

```bash
terraform init
terraform plan -var="cluster_name=parameta-devops-mvp" -var="aws_region=us-east-1"
terraform apply
```

> **Provider compatibility:** The AWS provider is pinned to `< 6.0` because version 6 removed launch template attributes that the upstream EKS module still references. If you previously initialized this directory and see errors such as `elastic_gpu_specifications are not expected here`, delete `.terraform.lock.hcl` (and optionally the `.terraform/` directory) and rerun `terraform init -upgrade` so Terraform downloads a 5.x provider release.

The configuration is intentionally opinionated to satisfy the MVP requirements. Adjust the variables defined in `variables.tf` to customize CIDR ranges, instance types, and the Kubernetes version.
