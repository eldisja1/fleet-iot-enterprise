# APN Network Simulation

## Purpose
This document describes how an APN (Access Point Name) concept is simulated
within this project using container networking.

The goal is to demonstrate architectural understanding of private IoT
connectivity without relying on real cellular infrastructure.

## What is an APN?
In real-world cellular IoT deployments, an APN:
- Provides a private network for devices
- Isolates device traffic from the public internet
- Allows controlled routing to backend services

## Simulation Approach
This project simulates APN behavior by:

- Using an isolated Docker network
- Restricting service exposure to internal containers only
- Allowing devices to communicate only with the MQTT broker
- Allowing backend services to consume data internally

All communication occurs inside a controlled virtual network.

## Traffic Flow
1. Device simulators publish data to the MQTT broker
2. MQTT broker forwards messages internally
3. Backend services consume messages and process data
4. External access is limited to backend APIs (if exposed)

## Security Assumptions
- Devices cannot directly access the database
- Devices cannot access backend APIs
- Public internet access is not required for device communication

## Limitations
- This is a logical simulation, not a real APN
- No SIM, IMSI, or telecom authentication is implemented
- Focus is on architectural concepts, not cellular protocols

## Value of This Simulation
Although simplified, this approach demonstrates:
- Network isolation principles
- Secure IoT traffic routing concepts
- Enterprise-style IoT system design thinking
