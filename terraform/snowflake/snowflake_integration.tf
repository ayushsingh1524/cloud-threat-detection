terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.85"
    }
  }
}

variable "aws_iam_role_arn" {
  type = string
}

resource "snowflake_database" "threat_analytics" {
  name = "THREAT_ANALYTICS"
}

resource "snowflake_schema" "cloudtrail" {
  database = snowflake_database.threat_analytics.name
  name     = "CLOUDTRAIL"
}

resource "snowflake_storage_integration" "aws_s3" {
  name    = "AWS_S3_INTEGRATION"
  type    = "EXTERNAL_STAGE"
  enabled = true

  storage_allowed_locations = ["s3://cloud-threat-detection-cloudtrail-logs/"]
  storage_provider         = "S3"
  storage_aws_role_arn     = var.aws_iam_role_arn
}

resource "snowflake_stage" "cloudtrail_stage" {
  name                = "CLOUDTRAIL_STAGE"
  url                 = "s3://cloud-threat-detection-cloudtrail-logs/"
  database            = snowflake_database.threat_analytics.name
  schema              = snowflake_schema.cloudtrail.name
  storage_integration = snowflake_storage_integration.aws_s3.name
}

resource "snowflake_table" "cloudtrail_logs_raw" {
  database = snowflake_database.threat_analytics.name
  schema   = snowflake_schema.cloudtrail.name
  name     = "CLOUDTRAIL_LOGS_RAW"

  column {
    name = "RAW_EVENT"
    type = "VARIANT"
  }
}

resource "snowflake_table" "cloudtrail_logs_normalized" {
  database = snowflake_database.threat_analytics.name
  schema   = snowflake_schema.cloudtrail.name
  name     = "CLOUDTRAIL_LOGS_NORMALIZED"

  column {
    name = "EVENT_TIME"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "SOURCE_IP"
    type = "VARCHAR"
  }
  column {
    name = "USER_IDENTITY"
    type = "VARCHAR"
  }
  column {
    name = "AWS_REGION"
    type = "VARCHAR"
  }
  column {
    name = "EVENT_NAME"
    type = "VARCHAR"
  }
  column {
    name = "RESOURCE"
    type = "VARCHAR"
  }
  column {
    name = "SEVERITY"
    type = "VARCHAR"
  }
}
