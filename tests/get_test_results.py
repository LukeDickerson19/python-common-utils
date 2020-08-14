import sys

TEST_RESULTS_FILE = './results.txt'

# return 1 if any of the tests failed, 0 otherwise
f = open(TEST_RESULTS_FILE, 'r')
ret = 0
for line in f.readlines():
    if line.split(' ')[-1] == 'FAILURE\n':
        ret = 1
        break
f.close()
sys.exit(ret)
