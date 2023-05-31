This directory contains Terraform scripts for provisioning a GPU-accelerated compute instance on Google Cloud, that also starts a JupyterHub server during its setup.

### Prerequisites
- Terraform installed. [Installation Instructions](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- A Google Cloud project with necessary APIs enabled.
- Sufficient permissions to create and manage resources on Google Cloud.

### Steps to deploy
1. Navigate to the `terraform` directory.
2. Initialize the Terraform configuration with the command:
    ```
    terraform init
    ```
3. Plan the deployment and review the resources that will be created:
    ```
    terraform plan -var 'project=YOUR_PROJECT_ID'
    ```
   Replace `YOUR_PROJECT_ID` with your Google Cloud project ID.
4. Apply the configuration to create the resources:
    ```
    terraform apply -var 'project=YOUR_PROJECT_ID'
    ```
   Confirm the deployment by typing `yes` when prompted.
5. Once the deployment is successful, Terraform will output the public IP address of the created instance, `[your-server-ip]`. Use this IP address to access your JupyterHub.at `http://[your-server-ip]:8000`.  Note that the created instance will appear quickly but it might take ~10 minutes for the JupyterHub to start (several Docker images need to be created).
6. To clean up the resources when you're done, run:
    ```
    terraform destroy -var 'project=YOUR_PROJECT_ID'
    ```
   Confirm the destruction by typing `yes` when prompted.
Remember to replace `YOUR_PROJECT_ID` with your actual Google Cloud project ID in the Terraform commands. The above instructions assume that Docker daemon is accessible via `sudo`. If your user is in the Docker group and can run Docker commands without `sudo`, you can remove `sudo` from the commands.

The Terraform script in this project will create an instance with the specified configurations. During startup, the `start-up-script.sh` script will be executed. This script installs necessary drivers and software, including Docker and Nvidia-docker2 for GPU support. The script then clones the `video_parser` repository, builds Docker images for JupyterHub and a custom notebook from the Dockerfiles provided, and starts the JupyterHub service using Docker Compose.
