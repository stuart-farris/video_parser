provider "google" {
  project = var.project
  region  = "us-central1"
  zone    = "us-central1-a"
}

variable "project" {
  description = "The ID of the project to apply this configuration to"
}

resource "google_compute_instance" "hpc-instance-gpu" {
  count        = 1
  name         = "hpc-instance-gpu"
  machine_type = "n1-standard-4" // 1 CPU 16 Gig of RAM
  zone         = "us-central1-a"
  tags         = ["http"]
  boot_disk {
    initialize_params {
      # image = "ubuntu-os-cloud/ubuntu-2004-lts"
      image = "deeplearning-platform-release/pytorch-latest-gpu-v20230501-ubuntu-2004"
      size  = 100 // 100GB of storage
    }
  }
  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static_ip.address
    }
  }
  guest_accelerator {
    type  = "nvidia-tesla-v100" // Type of GPU attahced
    count = 1                   // Num of GPU attached
  }
  scheduling {
    on_host_maintenance = "TERMINATE" // Need to terminate GPU on maintenance
  }
  metadata_startup_script = file("start-up-script.sh") // Here we will add the env setup
}
resource "google_compute_firewall" "allow_jupyterhub_gpu" {
  name    = "allow-jupyterhub-gpu"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }

  source_ranges = ["0.0.0.0/0"]
}

output "hpc_instance_gpu_ip" {
  value = google_compute_instance.hpc-instance-gpu[0].network_interface[0].access_config[0].nat_ip
  description = "The IP address of the hpc-instance-gpu"
}