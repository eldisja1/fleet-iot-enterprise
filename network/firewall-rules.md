# Firewall Rules

## Overview

This document defines the firewall configuration and network exposure policy for the Fleet IoT Enterprise project. It describes which ports are allowed, which services are exposed, and how access should be restricted in development and production environments.

The goal is to minimize attack surface while maintaining required connectivity between services.

---

## Network Architecture

All services communicate through an internal Docker bridge network:

- Network name: `apn_net`

Internal communication between containers does not require exposed host ports unless external access is necessary.

---

## Port Exposure Policy

### 1. MQTT Broker

- Service: Eclipse Mosquitto
- Port: 1883
- Protocol: TCP
- Purpose: Device-to-broker communication

#### Development

- Port 1883 may be exposed to localhost.
- Access should be limited to trusted internal networks.

#### Production

- Do not expose 1883 publicly without authentication.
- Prefer TLS-secured MQTT on port 8883.
- Restrict inbound access to known device IP ranges using firewall rules or cloud security groups.

---

### 2. PostgreSQL Database

- Port: 5432
- Protocol: TCP
- Purpose: Backend data storage

#### Development

- May be exposed locally for debugging.

#### Production

- Must not be publicly accessible.
- Remove `ports` mapping in Docker Compose.
- Allow access only from internal services (MQTT consumer, API service).
- Deploy inside a private subnet if using cloud infrastructure.

---

### 3. API Service (Planned)

- Port: 8000 (example)
- Protocol: TCP
- Purpose: Application backend

#### Production

- Expose only through HTTPS (port 443).
- Use reverse proxy (e.g., Nginx) for TLS termination.
- Block direct public access to internal service ports.

---

### 4. Web Dashboard (Planned)

- Port: 3000 (example)
- Protocol: TCP
- Purpose: Web interface

#### Production

- Serve behind reverse proxy.
- Expose only via HTTPS (443).
- Do not expose development server directly to the internet.

---

## Linux Firewall Example (UFW)

Allow SSH:

```bash
sudo ufw allow 22/tcp
