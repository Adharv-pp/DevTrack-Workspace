import sys, requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QGridLayout, QStackedWidget, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QColor, QPainter, QBrush, QFont

# --- STYLESHEET ---
SS = """
* { font-family: 'Consolas', 'Segoe UI', monospace; color: #ddd8ff; }
QFrame#card {
    background-color: #111028; border-radius: 14px;
    border-left: 3px solid #7c5df5;
    border-top: 1px solid rgba(124,93,245,0.18);
    border-right: 1px solid rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
QFrame#page { background-color: transparent; }
QGroupBox {
    border: 1px solid rgba(255,255,255,0.06); border-radius: 8px;
    margin-top: 14px; padding: 12px;
    font-size: 12px; color: #a78bfa; letter-spacing: 1.5px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
QPushButton#p {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #5b3fd4, stop:1 #7c5df5);
    color: #fff; border: none; border-radius: 8px; padding: 10px 16px; font-size: 13px; font-weight: bold;
}
QPushButton#p:hover  { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6b4fe4,stop:1 #9070ff); }
QPushButton#s {
    background: rgba(255,255,255,0.04); color: #8b85cc;
    border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 8px 14px; font-size: 12px; text-align: left;
}
QPushButton#s:hover { background: rgba(124,93,245,0.12); color: #c4bfff; }
QPushButton#action {
    background: rgba(124,93,245,0.15); color: #a78bfa;
    border: 1px solid #7c5df5; border-radius: 6px; padding: 8px; font-size: 11px;
}
QPushButton#action:hover { background: #7c5df5; color: #fff; }
QLineEdit {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px; padding: 8px; color: #c4bfff; font-size: 12px;
}
QLineEdit:focus { border-color: #7c5df5; background: rgba(124,93,245,0.07); }
QTextEdit {
    background: #0d0b20; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px; padding: 10px; color: #4ade80; font-size: 12px;
}
QLabel#h1 { color: #a78bfa; font-size: 26px; font-weight: bold; letter-spacing: -1px; }
QLabel#sub { color: #4ade80; font-size: 12px; letter-spacing: 1px; }
QLabel#header { font-size: 22px; font-weight: bold; color: #fff; }
QLabel#data_title { color: #c4bfff; font-size: 15px; font-weight: bold; }
QLabel#data_sub { color: #8b85cc; font-size: 13px; }
"""

