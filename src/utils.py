from datetime import datetime


TIME_FRMT_LOG = '%H:%M:%S'

def print_log(time_frmt, msg):
    print('[{}] {}'.format(datetime.now().strftime(time_frmt), msg))
