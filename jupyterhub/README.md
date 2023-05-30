
This directory contains Docker and Docker Compose configurations for running a JupyterHub server.

### Prerequisites
- Docker installed. [Installation Instructions](https://docs.docker.com/get-docker/)
- Docker Compose installed. [Installation Instructions](https://docs.docker.com/compose/install/)

### Steps to deploy
1. Navigate to the `jupyterhub` directory.
2. Build the Docker images with the command:
    ```
    sudo docker-compose build
    sudo docker build -t notebook_image Dockerfile.notebook_image
    ```
3. Start the JupyterHub server:
    ```
    sudo docker-compose up -d
    ```
   The JupyterHub server is now running and accessible at `http://localhost:8000` or `http://[your-server-ip]:8000` if you're deploying on a remote server.
4. To stop the JupyterHub server and remove the containers, run:
    ```
    sudo docker-compose down
    ```
5. To view the logs of the JupyterHub server, run:
    ```
    sudo docker-compose logs
    ```
In case the JupyterHub was started via the Terraform setup, you can find the JupyterHub running on the public IP of the created instance, which is displayed as an output of the Terraform script. The JupyterHub and custom notebook Docker images are built during the instance startup, and the JupyterHub service is started immediately afterward. The JupyterHub configurations can