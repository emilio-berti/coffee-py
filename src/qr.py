from time import asctime
import qrcode
import cv2
import psycopg2 as psy

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

img = cv2.imread('/home/squirry/Pictures/coffee/emilio.png', cv2.IMREAD_GRAYSCALE)
data, bbox, _ = detector.detectAndDecode(img)

# bbox = None
# while bbox is None:
# 	state, img = cap.read()
# 	if state:
# 		print("QR code detected\n")
# 		data, bbox, _ = detector.detectAndDecode(img)
# 		print(f"ID:\n{data}")
# 		cap.release()
# 	else:
# 		print("No QR code detected\n")
# 		time.sleep(.5)


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

ev = event(data)
ev.db_connect()
ev.db_add_coffee()
ev.db_close()