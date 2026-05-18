terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.85"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "snowflake" {
  account  = var.snowflake_account
  user     = var.snowflake_user
  password = var.snowflake_password
  role     = var.snowflake_role
}

module "cloudtrail" {
  source = "./cloudtrail"
  bucket_name = var.cloudtrail_bucket_name
}

module "iam" {
  source = "./iam"
}

module "snowflake_integration" {
  source = "./snowflake"
  aws_iam_role_arn = module.iam.snowflake_ingestion_role_arn
}

module "monitoring" {
  source = "./monitoring"
  sns_topic_name = var.sns_alert_topic_name
}
