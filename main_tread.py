from threading import Thread
from macchina import macchina
from fake_obd_script import obd_read
from gui_script import MainWindow
from PyQt5 import QtWidgets
import sys
import time
import os

def start_thread(target, obj):
    t = Thread(target=target, args=(obj,), daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    # Imposta la cartella di lavoro sulla directory dove si trova questo script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    m = macchina()
    threads = {'obd': start_thread(obd_read, m)}

    def monitor_thread():
        while True:
            if not threads['obd'].is_alive():
                time.sleep(5)
                print("🔄 Riavvio del thread OBD...")
                threads['obd'] = start_thread(obd_read, m)
            time.sleep(2)

    Thread(target=monitor_thread, daemon=True).start()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(m)
    window.show()
    sys.exit(app.exec_())
