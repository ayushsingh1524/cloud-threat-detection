variable "sns_topic_name" {
  type = string
}

resource "aws_sns_topic" "threat_alerts" {
  name = var.sns_topic_name
}

resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.threat_alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowPublishFromPipeline"
        Effect    = "Allow"
        Principal = {
          AWS = "*" # In production, restrict to the IAM role of the alert generation service
        }
        Action    = "sns:Publish"
        Resource  = aws_sns_topic.threat_alerts.arn
      }
    ]
  })
}

output "sns_topic_arn" {
  value = aws_sns_topic.threat_alerts.arn
}
