import schedule
import time
import server


def mail():
    print "sending mail"

schedule.every().day.at("13:10").do(server.check_best_before)

while True:
    schedule.run_pending()
    time.sleep(1)


