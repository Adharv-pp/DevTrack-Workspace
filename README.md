# DevTrack_ Workspace 🚀

A Python project suite built around a freelance developer workflow: a PyQt5 desktop dashboard, a Flask REST API, and Streamlit apps for analytics and file management.

## 🌟 Core Features
* **Interactive GUI Dashboard:** `PyQt5` dark-mode, multi-page layout with RegEx-validated login (Labs 1-4).
* **Public API Integration:** Open-Meteo (live weather), GitHub REST API (portfolio stats), Frankfurter (USD to INR), RandomUser (mock client generation).
* **Custom REST API (Lab 5):** `Flask` backend with full CRUD (`GET` all or by ID, `POST`, `PUT`, `DELETE`), JSON validation, and 400/404 error handling. A PyQt client consumes it with `requests`.
* **Project Dashboard (Lab 6):** Streamlit app backed by a CSV, with filters, an add-project form, summary metrics, and Bar/Line/Pie charts.
* **Client Records Manager (Lab 7):** Streamlit app with plain-text file handling (create, read, append, search, update, delete, verified backup) and RegEx input validation.
* **Project Analytics (Lab 9):** NumPy computation, aggregations, boolean masks, fancy indexing, sorting, and 5 plot types on DevTrack data.

## 🛠️ Tech Stack
* **GUI:** Python, PyQt5, RegEx
* **Backend:** Flask, `requests`
* **Data & Analytics:** Streamlit, Pandas, NumPy, Matplotlib

## 📁 Project Structure
| File | Lab | Description |
|---|---|---|
| `lab_1.py` - `lab_4.py` | 1-4 | Core Python, PyQt dashboard, public API integrations |
| `devtrack_api.py`, `lab_5_client.py` | 5 | Flask REST API + PyQt client |
| `lab_6_streamlit.py`, `projects_data.csv` | 6 | Streamlit project dashboard |
| `lab_7_streamlit.py`, `devtrack_file_manager.py` | 7 | File-handling client records manager |
| `lab_9_streamlit.py`, `devtrack_analytics.csv` | 9 | NumPy project analytics |

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies:
   ```
   pip install PyQt5 requests flask streamlit pandas numpy matplotlib
   ```
3. **Lab 4:** `python lab_4.py`
4. **Lab 5:** start the server with `python devtrack_api.py`, then in a second terminal run `python lab_5_client.py`
5. **Lab 6:** `streamlit run lab_6_streamlit.py`
6. **Lab 7:** `streamlit run lab_7_streamlit.py` (creates `clients_data.txt` on first run)
7. **Lab 9:** `streamlit run lab_9_streamlit.py`

Keep each CSV in the same folder as its script.