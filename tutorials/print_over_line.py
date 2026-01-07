import time
import sys

SLEEP_TIME = 1

sys.stdout.write('.')
# sys.stdout.flush()
time.sleep(SLEEP_TIME)
sys.stdout.write('\r..')
# sys.stdout.flush()
time.sleep(SLEEP_TIME)
sys.stdout.write('\r...')
# sys.stdout.flush()
time.sleep(SLEEP_TIME)
sys.stdout.write('\r....')
# sys.stdout.flush()
time.sleep(SLEEP_TIME)
