import sys, re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QRadioButton, QCheckBox, QLabel, QPushButton,
    QMessageBox, QButtonGroup, QGroupBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QColor, QPainter, QBrush, QFont

SS = """
* { font-family: 'Consolas', 'Segoe UI', monospace; color: #ddd8ff; }
QFrame#card {
    background-color: #111028;
    border-radius: 14px;
    border-left: 3px solid #7c5df5;
    border-top: 1px solid rgba(124,93,245,0.18);
    border-right: 1px solid rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
QLineEdit, QComboBox {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 12px;
    color: #c4bfff;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #7c5df5;
    background: rgba(124,93,245,0.07);
}
QComboBox::drop-down { border:none; width:20px; }
QComboBox QAbstractItemView {
    background:#1a1640; color:#c4bfff;
    border:1px solid #3b2fa0;
    selection-background-color:#3b2fa0; outline:none;
}
QRadioButton { color:#8b85cc; font-size:12px; spacing:6px; }
QRadioButton::indicator {
    width:13px; height:13px; border-radius:7px;
    border:2px solid #2e2a6b; background:#0d0b20;
}
QRadioButton::indicator:checked { background:#7c5df5; border-color:#a78bfa; }
QCheckBox { color:#8b85cc; font-size:12px; spacing:6px; }
QCheckBox::indicator {
    width:13px; height:13px; border-radius:3px;
    border:2px solid #2e2a6b; background:#0d0b20;
}
QCheckBox::indicator:checked { background:#7c5df5; border-color:#a78bfa; }
QGroupBox {
    border:1px solid rgba(255,255,255,0.06); border-radius:8px;
    margin-top:10px; padding:8px 6px 4px 6px;
    font-size:10px; color:#3d3880; letter-spacing:1.5px;
}
QGroupBox::title { subcontrol-origin:margin; left:10px; padding:0 4px; }
QPushButton#p {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #5b3fd4, stop:1 #7c5df5);
    color:#fff; border:none; border-radius:8px;
    padding:10px; font-size:12px; font-weight:bold;
}
QPushButton#p:hover  { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6b4fe4,stop:1 #9070ff); }
QPushButton#p:pressed{ background:#3d27a8; }
QPushButton#s {
    background:rgba(255,255,255,0.04); color:#8b85cc;
    border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; font-size:12px;
}
QPushButton#s:hover { background:rgba(124,93,245,0.12); color:#c4bfff; }
"""

class Canvas(QWidget):
    def paintEvent(self, _):
        p = QPainter(self)
        g = QLinearGradient(0, 0, self.width(), self.height())
        g.setColorAt(0.0, QColor("#07080f"))
        g.setColorAt(0.55, QColor("#0d0b20"))
        g.setColorAt(1.0, QColor("#100d2e"))
        p.fillRect(self.rect(), QBrush(g))


class ExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exit")
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        wrapper = QFrame(self)
        wrapper.setObjectName("card")
        wrapper.setFixedSize(300, 150)

        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        msg = QLabel("Exit DevTrack?")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color:#c4bfff; font-size:14px; font-weight:bold;")

        sub = QLabel("Any unsaved changes will be lost.")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color:#3d3880; font-size:10px; letter-spacing:0.5px;")

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        no_btn = QPushButton("Cancel")
        no_btn.setObjectName("s")
        no_btn.clicked.connect(self.reject)

        yes_btn = QPushButton("Yes, Exit")
        yes_btn.setObjectName("p")
        yes_btn.clicked.connect(self.accept)

        btn_row.addWidget(no_btn)
        btn_row.addWidget(yes_btn)

        layout.addWidget(msg)
        layout.addWidget(sub)
        layout.addLayout(btn_row)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(wrapper)


