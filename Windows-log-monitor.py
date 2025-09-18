import win32evtlog
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, scrolledtext
from tkcalendar import DateEntry

# -- Task Category Mapping for Security Logs --
TASK_CATEGORY_MAP_SECURITY = {
    12288: "System Event",
    12544: "Logon",
    12545: "Logoff",
    12546: "Account Lockout",
    13184: "IPsec Main Mode",
    13185: "IPsec Quick Mode",
    13186: "IPsec Extended Mode",
    13312: "Special Logon",
    13313: "Special Logoff",
    13314: "Other Logon/Logoff Events",
    13440: "Network Policy Server",
    13441: "Network Policy Server Account Lockout",
    13568: "File Share",
    13696: "Detailed File Share",
    13824: "User Account Management",
    13825: "Computer Account Management",
    13826: "Security Group Management",
    13827: "Distribution Group Management",
    13828: "Application Group Management",
    14080: "Other Account Management Events",
    14208: "Directory Service Access",
    14336: "Directory Service Changes",
    14337: "Directory Service Replication",
    14338: "Detailed Directory Service Replication",
    14464: "Credential Validation",
    14688: "Kerberos Service Ticket Operations",
    14689: "Other Kerberos Authentication Events",
    14848: "User Device Claims",
    14849: "Device Claims",
    16384: "Logoff",
}

def resolve_task_category(numeric, log_type):
    if log_type == "Security":
        return TASK_CATEGORY_MAP_SECURITY.get(numeric, "None")
    else:
        return "None"

def event_type_str(event_type):
    mapping = {
        1: "Error",
        2: "Warning",
        4: "Information",
        8: "Success Audit",
        16: "Failure Audit"
    }
    return mapping.get(event_type, f"Unknown({event_type})")

def fetch_events(logtype, start_date, end_date, filter_eventids=None):
    server = 'localhost'
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    start_dt = datetime.strptime(start_date, "%d/%m/%Y")
    end_dt = datetime.strptime(end_date, "%d/%m/%Y") + timedelta(days=1) - timedelta(seconds=1)
    event_rows = []
    event_xmls = []
    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break
        for event in events:
            try:
                event_time = event.TimeGenerated
                event_id_match = True
                if filter_eventids:
                    event_id_match = event.EventID in filter_eventids
                if start_dt <= event_time <= end_dt and event_id_match:
                    friendly_taskcat = resolve_task_category(event.EventCategory, logtype)
                    row = (
                        event.RecordNumber,
                        event.EventID,
                        friendly_taskcat,
                        event.EventCategory,
                        event_time.strftime("%Y-%m-%d %H:%M:%S"),
                        event.SourceName,
                        event_type_str(event.EventType),
                        event.ComputerName,
                        (" | ".join(event.StringInserts) if event.StringInserts else "")
                    )
                    # XML for popup
                    xml_txt = "<Event>\n"
                    xml_txt += f"  <RecordNumber>{event.RecordNumber}</RecordNumber>\n"
                    xml_txt += f"  <EventID>{event.EventID}</EventID>\n"
                    xml_txt += f"  <TaskCategory>{friendly_taskcat}</TaskCategory>\n"
                    xml_txt += f"  <TaskCategoryID>{event.EventCategory}</TaskCategoryID>\n"
                    xml_txt += f"  <TimeGenerated>{event_time}</TimeGenerated>\n"
                    xml_txt += f"  <Source>{event.SourceName}</Source>\n"
                    xml_txt += f"  <Type>{event_type_str(event.EventType)}</Type>\n"
                    xml_txt += f"  <Computer>{event.ComputerName}</Computer>\n"
                    if event.StringInserts:
                        xml_txt += f"  <Message>{' | '.join(event.StringInserts)}</Message>\n"
                    xml_txt += "</Event>"
                    event_rows.append(row)
                    event_xmls.append(xml_txt)
            except Exception:
                continue
        if events and events[-1].TimeGenerated < start_dt:
            break
    win32evtlog.CloseEventLog(hand)
    return event_rows, event_xmls

