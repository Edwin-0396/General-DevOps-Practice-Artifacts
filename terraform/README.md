# AWS Infrastructure Automation

This Terraform module provisions the core infrastructure required to run the Parameta DevOps MVP in AWS:

- A dedicated VPC with public and private subnets across three Availability Zones.
- An EKS cluster with a managed node group sized for test and production workloads.
- A Kubernetes provider configuration ready to apply platform add-ons (e.g., monitoring stack).

## Usage

```bash
terraform init
terraform plan -var="cluster_name=parameta-devops-mvp" -var="aws_region=us-east-1"
terraform apply
```

The configuration is intentionally opinionated to satisfy the MVP requirements. Adjust the variables defined in `variables.tf` to customize CIDR ranges, instance types, and the Kubernetes version.
