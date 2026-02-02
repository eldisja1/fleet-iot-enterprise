# Enterprise Fleet Tracking IoT Platform with Private APN


## Overview
This project is a simulation of an enterprise-grade IoT fleet system.
It demonstrates how multiple IoT devices communicate through an MQTT broker,
are processed by a backend service, and operate within a private network that
conceptually mimics an APN (Access Point Name) environment.

The project is designed as a portfolio to showcase system architecture,
network isolation, and troubleshooting practices in IoT systems.

## Architecture Components
- **Device Simulator**  
  Simulates multiple IoT devices publishing telemetry data via MQTT.

- **MQTT Broker**  
  Acts as the message broker for device-to-backend communication.

- **Backend Services**
  - MQTT Consumer
  - REST API for data access and monitoring

- **Network (APN Simulation)**  
  Logical simulation of a private APN-like network using Docker networking.

- **Troubleshooting Documentation**  
  Common failure scenarios and decision trees for debugging IoT systems.

## Key Goals
- Demonstrate MQTT-based communication
- Simulate APN-like network isolation
- Apply containerized microservice principles
- Provide clear documentation and troubleshooting guides

## Scope & Limitations
This project simulates APN behavior at a network and routing level.
It does **not** interact with real cellular networks or telecom providers.

## Technology Stack
- MQTT (Mosquitto)
- Docker & Docker Compose
- Backend Service (Node.js or Python)
- Python-based Device Simulator

## Status
Work in progress — developed incrementally within a limited timeframe.

## Documentation
- [System Architecture](docs/architecture.md)
