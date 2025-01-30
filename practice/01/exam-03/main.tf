terraform{
    required_providers{
        google = {
            source = 'hashicorp/google'
            version = '5.6.0'
        }
    }
}

resource "google_compute_instance" "vm_with_docker" {
  name         = "docker-vm"
  machine_type = "n1-standard-1"
  zone         = "us-central1-a"


  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
  EOT
}
