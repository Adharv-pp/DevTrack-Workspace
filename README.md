# DevTrack_ Workspace 🚀

A comprehensive Python-based desktop application and analytics suite designed for freelance developers to manage active projects, track invoices, and analyze their business data.

## 🌟 Core Features
* **Interactive GUI Dashboard:** Built using `PyQt5` with a custom dark-mode, multi-page layout.
* **Data Analytics & Visualization:** Uses `Streamlit` to render real-time web applications and dashboards for freelance business metrics (Labs 6, 7, & 9).
* **Data Processing Pipeline:** Implements `pandas` for robust CSV data manipulation, tracking project files and analytics.
* **REST API Integration:** Consumes multiple public APIs for live developer stats, including:
  * Open-Meteo API (Live weather tracking)
  * GitHub REST API (Live developer portfolio stats)
  * Frankfurter API (Live USD to INR currency conversion)
  * RandomUser API (Mock client generation)
* **Local Database API:** Features a custom `Flask` backend server hosting a JSON dataset with full CRUD functionality (`GET`, `POST`, `PUT`, `DELETE`).

## 🛠️ Tech Stack
* **Frontend UI:** Python, PyQt5, RegEx (Data Validation)
* **Data Science & Analytics:** Streamlit, Pandas
* **Backend:** Python, Flask, `requests` library

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies: `pip install PyQt5 requests flask streamlit pandas`
3. **To run the main dashboard:** `python lab_5_client.py` (ensure `devtrack_api.py` is running first).
4. **To run the analytics dashboards:** `streamlit run lab_6_streamlit.py`