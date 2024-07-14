import cups

def get_printer_status():
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        print(f"Printer: {printer}, Status: {printers[printer]['printer-state-message']}")

get_printer_status()

