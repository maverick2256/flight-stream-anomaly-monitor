variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "raw_bucket_name" {
  type    = string
  default = "replace-me-flight-telemetry-raw"
}

variable "kinesis_stream_name" {
  type    = string
  default = "flight-telemetry-stream"
}
