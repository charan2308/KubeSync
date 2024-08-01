# Kubesync

**Kubesync** is an automated backup service designed to securely back up selected directories and their subdirectories to Google Drive. This service runs every day at midnight by default, but both the backup time and the target directory can be customized to fit your needs.

## Features

- **Automated Backups**: Schedules daily backups to Google Drive at midnight.
- **Customizable**: Easily change the backup time and target directory.
- **Secure Authentication**: Uses OAuth2 for secure access to Google Drive.
- **Containerized**: Runs seamlessly in a Docker container.
- **Scalable**: Managed with Kubernetes and CronJob for efficient scaling and reliability.

## Technology Stack

- **Python**: Core programming language for the application.
- **Docker**: Containerization for easy deployment and scaling.
- **Kubernetes (K8s)**: Orchestration platform for managing containers.
- **CronJob**: Scheduling tasks within Kubernetes.
- **Google Drive API**: Interface for interacting with Google Drive.
- **OAuth2**: Secure authentication for Google Drive access.

## Installation

### Prerequisites

- Docker
- Kubernetes cluster
- Google Cloud project with Drive API enabled
- OAuth2 credentials (client ID and secret)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/kubesync.git
   cd kubesync
   ```
2. **Start kubernetes service**
    ```sh
    minikube start
    ```
3. **Choose backup folder**
    </br>Choose the backup folder using the edityaml.py script. This script takes care of creating the docker file with the required folders.
    ```sh 
    python3 edityaml.py
    ```
4. **Start Cronjob**
     ```sh
    kubectl apply -f final_cron.yaml
    ```

### Stopping the service
```sh
kubectl delete cronjob backup3-cronjob
```



## License
This project is licensed under the **MIT** License. See the LICENSE file for details.