terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
  }

  required_version = ">= 1.0.0"
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

resource "google_compute_instance" "jenkins" {
  name         = "jenkins-instance2"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
      size  = 25
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    echo "Startup script executed" > /tmp/startup_script_status.txt

    # Update package list and install Java and Jenkins
    {
      sudo apt update
      sudo apt install -y openjdk-17-jre-headless
      java -version
      sudo apt install -y default-jdk
      javac -version

      # Add Jenkins repository and key
      curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc
      echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list

      # Install Jenkins
      sudo apt update
      sudo apt install -y jenkins

      # Start Jenkins service and check status
      sudo systemctl start jenkins
      sudo systemctl enable jenkins
      sudo systemctl status jenkins > /var/log/startup-script.log

    } >> /var/log/startup-script.log 2>&1

    echo "Startup script completed" >> /tmp/startup_script_status.txt
  EOT

  tags = ["jenkins"]
}

resource "google_compute_firewall" "default" {
  name    = "allow-jenkins"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080"]
  }

  target_tags = ["jenkins"]

  source_ranges = ["0.0.0.0/0"]
}
