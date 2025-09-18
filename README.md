# 🪟 Windows Log Monitor (Python + Tkinter)

A responsive **Windows Log Monitor** for security auditing, troubleshooting, and forensic analysis.
It retrieves Windows event logs using Python, offers powerful date-based filtering, and provides a modern, scrollable UI for deep investigation of log events.
Filter by multiple Event IDs using a simple input box!

---

## 🚀 Features

- **Log Source Selection:** Application, Security, Setup, System, and ForwardedEvents  
- **Date Range Filtering:** Filter logs by start and end date using a calendar popup
- **Event ID Filtering:** Input multiple Event IDs (comma-separated) to narrow results (e.g., 4624,4634,4720)
- **Event Details Table:** Tabular view with:
  - Record Number  
  - Event ID  
  - Task Category (mapped for secuity logs) 
  - Category Number  
  - Time  
  - Source  
  - Type (Error, Warning, Information, etc.)  
  - Computer Name  
- **Event XML Popup:** Double-click a row or click “Show More (XML)” for full event XML details.  
- **Responsive Display** Scalable window and vertical scrollbars for browsing large datasets.
- **Immediate Usage:** Fetches last 7 days of logs by default.
- **Task Category Mapping:** Friendly labels for Security logs. (e.g., Logon, Logoff, User Account Management)  
- 🔒 **Privacy:** Purely local — no data leaves your PC  

---

## ⚠️ Limitations

- 🪟 **Windows Only** — Uses Windows Event Log APIs (not supported on Linux/Mac)  
- 🔑 **Admin Rights** — Some logs (e.g., Security) may require administrator privileges  
- 🐢 **Performance** — Very large logs (100k+ entries) may take time to process  

---

## 🛠️ Requirements

- Windows OS  
- Python **3.7+**  

**Dependencies:**
- `pywin32`
- `tkcalendar`

---

## 📦 Installation

1. **Clone or Download:**
   ```
   git clone https://github.com/Rezwan0000000/Windows-log-monitor
   cd Windows-log-monitor
2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
3. **Run the Application:**
   
   `python Windows-log-monitor.py`

   <img width="1918" height="1035" alt="image" src="https://github.com/user-attachments/assets/2ba2b6a6-11c3-47a5-9287-bc8be69ed77b" />


## ⚡ Usage

1. **Select Event Log**  
   Choose **Application**, **Security**, **System**, etc. from the dropdown menu.

2. **Set Date Range**  
   Pick **start** and **end** dates (defaults: last 7 days).

3. **Load Events:**
   Click Load Logs to retrieve and display the matching events.

4. **Load Events**  
   Click **"Load Logs"** to query and populate results.

5. **Browse Logs**  
   Scroll through the results table with **sortable columns**.

6. **Event Details**  
   - Double-click a row, **or**  
   - Select a row → click **"Show More (XML)"**  
     
   to view the full event XML.

<img width="1920" height="1036" alt="image" src="https://github.com/user-attachments/assets/1cbda9d7-8951-4e06-8000-1f0d035f8604" />

## 🧩 Customization & Extensibility

- **Add More Task Categories**  
  Expand the `TASK_CATEGORY_MAP_SECURITY` dictionary to include additional Security event categories.

- **Advanced Filtering**  
  Extend the UI to filter by **Event ID**, **Source**, or **Event Type**.

- **Log Export**  
  Add **CSV/Excel/JSON export** functionality (future feature).

- **Live Monitoring**  
  Implement **real-time event streaming** (planned).

---

## 📌 Roadmap

- [ ] CSV/JSON export support  
- [ ] Keyword / EventID filtering  
- [ ] Live event monitoring mode  
- [ ] Dark theme for Tkinter UI  

---

## 🤝 Contributing

Contributions are welcome! You can help by:  

- Adding new task category mappings  
- Improving filtering and export features  
- Reporting bugs or suggesting features via **Issues** or **Pull Requests**  

---

## 📄 License

MIT License — free for professional, academic, and DFIR use.
