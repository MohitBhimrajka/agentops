###############################################################################
# main.tf  ──  Terraform bootstrap for AgentOps (DevSecOps demo)
# Creates: API enablement, Artifact Registry repo (with scanning ON),
#          BigQuery dataset, runner Service Account + IAM, Secret placeholders
###############################################################################

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.38.0"                     # same as `terraform init` output
    }
  }
}

############################   INPUT VARIABLES   ##############################
variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Primary region (e.g. us-central1)"
  type        = string
  default     = "us-central1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ------------------------ ENABLE GOOGLE CLOUD APIS ------------------------
locals {
  base_services = [
    # Core GCP
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "secretmanager.googleapis.com",
    # Gen-AI / Vertex
    "aiplatform.googleapis.com",          # Vertex AI (includes Agent Engine)  :contentReference[oaicite:8]{index=8}
    # Optional: Gemini REST endpoint if you plan to call it directly
    # "generativelanguage.googleapis.com",   # Gemini API  :contentReference[oaicite:9]{index=9}
  ]
}

resource "google_project_service" "services" {
  for_each = toset(local.base_services)
  project  = var.project_id
  service  = each.value
  disable_dependent_services = false
}
# google_project_service pattern from official guide :contentReference[oaicite:0]{index=0}

#########################  ARTIFACT REGISTRY REPO  ############################
resource "google_artifact_registry_repository" "docker_repo" {
  project       = var.project_id
  location      = var.region
  repository_id = "agentops"
  description   = "Docker images for AgentOps pipelines"
  format        = "DOCKER"

  # Nested block required for provider v5.17+ / v6.x
  vulnerability_scanning_config {
    enablement_config = "INHERITED"
  }
}
# vulnerability_scanning_config syntax in provider docs :contentReference[oaicite:1]{index=1}
# Recent provider issue notes the older root-level attr was removed :contentReference[oaicite:2]{index=2}

###########################  BIGQUERY DATASET  ################################
resource "google_bigquery_dataset" "audit" {
  dataset_id                 = "agentops_audit"
  friendly_name              = "AgentOps Audit Logs"
  location                   = var.region
  delete_contents_on_destroy = true
}
# BigQuery dataset resource example :contentReference[oaicite:3]{index=3}

######################  SERVICE ACCOUNT + IAM ROLES  ##########################
resource "google_service_account" "runner" {
  account_id   = "agentops-runner"
  display_name = "AgentOps pipeline runner"
}
# google_service_account usage :contentReference[oaicite:4]{index=4}

locals {
  runner_roles = [
    "roles/cloudbuild.builds.editor",   # submit builds
    "roles/run.developer",              # deploy Cloud Run
    "roles/artifactregistry.writer",    # push images
    "roles/bigquery.dataEditor",        # write audit logs
    "roles/secretmanager.secretAccessor"
  ]
}

resource "google_project_iam_member" "runner_bindings" {
  for_each = toset(local.runner_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${google_service_account.runner.email}"
}
# IAM-member pattern from registry docs :contentReference[oaicite:5]{index=5}

###########################  SECRET MANAGER  ##################################
resource "google_secret_manager_secret" "gh_token" {
  secret_id = "GITHUB_TOKEN"

  replication {
    auto {}          # new syntax replaces deprecated `automatic = true`
  }
}

resource "google_secret_manager_secret" "slack_webhook" {
  secret_id = "SLACK_WEBHOOK"

  replication {
    auto {}
  }
}
# Empty `auto {}` block per current Secret Manager docs :contentReference[oaicite:6]{index=6}
# Removal of the old 'automatic' arg discussed in provider issue :contentReference[oaicite:7]{index=7}

###############################  OUTPUTS  #####################################
output "artifact_repo" {
  description = "Artifact Registry repository resource ID"
  value       = google_artifact_registry_repository.docker_repo.id
}

output "runner_sa_email" {
  description = "Service Account email for pipeline runners"
  value       = google_service_account.runner.email
}

output "bigquery_dataset_id" {
  description = "BigQuery dataset ID for audit logs"
  value       = google_bigquery_dataset.audit.id
}
