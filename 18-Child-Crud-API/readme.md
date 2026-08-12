# Child Management CRUD API

An asynchronous, high-performance RESTful API built with **FastAPI**, **Pydantic**, and Object-Oriented Programming (OOP) principles for managing child health and demographic records. This module serves as the primary data ingestion and management layer for the **NourishPak** platform.

---

## Table of Contents

1. [Understanding CRUD](#understanding-crud)
2. [Child Data Fields & Schema](#child-data-fields--schema)
3. [Data Validation Rules](#data-validation-rules)
4. [API Endpoints Overview](#api-endpoints-overview)
5. [HTTP Methods & Status Codes](#http-methods--status-codes)
6. [Sample Requests & Responses](#sample-requests--responses)

---

## Understanding CRUD

**CRUD** is an acronym for the four basic functions of persistent storage:

| Operation | Description | HTTP Method | API Endpoint Equivalent |
| :--- | :--- | :--- | :--- |
| **C**reate | Adds a new child record to the system | `POST` | `/children` |
| **R**ead | Retrieves existing child record(s) | `GET` | `/children` or `/children/{child_id}` |
| **U**pdate | Modifies an existing child record | `PUT` | `/children/{child_id}` |
| **D**elete | Removes a child record from the system | `DELETE` | `/children/{child_id}` |

---

## Child Data Fields & Schema

The `Child` entity represents a pediatric record monitored for growth and nutritional metrics.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `child_id` | `Integer` | Unique identification number for the child |
| `name` | `String` | Full name of the child |
| `age_months` | `Integer` | Age expressed in total months |
| `gender` | `String` | Biological sex (`Male` or `Female`) |
| `weight_kg` | `Float` | Current weight measured in kilograms |
| `height_cm` | `Float` | Current standing height or recumbent length in centimeters |

---

## Data Validation Rules

All requests are validated automatically using **Pydantic** models prior to hitting service logic:

- **`child_id`**: Must be an integer strictly **greater than 0** (`gt=0`).
- **`name`**: Must be a non-empty string (**minimum length of 1**).
- **`age_months`**: Must be a non-negative integer (**0 or greater**, `ge=0`).
- **`gender`**: Must be a non-empty string (`Male`, `Female`).
- **`weight_kg`**: Must be a float strictly **greater than 0** (`gt=0`).
- **`height_cm`**: Must be a float strictly **greater than 0** (`gt=0`).

---

## API Endpoints Overview

| Endpoint | Method | Action | Request Body | Success Code |
| :--- | :--- | :--- | :--- | :--- |
| `/children` | `POST` | Add a new child record | `Child` JSON | `201 Created` |
| `/children` | `GET` | Fetch list of all children | None | `200 OK` |
| `/children/{child_id}` | `GET` | Fetch details of a single child | None | `200 OK` |
| `/children/{child_id}` | `PUT` | Update child details | `Child` JSON | `200 OK` |
| `/children/{child_id}` | `DELETE` | Delete a child record | None | `200 OK` |

---

## HTTP Methods & Status Codes

### HTTP Methods Used
- **`POST`**: Used to submit data to create a new resource.
- **`GET`**: Used to retrieve resource data without modifying state.
- **`PUT`**: Used to replace or update an existing resource completely.
- **`DELETE`**: Used to remove a specific resource.

### Status Codes Explained
- **`200 OK`**: Standard successful HTTP response for read, update, and delete requests.
- **`201 Created`**: Resource was created successfully.
- **`400 Bad Request`**: Client-side error (e.g., trying to add a duplicate `child_id`).
- **`404 Not Found`**: The requested `child_id` does not exist in the service registry.
- **`422 Unprocessable Entity`**: Payload failed Pydantic schema validation rules.

---

## Sample Requests & Responses

### 1. Add Child (`POST /children`)
**Request:**
```json
POST /children
Content-Type: application/json

{
  "child_id": 101,
  "name": "Ahmed Ali",
  "age_months": 18,
  "gender": "Male",
  "weight_kg": 8.5,
  "height_cm": 74
}
Response (201 Created):
{
  "message": "Child Added Successfully",
  "child_id": 101
}

2. View All Children (GET /children)
Response (200 OK):
[
  {
    "child_id": 101,
    "name": "Ahmed Ali",
    "age_months": 18,
    "gender": "Male",
    "weight_kg": 8.5,
    "height_cm": 74.0
  },
  {
    "child_id": 102,
    "name": "Ayesha Khan",
    "age_months": 24,
    "gender": "Female",
    "weight_kg": 10.2,
    "height_cm": 82.0
  }
]

3. View Single Child (GET /children/101)
Response (200 OK):

JSON
{
  "child_id": 101,
  "name": "Ahmed Ali",
  "age_months": 18,
  "gender": "Male",
  "weight_kg": 8.5,
  "height_cm": 74.0
}

4. Update Child (PUT /children/101)
Request:

JSON
PUT /children/101
Content-Type: application/json

{
  "child_id": 101,
  "name": "Ahmed Ali",
  "age_months": 19,
  "gender": "Male",
  "weight_kg": 8.9,
  "height_cm": 75
}
Response (200 OK):

JSON
{
  "message": "Child Updated Successfully",
  "child_id": 101
}
5. Delete Child (DELETE /children/101)
Response (200 OK):

JSON
{
  "message": "Child Deleted Successfully",
  "child_id": 101
}
6. Error Response - Not Found (404 Not Found)
JSON
{
  "detail": "Child not found"
}
7. Error Response - Validation Failure (422 Unprocessable Entity)
JSON
{
  "detail": [
    {
      "loc": ["body", "weight_kg"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]


