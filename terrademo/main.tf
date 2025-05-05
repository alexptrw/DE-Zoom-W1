terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.33.0"
    }
  }
}

provider "google" {
    credentials =  "./keys/my-credentials.json"
  project = "terraform-demo-458815"
  region  = "europe-west2-a"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-458815-terrabucket"
  location      = "EU"
  force_destroy = true
  
  
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}