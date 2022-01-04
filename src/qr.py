import sys
from time import asctime, sleep
import qrcode
import cv2
import psycopg2 as psy

class event:
    def __init__(self, data):
        self.name = data.split('-')[1]
        self.org = data.split('-')[0]
    def print_id(self):
        print('ID:', self.name, '-', 'ORG:', self.org)
    def db_connect(self):
        self.conn = psy.connect(dbname = 'coffee', user = 'postgres')
        self.curs = self.conn.cursor()
        print('Connection to DB established')
    def db_add_coffee(self):
        self.curs.execute("INSERT INTO log (username, event) VALUES ('{}', now())"
                          .format(self.name))
        self.conn.commit()
        print('One coffee added to', self.name)
        with open('log', 'a') as log:
            log.writelines(asctime())
            log.writelines('; ')
            log.writelines('One coffee added to ')
            log.writelines(self.name)
            log.writelines('\n')
    def db_close(self):
        self.conn.close()

# initialize camera and detector
cap = cv2.VideoCapture(4)
detector = cv2.QRCodeDetector()

# capture camera until a QR code is found or 
# five seconds passed
freq = int(sys.argv[1]) if len(sys.argv) > 1 else 4 #default to 4
time = 0
max_elapsed = 5 * freq
bbox = None
data = ''
while (bbox is None or len(data) == 0) and time < max_elapsed:
    time += 1
    state, img = cap.read()
    if state:
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None and len(data) > 0:
            print("QR code detected - ID: {}".format(data))
            exit_status = 0
            cap.release()
        else:
            print("No QR code detected")
            sleep(1 / freq)
    else:
        print("No video connection")
        sleep(1 / freq)

if (bbox is None or len(data) == 0) and time == max_elapsed:
    exit_status = 1
    print("No QR code found (Error {}). Exiting...".format(exit_status))

# ev = event(data)
# ev.db_connect()
# ev.db_add_coffee()
# ev.db_close()