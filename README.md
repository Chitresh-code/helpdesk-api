## Running the Project with Docker

This project is containerized using Docker and Docker Compose for a reproducible development and deployment environment. Below are the instructions and details specific to this project:

### Requirements & Versions
- **Python Version:** 3.13 (as specified in the Dockerfile)
- **Dependency Management:** Uses `uv` for creating a virtual environment and installing dependencies from `requirements.txt` and `pyproject.toml`.

### Environment Variables
- The Docker Compose file is set up to optionally use a `.env` file (see the commented `env_file: ./.env` line). If your application requires environment variables, place them in a `.env` file at the project root and uncomment this line in `docker-compose.yml`.

### Build and Run Instructions
1. **(Optional) Prepare your `.env` file:**
   - If your application requires environment variables, create a `.env` file in the project root.
2. **Build and start the service:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the `python-uv` service.

### Service Details
- **Service Name:** `python-uv`
- **Exposed Port:** `8000` (host) → `8000` (container)
- **Entrypoint:** Runs `uvicorn app.main:app` on port 8000
- **User:** Runs as a non-root user for improved security

### Special Configuration
- The project uses a multi-stage build for a minimal runtime image and improved security (non-root user).
- The `uv` tool is used for dependency management and virtual environment creation, which is less common than `pip` or `poetry`.
- The application code is located in the `app/` directory and is served via Uvicorn.
- The Docker Compose file defines a custom bridge network named `backend` for service isolation and extensibility.

---

_If you add additional services (e.g., databases), update the `docker-compose.yml` and these instructions accordingly._