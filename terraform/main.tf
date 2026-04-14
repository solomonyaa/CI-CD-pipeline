terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "ci-cd-vpc"
  cidr = "10.0.0.0/16"
  azs            = ["us-east-1a"]
  public_subnets = ["10.0.1.0/24"]
  tags = {
    Owner       = "Solomon"
    Environment = "CI/CD"
  }
}

module "the-web-comp" {
  source    = "./webcomp"
  vpc_id    = module.vpc.vpc_id
  subnet_id = module.vpc.public_subnets[0]
}

output "ec2_public_ip" {
  value = module.the-web-comp.ec2_public_ip
}