terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "telemetry_raw" {
  bucket = var.raw_bucket_name
}

resource "aws_kinesis_stream" "telemetry_stream" {
  name             = var.kinesis_stream_name
  shard_count      = 1
  retention_period = 24
}

resource "aws_sns_topic" "anomaly_alerts" {
  name = "flight-anomaly-alerts"
}

output "kinesis_stream_name" {
  value = aws_kinesis_stream.telemetry_stream.name
}
