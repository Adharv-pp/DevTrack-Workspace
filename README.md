# DevTrack_ Workspace 

A comprehensive Python-based desktop application designed for freelance developers to manage active projects, track invoices, and manage client relationships. 

## Features
* **Interactive GUI:** Built using `PyQt5` with a custom dark-mode, multi-page dashboard.
* **REST API Integration (Client):** Consumes multiple public APIs including:
  * Open-Meteo API (Live weather tracking)
  * GitHub REST API (Live developer portfolio stats)
  * Frankfurter API (Live USD to INR currency conversion)
  * RandomUser API (Mock client generation)
* **Local Database API (Server):** Features a custom `Flask` backend server that hosts a JSON dataset.
* **Full CRUD Functionality:** The dashboard acts as an API client capable of executing `GET`, `POST`, `PUT`, and `DELETE` requests to the local server with robust error handling.

## Tech Stack
* **Frontend:** Python, PyQt5, RegEx (Data Validation)
* **Backend:** Python, Flask, `requests` library

## How to Run
1. Clone the repository.
2. Install required dependencies: `pip install PyQt5 requests flask`
3. Start the local API server: `python devtrack_api.py`
4. Launch the dashboard client: `python lab_5_client.py`