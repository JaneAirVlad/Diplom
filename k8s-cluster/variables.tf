variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  default     = "europe-west1"
  description = "Region for GCP resources"
}

variable "cluster_name" {
  type        = string
  default     = "diploma-k8s-cluster"
  description = "Имя Kubernetes кластера"
}
