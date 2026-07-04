from pathlib import Path
import csv
import random
from datetime import datetime, timedelta

root = Path(__file__).resolve().parent

random.seed(42)

first_names = [
    "Ava", "Liam", "Sophia", "Noah", "Olivia", "Ethan", "Emma", "Mason", "Charlotte", "Lucas",
    "Amelia", "Elijah", "Mia", "James", "Harper", "Benjamin", "Evelyn", "Alexander", "Abigail", "Henry"
]
last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]
genders = ["M", "F", "Other"]
race_values = ["White", "Black or African American", "Asian", "American Indian or Alaska Native", "Hispanic/Latino", "Other"]
ethnicity_values = ["Non-Hispanic", "Hispanic", "Not reported"]
relationship_values = ["Single", "Married", "Divorced", "Widowed"]
city_state_pairs = [
    ("Phoenix", "AZ"), ("Denver", "CO"), ("Austin", "TX"), ("Chicago", "IL"), ("Dallas", "TX"),
    ("Seattle", "WA"), ("Atlanta", "GA"), ("Miami", "FL"), ("Boston", "MA"), ("San Diego", "CA"),
    ("Los Angeles", "CA"), ("Houston", "TX"), ("New York", "NY"), ("San Francisco", "CA"), ("Philadelphia", "PA")
]
appointment_types = ["Routine Checkup", "Specialist Visit", "Vaccination", "Follow-up", "Physical Therapy", "Lab Review"]
departments = ["Primary Care", "Cardiology", "Pediatrics", "Orthopedics", "Dermatology", "Neurology"]
provider_names = [
    "Dr. Emily Carter", "Dr. Michael Nguyen", "Dr. Sarah Patel", "Dr. David Kim", "Dr. Jessica Brooks",
    "Dr. Robert Chen", "Dr. Linda Flores", "Dr. William Ortiz", "Dr. Anna Rivera", "Dr. Kevin Lewis"
]
statuses = ["Scheduled", "Completed", "No Show", "Cancelled"]
plan_types = ["HMO", "PPO", "EPO", "POS", "HDHP"]
coverage_levels = ["Basic", "Standard", "Premium", "Family", "Senior"]
network_types = ["National", "Regional", "Local"]
payer_names = ["BlueCross", "Aetna", "Cigna", "UnitedHealthcare", "Humana", "Kaiser"]
resource_names = ["Exam Room 1", "Exam Room 2", "Lab Station", "Imaging Suite", "Procedure Room", "Therapy Room"]
appointment_event_names = ["Booked", "Checked In", "Completed", "Cancelled", "Rescheduled"]


def random_date(start_year=1980, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days)
    return (start + timedelta(days=random_days)).date().isoformat()


def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


# Dimension tables
race_rows = [[idx + 1, name] for idx, name in enumerate(race_values)]
write_csv(root / "race.csv", ["race_id", "race_name"], race_rows)

ethnicity_rows = [[idx + 1, name] for idx, name in enumerate(ethnicity_values)]
write_csv(root / "ethnicity.csv", ["ethnicity_id", "ethnicity_name"], ethnicity_rows)

relationship_rows = [[idx + 1, name] for idx, name in enumerate(relationship_values)]
write_csv(root / "relationship.csv", ["relationship_id", "relationship_name"], relationship_rows)

payer_rows = [[idx + 1, name] for idx, name in enumerate(payer_names)]
write_csv(root / "payer.csv", ["payer_id", "payer_name"], payer_rows)

location_rows = []
for idx, (city, state) in enumerate(city_state_pairs, start=1):
    location_rows.append([idx, city, state, f"{city}, {state}"])
write_csv(root / "location.csv", ["location_id", "city", "state", "location_name"], location_rows)

resource_rows = [[idx + 1, name] for idx, name in enumerate(resource_names)]
write_csv(root / "appt_resource.csv", ["resource_id", "resource_name"], resource_rows)

event_rows = [[idx + 1, name] for idx, name in enumerate(appointment_event_names)]
write_csv(root / "appt_events.csv", ["event_id", "event_name"], event_rows)