class Canvas(QWidget):
    def paintEvent(self, _):
        p = QPainter(self)
        g = QLinearGradient(0, 0, self.width(), self.height())
        g.setColorAt(0.0, QColor("#07080f")); g.setColorAt(0.55, QColor("#0d0b20")); g.setColorAt(1.0, QColor("#100d2e"))
        p.fillRect(self.rect(), QBrush(g))

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevTrack Pro - API Client")
        self.setFixedSize(950, 600)
        self.setStyleSheet(SS)

        # Flask API URL
        self.api_url = "http://127.0.0.1:5000/api/projects"

        body = Canvas(); self.setCentralWidget(body)
        main_layout = QHBoxLayout(body); main_layout.setContentsMargins(20, 20, 20, 20); main_layout.setSpacing(20)

        # --- LEFT SIDEBAR ---
        sidebar = QFrame(); sidebar.setObjectName("card"); sidebar.setFixedWidth(220)
        side_layout = QVBoxLayout(sidebar); side_layout.setContentsMargins(20, 30, 20, 30); side_layout.setSpacing(15)
        
        logo = QLabel("DevTrack_"); logo.setObjectName("h1"); logo.setAlignment(Qt.AlignCenter)
        user_sub = QLabel("WELCOME, ADHARV"); user_sub.setObjectName("sub"); user_sub.setAlignment(Qt.AlignCenter)
        side_layout.addWidget(logo); side_layout.addWidget(user_sub); side_layout.addSpacing(30)

        # Navigation Buttons (Now 5 tabs)
        self.btn_dash = QPushButton("📊 Dashboard"); self.btn_dash.setObjectName("s")
        self.btn_proj = QPushButton("📁 Active Projects"); self.btn_proj.setObjectName("s")
        self.btn_inv = QPushButton("🧾 Invoices"); self.btn_inv.setObjectName("s")
        self.btn_cli = QPushButton("👥 Clients"); self.btn_cli.setObjectName("s")
        self.btn_api = QPushButton("🗄️ Local DB API"); self.btn_api.setObjectName("s")
        
        for btn in (self.btn_dash, self.btn_proj, self.btn_inv, self.btn_cli, self.btn_api): side_layout.addWidget(btn)
        
        side_layout.addStretch()
        btn_exit = QPushButton("Exit Workspace"); btn_exit.setObjectName("s"); btn_exit.clicked.connect(self.close)
        side_layout.addWidget(btn_exit)
        main_layout.addWidget(sidebar)

        # --- RIGHT CONTENT (STACKED WIDGET) ---
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        # Add all 5 pages to the stack
        self.stacked.addWidget(self.create_dash_page())
        self.stacked.addWidget(self.create_projects_page())
        self.stacked.addWidget(self.create_invoices_page())
        self.stacked.addWidget(self.create_clients_page())
        self.stacked.addWidget(self.create_api_page()) # Lab 5 API

        # Connect Sidebar Buttons
        self.btn_dash.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.btn_proj.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        self.btn_inv.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        self.btn_cli.clicked.connect(lambda: self.stacked.setCurrentIndex(3))
        self.btn_api.clicked.connect(lambda: self.stacked.setCurrentIndex(4))


    # ================= PAGE 1: DASHBOARD =================
    def create_dash_page(self):
        page = QFrame(); page.setObjectName("page")
        layout = QVBoxLayout(page)
        
        top = QHBoxLayout()
        header = QLabel("Workspace Overview"); header.setObjectName("header")
        self.lbl_weather = QLabel("HQ Weather: Standby..."); self.lbl_weather.setStyleSheet("color: #8b85cc;")
        btn_weather = QPushButton("🌤️ Sync HQ"); btn_weather.setObjectName("p"); btn_weather.clicked.connect(self.api_weather)
        top.addWidget(header); top.addStretch(); top.addWidget(self.lbl_weather); top.addWidget(btn_weather)
        
        layout.addLayout(top); layout.addSpacing(20)

        grid = QGridLayout(); grid.setSpacing(20)

        projects_grp = QGroupBox("ACTIVE PROJECTS")
        p_layout = QVBoxLayout(projects_grp); p_layout.setSpacing(15)
        p1 = QLabel("E-Commerce Backend (DEV-101)"); p1.setObjectName("data_title")
        s1 = QLabel("Hourly Rate | 45 Hours Logged"); s1.setObjectName("data_sub")
        p2 = QLabel("Mobile App UI (DEV-102)"); p2.setObjectName("data_title")
        s2 = QLabel("Fixed Contract | $4,500"); s2.setObjectName("data_sub")
        p_layout.addWidget(p1); p_layout.addWidget(s1); p_layout.addSpacing(10)
        p_layout.addWidget(p2); p_layout.addWidget(s2); p_layout.addStretch()
        
        finance_grp = QGroupBox("MONTHLY REVENUE")
        f_layout = QVBoxLayout(finance_grp); f_layout.setSpacing(10)
        f1 = QLabel("$ 8,240.00"); f1.setStyleSheet("color: #4ade80; font-size: 34px; font-weight: bold;")
        s3 = QLabel("+14% from last month"); s3.setStyleSheet("color: #8b85cc; font-size: 13px;")
        f2 = QLabel("Pending Invoices: 2"); f2.setObjectName("data_title")
        f_layout.addSpacing(20); f_layout.addWidget(f1); f_layout.addWidget(s3)
        f_layout.addSpacing(20); f_layout.addWidget(f2); f_layout.addStretch()

        grid.addWidget(projects_grp, 0, 0); grid.addWidget(finance_grp, 0, 1)
        layout.addLayout(grid)
        return page

    def api_weather(self):
        self.lbl_weather.setText("Syncing..."); QApplication.processEvents()
        try:
            res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current=temperature_2m", timeout=3)
            temp = res.json()["current"]["temperature_2m"]
            self.lbl_weather.setText(f"Bengaluru HQ: {temp}°C")
            self.lbl_weather.setStyleSheet("color: #4ade80; font-weight:bold;")
        except: self.lbl_weather.setText("API Error")

    # ================= PAGE 2: PROJECTS =================
    def create_projects_page(self):
        page = QFrame(); page.setObjectName("page")
        layout = QVBoxLayout(page)
        
        header = QLabel("Active Projects & Portfolio"); header.setObjectName("header")
        layout.addWidget(header); layout.addSpacing(10)

        grp = QGroupBox("GITHUB PORTFOLIO STATS (LIVE API)")
        gl = QVBoxLayout(grp); gl.setSpacing(12)
        
        search_row = QHBoxLayout()
        self.git_input = QLineEdit()
        self.git_input.setPlaceholderText("Enter a GitHub username (e.g., torvalds, octocat)")
        btn_git = QPushButton("Fetch Live Stats"); btn_git.setObjectName("p")
        btn_git.clicked.connect(self.api_github)
        search_row.addWidget(self.git_input); search_row.addWidget(btn_git)

        self.lbl_git = QLabel("Search any GitHub user to fetch their repository stats."); self.lbl_git.setStyleSheet("color: #8b85cc;")
        gl.addLayout(search_row); gl.addWidget(self.lbl_git)
        
        grp2 = QGroupBox("CURRENT WORK")
        gl2 = QVBoxLayout(grp2)
        gl2.addWidget(QLabel("1. Volunteer Management System (.NET) - 80% Complete"))
        gl2.addWidget(QLabel("2. Synthetic Voice Detection (Python) - Model Training phase"))
        
        layout.addWidget(grp); layout.addWidget(grp2); layout.addStretch()
        return page

    def api_github(self):
        username = self.git_input.text().strip()
        if not username:
            self.lbl_git.setText("Please enter a username first."); self.lbl_git.setStyleSheet("color: #f87171;")
            return
            
        self.lbl_git.setText(f"Searching for '{username}'..."); self.lbl_git.setStyleSheet("color: #8b85cc;")
        QApplication.processEvents()
        
        try:
            res = requests.get(f"https://api.github.com/users/{username}", timeout=3)
            if res.status_code == 404:
                self.lbl_git.setText("User not found on GitHub."); self.lbl_git.setStyleSheet("color: #f87171;")
                return
            res.raise_for_status()
            data = res.json()
            display_name = data.get('name') or username
            self.lbl_git.setText(f"User: {display_name} | Public Repos: {data['public_repos']} | Followers: {data['followers']}")
            self.lbl_git.setStyleSheet("color: #4ade80; font-size: 14px; font-weight: bold;")
        except: 
            self.lbl_git.setText("Network Error / Rate Limit Reached"); self.lbl_git.setStyleSheet("color: #f87171;")

    # ================= PAGE 3: INVOICES =================
    def create_invoices_page(self):
        page = QFrame(); page.setObjectName("page")
        layout = QVBoxLayout(page)
        
        header = QLabel("Billing & Invoices"); header.setObjectName("header")
        layout.addWidget(header); layout.addSpacing(10)

        grp = QGroupBox("LIVE CURRENCY CONVERTER (USD TO INR)")
        gl = QVBoxLayout(grp)
        self.lbl_cur = QLabel("Check live exchange rates before generating invoices.")
        btn_cur = QPushButton("Fetch Forex Rates"); btn_cur.setObjectName("p"); btn_cur.clicked.connect(self.api_currency)
        gl.addWidget(self.lbl_cur); gl.addWidget(btn_cur)
        
        grp2 = QGroupBox("UNPAID INVOICES")
        gl2 = QVBoxLayout(grp2)
        gl2.addWidget(QLabel("INV-001 | Client: TechCorp | Amount: $1,200 | STATUS: OVERDUE"))
        gl2.addWidget(QLabel("INV-002 | Client: StartupX | Amount: $450  | STATUS: PENDING"))
        
        layout.addWidget(grp); layout.addWidget(grp2); layout.addStretch()
        return page

    def api_currency(self):
        self.lbl_cur.setText("Contacting Bank APIs..."); QApplication.processEvents()
        try:
            res = requests.get("https://api.frankfurter.app/latest?from=USD&to=INR", timeout=3)
            rate = res.json()["rates"]["INR"]
            self.lbl_cur.setText(f"1 USD = {rate} INR (Live Bank Rate)")
            self.lbl_cur.setStyleSheet("color: #4ade80; font-size: 14px;")
        except: self.lbl_cur.setText("Currency API Offline")

    # ================= PAGE 4: CLIENTS =================
    def create_clients_page(self):
        page = QFrame(); page.setObjectName("page")
        layout = QVBoxLayout(page)
        
        header = QLabel("Client CRM"); header.setObjectName("header")
        layout.addWidget(header); layout.addSpacing(10)

        grp = QGroupBox("GENERATE NEW MOCK CLIENT (API)")
        gl = QVBoxLayout(grp)
        self.lbl_cli = QLabel("Click to simulate a new client lead.")
        btn_cli = QPushButton("Generate Client Lead"); btn_cli.setObjectName("p"); btn_cli.clicked.connect(self.api_client)
        gl.addWidget(self.lbl_cli); gl.addWidget(btn_cli)
        
        layout.addWidget(grp); layout.addStretch()
        return page

    def api_client(self):
        self.lbl_cli.setText("Finding a client..."); QApplication.processEvents()
        try:
            res = requests.get("https://randomuser.me/api/?inc=name,email,location", timeout=3)
            data = res.json()["results"][0]
            name = f"{data['name']['first']} {data['name']['last']}"
            email = data['email']
            country = data['location']['country']
            self.lbl_cli.setText(f"New Lead: {name}\nEmail: {email}\nLocation: {country}")
            self.lbl_cli.setStyleSheet("color: #4ade80; font-size: 13px;")
        except: self.lbl_cli.setText("CRM API Error")


    # ================= PAGE 5: LAB 5 LOCAL DB API =================
    def create_api_page(self):
        page = QFrame(); page.setObjectName("page")
        layout = QVBoxLayout(page)
        
        header = QLabel("Database API Controls"); header.setObjectName("header")
        layout.addWidget(header); layout.addSpacing(10)

        # Interactive Controls Grid
        grid = QGridLayout(); grid.setSpacing(10)
        
        # 1. GET Request
        btn_get = QPushButton("GET (Fetch All Records)"); btn_get.setObjectName("action")
        btn_get.clicked.connect(self.req_get)
        grid.addWidget(btn_get, 0, 0, 1, 4)

        # 2. POST Request (Inputs: Title, Tech, Status)
        self.post_title = QLineEdit(); self.post_title.setPlaceholderText("Project Title")
        self.post_tech = QLineEdit(); self.post_tech.setPlaceholderText("Tech Stack")
        self.post_status = QLineEdit(); self.post_status.setPlaceholderText("Status (e.g., Planning)")
        btn_post = QPushButton("POST"); btn_post.setObjectName("action")
        btn_post.clicked.connect(self.req_post)
        
        grid.addWidget(self.post_title, 1, 0)
        grid.addWidget(self.post_tech, 1, 1)
        grid.addWidget(self.post_status, 1, 2)
        grid.addWidget(btn_post, 1, 3)

        # 3. PUT Request (Inputs: ID, New Status)
        self.put_id = QLineEdit(); self.put_id.setPlaceholderText("Project ID to Update")
        self.put_status = QLineEdit(); self.put_status.setPlaceholderText("New Status")
        btn_put = QPushButton("PUT"); btn_put.setObjectName("action")
        btn_put.clicked.connect(self.req_put)
        
        grid.addWidget(self.put_id, 2, 0)
        grid.addWidget(self.put_status, 2, 1, 1, 2)
        grid.addWidget(btn_put, 2, 3)

        # 4. DELETE Request (Input: ID)
        self.del_id = QLineEdit(); self.del_id.setPlaceholderText("Project ID to Delete")
        btn_del = QPushButton("DELETE"); btn_del.setObjectName("action")
        btn_del.clicked.connect(self.req_del)
        
        grid.addWidget(self.del_id, 3, 0, 1, 3)
        grid.addWidget(btn_del, 3, 3)

        layout.addLayout(grid); layout.addSpacing(10)

        # Output Display
        self.api_output = QTextEdit()
        self.api_output.setReadOnly(True)
        self.api_output.setText("Waiting for API requests...\nEnsure 'devtrack_api.py' is running on port 5000.")
        layout.addWidget(self.api_output)

        return page

    # --- HTTP METHODS FOR LAB 5 ---
    
    def log_response(self, text, is_error=False):
        color = "#f87171" if is_error else "#4ade80"
        self.api_output.append(f'<span style="color:{color}">{text}</span><br><hr>')

    def req_get(self):
        self.api_output.clear()
        try:
            res = requests.get(self.api_url, timeout=3)
            res.raise_for_status() 
            data = res.json()["data"]
            self.log_response("<b>[200 OK] Successfully retrieved records:</b>")
            for proj in data:
                formatted = f"ID: {proj['id']} | Title: {proj['title']} | Tech: {proj['tech']} | Status: {proj['status']}"
                self.api_output.append(f'<span style="color:#c4bfff">{formatted}</span>')
        except requests.exceptions.RequestException as e:
            self.log_response(f"Connection Failed: Is the Flask server running? Error: {e}", is_error=True)

    def req_post(self):
        t = self.post_title.text().strip()
        tc = self.post_tech.text().strip()
        s = self.post_status.text().strip()
        
        if not t or not tc or not s:
            self.log_response("POST Error: All fields (Title, Tech, Status) are required.", is_error=True)
            return
            
        new_data = {"title": t, "tech": tc, "status": s}
        try:
            res = requests.post(self.api_url, json=new_data, timeout=3)
            res.raise_for_status()
            parsed = res.json()
            self.log_response(f"[201 CREATED] {parsed['message']}: {parsed['data']['title']}")
            self.post_title.clear(); self.post_tech.clear(); self.post_status.clear()
        except requests.exceptions.RequestException as e:
            self.log_response(f"POST Failed: {e}", is_error=True)

    def req_put(self):
        pid = self.put_id.text().strip()
        s = self.put_status.text().strip()
        
        if not pid or not s:
            self.log_response("PUT Error: Both ID and New Status are required.", is_error=True)
            return
        if not pid.isdigit():
            self.log_response("PUT Error: Project ID must be a valid number.", is_error=True)
            return
            
        update_data = {"status": s}
        try:
            res = requests.put(f"{self.api_url}/{pid}", json=update_data, timeout=3)
            if res.status_code == 404:
                self.log_response(f"PUT Error: Project ID {pid} not found in database.", is_error=True)
                return
            res.raise_for_status()
            parsed = res.json()
            self.log_response(f"[200 OK] {parsed['message']}! New Status: {parsed['data']['status']}")
            self.put_id.clear(); self.put_status.clear()
        except requests.exceptions.RequestException as e:
            self.log_response(f"PUT Failed: {e}", is_error=True)

    def req_del(self):
        pid = self.del_id.text().strip()
        if not pid or not pid.isdigit():
            self.log_response("DELETE Error: A valid numeric Project ID is required.", is_error=True)
            return
            
        try:
            res = requests.delete(f"{self.api_url}/{pid}", timeout=3)
            res.raise_for_status()
            parsed = res.json()
            self.log_response(f"[200 OK] {parsed['message']}")
            self.del_id.clear()
        except requests.exceptions.RequestException as e:
            self.log_response(f"DELETE Failed: {e}", is_error=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Consolas", 10))
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())