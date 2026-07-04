-- Azure SQL Database script to create a simple healthcare star schema
-- Run this script in your target Azure SQL Database.

USE [master];
GO

-- Optional: create a dedicated schema for analytics
-- CREATE SCHEMA analytics;
-- GO

IF OBJECT_ID('dbo.appointments', 'U') IS NOT NULL DROP TABLE dbo.appointments;
IF OBJECT_ID('dbo.insurance', 'U') IS NOT NULL DROP TABLE dbo.insurance;
IF OBJECT_ID('dbo.patient_demographics', 'U') IS NOT NULL DROP TABLE dbo.patient_demographics;
IF OBJECT_ID('dbo.providers', 'U') IS NOT NULL DROP TABLE dbo.providers;
IF OBJECT_ID('dbo.location', 'U') IS NOT NULL DROP TABLE dbo.location;
IF OBJECT_ID('dbo.appt_resource', 'U') IS NOT NULL DROP TABLE dbo.appt_resource;
IF OBJECT_ID('dbo.appt_events', 'U') IS NOT NULL DROP TABLE dbo.appt_events;
IF OBJECT_ID('dbo.payer', 'U') IS NOT NULL DROP TABLE dbo.payer;
IF OBJECT_ID('dbo.race', 'U') IS NOT NULL DROP TABLE dbo.race;
IF OBJECT_ID('dbo.ethnicity', 'U') IS NOT NULL DROP TABLE dbo.ethnicity;
IF OBJECT_ID('dbo.relationship', 'U') IS NOT NULL DROP TABLE dbo.relationship;
GO

CREATE TABLE dbo.race (
    race_id INT PRIMARY KEY,
    race_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.ethnicity (
    ethnicity_id INT PRIMARY KEY,
    ethnicity_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.relationship (
    relationship_id INT PRIMARY KEY,
    relationship_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.payer (
    payer_id INT PRIMARY KEY,
    payer_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.location (
    location_id INT PRIMARY KEY,
    city NVARCHAR(100) NOT NULL,
    state_code NVARCHAR(10) NOT NULL,
    location_name NVARCHAR(200) NOT NULL
);

CREATE TABLE dbo.appt_resource (
    resource_id INT PRIMARY KEY,
    resource_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.appt_events (
    event_id INT PRIMARY KEY,
    event_name NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.providers (
    provider_id INT PRIMARY KEY,
    provider_name NVARCHAR(200) NOT NULL
);

CREATE TABLE dbo.patient_demographics (
    patient_id NVARCHAR(20) PRIMARY KEY,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    gender NVARCHAR(20) NULL,
    date_of_birth DATE NULL,
    age INT NULL,
    race_id INT NOT NULL,
    ethnicity_id INT NOT NULL,
    relationship_id INT NOT NULL,
    location_id INT NOT NULL,
    zip_code NVARCHAR(20) NULL,
    phone NVARCHAR(50) NULL,
    email NVARCHAR(200) NULL,
    created_date DATE NULL,
    CONSTRAINT FK_patient_race FOREIGN KEY (race_id) REFERENCES dbo.race(race_id),
    CONSTRAINT FK_patient_ethnicity FOREIGN KEY (ethnicity_id) REFERENCES dbo.ethnicity(ethnicity_id),
    CONSTRAINT FK_patient_relationship FOREIGN KEY (relationship_id) REFERENCES dbo.relationship(relationship_id),
    CONSTRAINT FK_patient_location FOREIGN KEY (location_id) REFERENCES dbo.location(location_id)
);

CREATE TABLE dbo.insurance (
    insurance_id NVARCHAR(20) PRIMARY KEY,
    patient_id NVARCHAR(20) NOT NULL,
    payer_id INT NOT NULL,
    plan_name NVARCHAR(200) NOT NULL,
    plan_type NVARCHAR(50) NULL,
    coverage_level NVARCHAR(50) NULL,
    deductible DECIMAL(10,2) NULL,
    copay DECIMAL(10,2) NULL,
    effective_date DATE NULL,
    termination_date DATE NULL,
    network_type NVARCHAR(50) NULL,
    state NVARCHAR(20) NULL,
    CONSTRAINT FK_insurance_patient FOREIGN KEY (patient_id) REFERENCES dbo.patient_demographics(patient_id),
    CONSTRAINT FK_insurance_payer FOREIGN KEY (payer_id) REFERENCES dbo.payer(payer_id)
);

CREATE TABLE dbo.appointments (
    appointment_id INT PRIMARY KEY,
    patient_id NVARCHAR(20) NOT NULL,
    insurance_id NVARCHAR(20) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time NVARCHAR(10) NOT NULL,
    appointment_type NVARCHAR(100) NULL,
    department NVARCHAR(100) NULL,
    provider_id INT NOT NULL,
    location_id INT NOT NULL,
    resource_id INT NOT NULL,
    event_id INT NOT NULL,
    status NVARCHAR(50) NULL,
    duration_minutes INT NULL,
    copay_amount DECIMAL(10,2) NULL,
    CONSTRAINT FK_appointment_patient FOREIGN KEY (patient_id) REFERENCES dbo.patient_demographics(patient_id),
    CONSTRAINT FK_appointment_insurance FOREIGN KEY (insurance_id) REFERENCES dbo.insurance(insurance_id),
    CONSTRAINT FK_appointment_provider FOREIGN KEY (provider_id) REFERENCES dbo.providers(provider_id),
    CONSTRAINT FK_appointment_location FOREIGN KEY (location_id) REFERENCES dbo.location(location_id),
    CONSTRAINT FK_appointment_resource FOREIGN KEY (resource_id) REFERENCES dbo.appt_resource(resource_id),
    CONSTRAINT FK_appointment_event FOREIGN KEY (event_id) REFERENCES dbo.appt_events(event_id)
);
GO

PRINT 'Healthcare star schema created successfully.';
GO
