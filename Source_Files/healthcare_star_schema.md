# Healthcare Star Schema Sample

This sample uses a simple star schema for a U.S. healthcare analytics workload.

## Fact Table
- appointments.csv
  - appointment_id (surrogate key)
  - patient_id (foreign key to patient_demographics)
  - insurance_id (foreign key to insurance)
  - provider_id (foreign key to providers)
  - location_id (foreign key to location)
  - resource_id (foreign key to appt_resource)
  - event_id (foreign key to appt_events)
  - appointment_date / appointment_time
  - appointment_type, department, status, duration_minutes, copay_amount

## Dimension Tables
- patient_demographics.csv
  - patient_id
  - first_name, last_name, gender, date_of_birth, age
  - race_id, ethnicity_id, relationship_id, location_id
  - zip_code, phone, email

- insurance.csv
  - insurance_id
  - patient_id (patient-specific coverage)
  - payer_id (foreign key to payer)
  - plan_name, plan_type, coverage_level
  - deductible, copay, effective_date, termination_date, network_type, state

- payer.csv
- race.csv
- ethnicity.csv
- relationship.csv
- providers.csv
- location.csv
- appt_resource.csv
- appt_events.csv

This structure is suitable for ADF -> Databricks -> PySpark -> downstream analytics workflows.
