provider "aws" {
  region = "us-west-2"
}

resource "aws_eks_cluster" "llm_cluster" {
  name     = "llm-doc-processor-cluster"
  role_arn = var.eks_role_arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_ecs_cluster" "llm_ecs" {
  name = "llm-doc-processor-ecs"
}

// Additional resources: load balancers, Fargate tasks, RDS, S3 buckets