class DevTrack(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevTrack")
        self.setFixedSize(500, 690)
        self.setStyleSheet(SS)

        body = Canvas()
        self.setCentralWidget(body)
        outer = QVBoxLayout(body)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame(); card.setObjectName("card"); card.setFixedWidth(430)
        outer.addWidget(card, 0, Qt.AlignCenter)
        c = QVBoxLayout(card)
        c.setContentsMargins(28, 26, 28, 24)
        c.setSpacing(10)

        # Header
        t = QLabel("DevTrack_"); t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("color:#a78bfa; font-size:22px; font-weight:bold; letter-spacing:-1px;")
        s = QLabel("DEVELOPER REGISTRATION"); s.setAlignment(Qt.AlignCenter)
        s.setStyleSheet("color:#3d3880; font-size:10px; letter-spacing:3px;")
        c.addWidget(t); c.addWidget(s); c.addSpacing(4)

        def inp(ph, pwd=False):
            w = QLineEdit(); w.setPlaceholderText(ph)
            if pwd: w.setEchoMode(QLineEdit.Password)
            return w

        self.name  = inp("Full Name  — First & Last")
        self.devid = inp("Dev ID  — DEV-001")
        self.uname = inp("Username  — 5–10 lowercase")
        self.pwd   = inp("Password  — needs  @_!#$%^&*", pwd=True)
        self.phone = inp("Phone  — 10+ digits")
        for w in (self.name, self.devid, self.uname, self.pwd, self.phone):
            c.addWidget(w)

        self.domain = QComboBox()
        self.domain.addItems(["Domain  ▾", "Frontend", "Backend",
            "Full-Stack", "DevOps / Cloud", "Data Science / ML",
            "Mobile", "Cybersecurity"])
        c.addWidget(self.domain)

        grp = QGroupBox("EXPERIENCE"); row = QHBoxLayout(grp); row.setSpacing(16)
        self.rb = [QRadioButton(x) for x in ("Junior", "Intermediate", "Senior")]
        self._rbg = QButtonGroup(self)
        for b in self.rb: self._rbg.addButton(b); row.addWidget(b)
        row.addStretch(); c.addWidget(grp)

        self.terms = QCheckBox("Agree to DevTrack Terms & Conditions")
        c.addWidget(self.terms)

        self.pill = QLabel("")
        self.pill.setAlignment(Qt.AlignCenter)
        self.pill.setWordWrap(True)
        self.pill.setStyleSheet("font-size:11px; min-height:30px;")
        c.addWidget(self.pill)

        # Buttons
        br = QHBoxLayout(); br.setSpacing(8)
        self.b_reg   = QPushButton("Register");  self.b_reg.setObjectName("p")
        self.b_clear = QPushButton("Clear");     self.b_clear.setObjectName("s")
        self.b_exit  = QPushButton("Exit");      self.b_exit.setObjectName("s")
        br.addWidget(self.b_reg, 3); br.addWidget(self.b_clear, 2); br.addWidget(self.b_exit, 2)
        c.addLayout(br)

        # Signals → Slots
        self.b_reg.clicked.connect(self.submit)
        self.b_clear.clicked.connect(self.reset)
        self.b_exit.clicked.connect(self.close)

    def submit(self):
        n = self.name.text().strip()
        parts = re.findall(r"[A-Za-z]+", n)
        errs = []
        if len(parts) < 2:                                          errs.append("Full name")
        if not re.match(r"^DEV-\d{3}$", self.devid.text().strip()): errs.append("Dev ID")
        if not re.fullmatch(r"[a-z0-9]{5,10}", self.uname.text().strip()): errs.append("Username")
        if not re.search(r"[@_!#$%^&*]", self.pwd.text()):         errs.append("Password")
        if len(re.sub(r"\D","",self.phone.text())) < 10:            errs.append("Phone")
        if self.domain.currentIndex() == 0:                        errs.append("Domain")
        if not self._rbg.checkedButton():                          errs.append("Experience")
        if not self.terms.isChecked():                             errs.append("Terms")

        if errs:
            self.pill.setStyleSheet(
                "color:#f87171; background:rgba(248,113,113,0.09);"
                "border:1px solid rgba(248,113,113,0.25); border-radius:8px; padding:7px; font-size:11px;")
            self.pill.setText("✗  Not logged in  ·  fix: " + ", ".join(errs))
        else:
            lvl = self._rbg.checkedButton().text()
            dom = self.domain.currentText()
            self.pill.setStyleSheet(
                "color:#4ade80; background:rgba(74,222,128,0.09);"
                "border:1px solid rgba(74,222,128,0.25); border-radius:8px; padding:7px; font-size:11px;")
            self.pill.setText(
                f"✓  Logged in  ·  {parts[0]} {parts[1]}  ·  {dom}  ·  {lvl}")

    def reset(self):
        for w in (self.name, self.devid, self.uname, self.pwd, self.phone): w.clear()
        self.domain.setCurrentIndex(0)
        self._rbg.setExclusive(False)
        for b in self.rb: b.setChecked(False)
        self._rbg.setExclusive(True)
        self.terms.setChecked(False)
        self.pill.setText(""); self.pill.setStyleSheet("")

    def closeEvent(self, e):
        dlg = ExitDialog(self)
        e.accept() if dlg.exec_() == QDialog.Accepted else e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Consolas", 10))

    window = DevTrack()
    window.show()

    sys.exit(app.exec_())