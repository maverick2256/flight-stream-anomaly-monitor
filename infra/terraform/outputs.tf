output "sns_topic_arn" {
  value       = aws_sns_topic.anomaly_alerts.arn
  description = "SNS topic ARN for anomaly alerts"
}
