CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'offline',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telemetry (
    id BIGSERIAL PRIMARY KEY,
    device_id UUID NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_device
        FOREIGN KEY(device_id)
        REFERENCES devices(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_telemetry_device_time
ON telemetry (device_id, created_at DESC);
