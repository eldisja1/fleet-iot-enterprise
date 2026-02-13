# System Architecture – Fleet IoT Enterprise Simulation

## 1. Document Purpose
This document describes the final system architecture of the **Fleet IoT Enterprise Simulation** project.
The architecture is designed to demonstrate IoT system design, service separation, and private network (APN-like) simulation using containerized services.

This document serves as a **final architectural reference** for implementation.

---

## 2. Design Principles
- Simple yet enterprise-oriented design
- Single responsibility for each service
- Easy to explain during technical interviews
- Cloud-agnostic architecture
- Focus on architecture and data flow rather than UI or production optimizations

---

## 3. System Components

### 3.1 Device Simulator
**Location:** `simulator/`

**Role:**
Simulates multiple IoT devices sending telemetry data.

**Characteristics:**
- Implemented in Python
- Publishes JSON-formatted telemetry data
- Communicates exclusively via MQTT
- No access to HTTP APIs or databases

---

### 3.2 MQTT Broker

**Role:**
Acts as the central message broker between devices and backend services.

**Characteristics:**
- Uses Mosquitto
- Runs as a containerized service
- Accessible only within the internal network

**Topic Structure:**
```
fleet/{device_id}/telemetry
```

The MQTT Broker functions as the **entry point**, conceptually similar to an APN in cellular IoT systems.

---

### 3.3 Backend – MQTT Consumer Service
**Location:** `backend/mqtt/`

**Role:**
Consumes and processes telemetry data from the MQTT Broker.

**Responsibilities:**
- Subscribe to MQTT topics
- Validate telemetry payloads
- Log events
- Persist data into the database

This service does **not** expose HTTP endpoints.

---

### 3.4 Backend – API Service
**Location:** `backend/api/`

**Role:**
Provides data access through REST APIs.

**Characteristics:**
- Built with FastAPI (Python)
- Reads data from the database
- Exposes endpoints such as:
  - `/health`
  - `/devices`
  - `/telemetry`

The API Service is the **only component optionally exposed to external clients**.

---

### 3.5 Database

**Role:**
Provides persistent storage for device and telemetry data.

**Characteristics:**
- Uses PostgreSQL
- Accessible only by backend services
- Not directly accessible by device simulators

---

## 4. Network Architecture (APN Simulation)

All services run within a single internal Docker network:

```
apn_net (internal)
```

**Communication rules:**
- Device Simulator → MQTT Broker only
- MQTT Consumer → Database
- API Service → Database
- Devices have no direct access to backend services or the database

This setup simulates a **private APN-like network**, isolating IoT traffic from public access.

---

## 5. Data Flow

```
[Device Simulator]
        |
      MQTT
        |
   [MQTT Broker]
        |
   [MQTT Consumer]
        |
    [Database]
        |
   [API Service]
        |
Optional Client / Dashboard
```

The dashboard or client component is **optional** and not part of the core system.

---

## 6. Deployment Model
- Managed using Docker Compose
- All services run as containers
- No dependency on a specific cloud provider
- Fully executable in a local environment

---

## 7. System Limitations
- No real cellular APN implementation
- No SIM, IMSI, or telecom-level authentication
- No high availability or auto-scaling
- Focused on architectural concepts rather than production hardening

---

## 8. Status

This architecture is considered **final**.
Subsequent work focuses on implementation, not architectural redesign.

