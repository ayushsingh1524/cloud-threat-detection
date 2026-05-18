resource "aws_iam_role" "snowflake_ingestion" {
  name = "snowflake_cloudtrail_ingestion_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "*" # In production, this should be restricted to the Snowflake account AWS ARN
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "snowflake_s3_access" {
  name = "snowflake_s3_access_policy"
  role = aws_iam_role.snowflake_ingestion.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion"
        ]
        Resource = "arn:aws:s3:::cloud-threat-detection-cloudtrail-logs/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = "arn:aws:s3:::cloud-threat-detection-cloudtrail-logs"
      }
    ]
  })
}

output "snowflake_ingestion_role_arn" {
  value = aws_iam_role.snowflake_ingestion.arn
}