def load_events(*args):
    selected_log = log_var.get()
    start_date = start_cal.get()
    end_date = end_cal.get()
    # Parse Event IDs from entry, allow comma separation, strip whitespace
    eventids_input = eventid_var.get().strip()
    if eventids_input:
        try:
            filter_eventids = set(int(eid) for eid in eventids_input.replace(" ", "").split(",") if eid)
        except Exception:
            messagebox.showerror("Invalid Event ID(s)", "Event ID filters must be integers, separated by commas.")
            return
    else:
        filter_eventids = None
    tree.delete(*tree.get_children())
    events_data, events_xml = fetch_events(selected_log, start_date, end_date, filter_eventids)
    for i, row in enumerate(events_data):
        tree.insert('', 'end', iid=i, values=row)
    global event_xml_list
    event_xml_list = events_xml

def show_more_popup(event=None):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("No selection", "Please select an event first.")
        return
    idx = int(sel[0])
    xml_text = event_xml_list[idx]
    popup = Toplevel(root)
    popup.title("Event XML View")
    popup.geometry("700x500")
    text_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Consolas', 10))
    text_widget.insert(tk.END, xml_text)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(expand=True, fill=tk.BOTH)

root = tk.Tk()
root.title("Responsive Windows Event Log Viewer (Date Range & Task Category)")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.geometry("1500x750")

top_frame = ttk.Frame(root)
top_frame.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=5)

logs = ["Application", "Security", "Setup", "System", "ForwardedEvents"]
log_var = tk.StringVar(value=logs[0])
ttk.Label(top_frame, text="Select Event Log:").pack(side=tk.LEFT)
log_combo = ttk.Combobox(top_frame, textvariable=log_var, values=logs, state='readonly', width=25)
log_combo.pack(side=tk.LEFT, padx=5)

ttk.Label(top_frame, text="Start Date:").pack(side=tk.LEFT, padx=(20,2))
start_cal = DateEntry(top_frame, width=12, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy')
start_cal.pack(side=tk.LEFT)
start_cal.set_date(datetime.now() - timedelta(days=7))

ttk.Label(top_frame, text="End Date:").pack(side=tk.LEFT, padx=(20,2))
end_cal = DateEntry(top_frame, width=12, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy')
end_cal.pack(side=tk.LEFT)
end_cal.set_date(datetime.now())

# -- Event ID filter Entry --
ttk.Label(top_frame, text="Filter Event ID(s):").pack(side=tk.LEFT, padx=(20,2))
eventid_var = tk.StringVar()
eventid_entry = ttk.Entry(top_frame, textvariable=eventid_var, width=20)
eventid_entry.pack(side=tk.LEFT)

load_btn = ttk.Button(top_frame, text="Load Logs", command=load_events)
load_btn.pack(side=tk.LEFT, padx=10)

show_btn = ttk.Button(top_frame, text="Show More (XML)", command=show_more_popup)
show_btn.pack(side=tk.LEFT, padx=10)

columns = (
    "Record#", "Event ID", "Task Category", "Category#", "Time",
    "Source", "Type", "Computer"
)
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    if col in ("Record#", "Event ID", "Task Category", "Category#"):
        tree.column(col, width=120, anchor=tk.CENTER)
    elif col == "Time":
        tree.column(col, width=160, anchor=tk.CENTER)
    elif col == "Type":
        tree.column(col, width=105, anchor=tk.CENTER)
    else:
        tree.column(col, width=200, anchor=tk.W)
tree.grid(row=1, column=0, sticky=tk.NSEW)

scroll_y = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll_y.set)
scroll_y.grid(row=1, column=1, sticky=tk.NS)

tree.bind("<Double-1>", show_more_popup)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

event_xml_list = []
log_combo.bind("<<ComboboxSelected>>", load_events)

load_events()
root.mainloop()
