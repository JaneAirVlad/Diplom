resource "google_container_cluster" "primary" {
  name                     = "diplom-cluster"
  location                 = var.region
  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false

  network    = "default"
  subnetwork = "default"

  ip_allocation_policy {}
}

resource "google_container_node_pool" "primary_nodes" {
  name     = "default-node-pool"
  location = var.region
  cluster  = google_container_cluster.primary.name

  node_count = 2

  node_config {
    preemptible    = true
    machine_type   = "e2-medium"
    disk_size_gb   = 50                    # Уменьшен размер диска
    disk_type      = "pd-standard"         # Используем HDD, не SSD
    oauth_scopes   = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
