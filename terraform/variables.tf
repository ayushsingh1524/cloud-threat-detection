variable "aws_region" {
  description = "AWS region for the pipeline"
  type        = string
  default     = "us-east-1"
}

variable "cloudtrail_bucket_name" {
  description = "S3 bucket for CloudTrail logs"
  type        = string
  default     = "cloud-threat-detection-cloudtrail-logs"
}

variable "sns_alert_topic_name" {
  description = "SNS topic for threat alerts"
  type        = string
  default     = "cloud-threat-alerts"
}

variable "snowflake_account" {
  description = "Snowflake account identifier"
  type        = string
}

variable "snowflake_user" {
  description = "Snowflake username"
  type        = string
}

variable "snowflake_password" {
  description = "Snowflake password"
  type        = string
  sensitive   = true
}

variable "snowflake_role" {
  description = "Snowflake role"
  type        = string
  default     = "ACCOUNTADMIN"
}