provider_rows = [[idx + 1, name] for idx, name in enumerate(provider_names)]
write_csv(root / "providers.csv", ["provider_id", "provider_name"], provider_rows)

# Main dimension and fact files
patient_rows = []
for patient_id in range(1, 1001):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    gender = random.choice(genders)
    dob = random_date(1950, 2010)
    age = datetime.now().year - int(dob.split("-")[0])
    race_id = random.randint(1, len(race_values))
    ethnicity_id = random.randint(1, len(ethnicity_values))
    relationship_id = random.randint(1, len(relationship_values))
    location_id = random.randint(1, len(city_state_pairs))
    zip_code = f"{random.randint(10000, 99999)}"
    phone = f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    email = f"{first_name.lower()}.{last_name.lower()}{patient_id}@examplemail.com"
    created_date = random_date(2018, 2024)
    patient_rows.append([
        f"P{patient_id:04d}", first_name, last_name, gender, dob, age, race_id, ethnicity_id,
        relationship_id, location_id, zip_code, phone, email, created_date
    ])

patient_headers = [
    "patient_id", "first_name", "last_name", "gender", "date_of_birth", "age", "race_id",
    "ethnicity_id", "relationship_id", "location_id", "zip_code", "phone", "email", "created_date"
]
write_csv(root / "patient_demographics.csv", patient_headers, patient_rows)

insurance_rows = []
for patient_id in range(1, 1001):
    patient_key = f"P{patient_id:04d}"
    payer_id = random.randint(1, len(payer_names))
    plan_name = f"{payer_names[payer_id - 1]} {random.choice(plan_types)} {patient_id % 100:02d}"
    plan_type = random.choice(plan_types)
    coverage_level = random.choice(coverage_levels)
    deductible = round(random.uniform(300, 6000), 2)
    copay = round(random.uniform(10, 75), 2)
    effective_date = random_date(2015, 2023)
    termination_date = random_date(2024, 2026)
    network_type = random.choice(network_types)
    state = random.choice([x[1] for x in city_state_pairs])
    insurance_rows.append([
        f"INS{patient_id:04d}", patient_key, payer_id, plan_name, plan_type, coverage_level,
        deductible, copay, effective_date, termination_date, network_type, state
    ])

insurance_headers = [
    "insurance_id", "patient_id", "payer_id", "plan_name", "plan_type", "coverage_level", "deductible",
    "copay", "effective_date", "termination_date", "network_type", "state"
]
write_csv(root / "insurance.csv", insurance_headers, insurance_rows)

appointment_rows = []
for appointment_id in range(1, 1001):
    patient_id = f"P{random.randint(1, 1000):04d}"
    insurance_id = f"INS{int(patient_id[1:]):04d}"
    appointment_date = random_date(2023, 2025)
    appointment_time = f"{random.randint(7, 18):02d}:{random.choice(['00', '15', '30', '45'])}"
    appointment_type = random.choice(appointment_types)
    department = random.choice(departments)
    provider_id = random.randint(1, len(provider_names))
    location_id = random.randint(1, len(city_state_pairs))
    resource_id = random.randint(1, len(resource_names))
    event_id = random.randint(1, len(appointment_event_names))
    status = random.choice(statuses)
    duration_minutes = random.choice([15, 30, 45, 60, 90])
    copay_amount = round(random.uniform(0, 75), 2)
    appointment_rows.append([
        appointment_id, patient_id, insurance_id, appointment_date, appointment_time,
        appointment_type, department, provider_id, location_id, resource_id, event_id,
        status, duration_minutes, copay_amount
    ])

appointment_headers = [
    "appointment_id", "patient_id", "insurance_id", "appointment_date", "appointment_time",
    "appointment_type", "department", "provider_id", "location_id", "resource_id", "event_id",
    "status", "duration_minutes", "copay_amount"
]
write_csv(root / "appointments.csv", appointment_headers, appointment_rows)

print("Generated files:")
for name in [
    "patient_demographics.csv", "insurance.csv", "appointments.csv", "payer.csv", "appt_resource.csv",
    "appt_events.csv", "location.csv", "providers.csv", "race.csv", "ethnicity.csv", "relationship.csv"
]:
    print(f"- {name}")
