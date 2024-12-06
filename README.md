# HealthSync

**HealthSync** is a Distributed Healthcare Data Integration and Query System designed to address fragmented healthcare data. It seamlessly integrates patient records, medical imaging, and laboratory results from multiple databases (two MongoDB and one SQL) into a unified global schema for efficient querying, management, and analysis.

---

## Features

- **Data Synchronization**:
  - Integrates patient records, medical imaging, and lab results from heterogeneous sources (two MongoDB databases and one MySQL database).
- **Schema Mapping**:
  - Advanced ETL process with schema matching ensures consistent and accurate data representation in the global schema.
- **Global Schema**:
  - A unified schema consolidates healthcare data for comprehensive management and accessibility.
- **Dynamic Querying**:
  - Allows querying of patients based on names, severity levels, or associated doctors.
- **Role-Based Interfaces**:
  - Separate interfaces for Doctors, Radiologists, and Patients.
- **Statistics Dashboard**:
  - Provides real-time statistics on total patients, total doctors, and the distribution of patients based on severity (e.g., Severe, Mild, Healthy).
- **File Management**:
  - Imaging data stored on Google Drive with dynamically generated download links.

---

## Technologies Used

- **Backend**:
  - Python (Django Framework)
  - MySQL (Relational Database)
  - MongoDB (Non-relational Databases for imaging and lab results)
- **ETL Process**:
  - Schema matching and transformation using Python to integrate disparate database structures.
- **Frontend**:
  - HTML, CSS, JavaScript
- **Other Tools**:
  - Google Drive API for imaging data storage and retrieval.
  - Git for version control.

---

## Global Schema Mapping and Integration

### Databases:

1. **MongoDB Database 1**:
   - Imaging data including patient imageid ,imaging types, dates, and descriptions , image url.
2. **MongoDB Database 2**:
   - Laboratory results including test names, results, and doctor comments.
3. **MySQL Database**:
   - Core patient records such as demographics, contact details, and severity levels.

### ETL Process:

1. **Extract**:
   - Patient data from MySQL.
   - Imaging and lab data from MongoDB collections.
2. **Transform**:
   - Schema mapping ensures that diverse formats align with the unified global schema.
   - Handles string-to-dictionary transformations for structured fields like lab test results.
3. **Load**:
   - Populates the `GlobalPatientSchema` in the unified database.

---

## Installation

### Prerequisites

- Python 3.x
- Git
- MySQL and MongoDB installed locally or accessible remotely

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/HealthSync.git
   cd HealthSync
