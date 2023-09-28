# ANAVARA HEALTH API

This is a coding assessment which implements a health api for managing medical reports of patients.

## Setup
1. In order to setup this project for contribution ensure you have the following installaed:
    a. docker 
    b. docker-compose
2. To Setup for for local development run the following command:
    ```bash
    make dev-setup
    ```
3. Create .env file using .env.example file properties
4. To start up the dev server run the following command:
    ```bash
    make dev-server
    ```
5. To run tests run the following command:
    ```bash
    make test
    ```

## DOCUMENTATION
Once dev server is started, you can access the api document at the routes
1. Swagger: /api/schema/swagger-ui/#/
2. Redoc: /api/schema/redoc/

Documentation on the following concepts:
1. Security: [Security Approach](/docs/security.md)
2. Infrastructure: [Infrastructure Approach](/docs/infrastructure.md)