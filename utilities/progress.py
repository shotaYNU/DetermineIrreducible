import math
import sys

class progress:
    MAX = 100
    MAX_LEN = 30

    def __init__(self):
        self.current = 0.0
    def flush_progress(self, progress):
        sys.stderr.write('\r\033[K' + self.get_progressbar_str(progress))
        sys.stderr.flush()
    def end_flush(self):
        sys.stderr.write('\n')
        sys.stderr.flush()
    def get_progressbar_str(self, progress):
        bar_len = int(self.MAX_LEN * progress)
        return ('[' + '=' * bar_len + ('>' if bar_len < self.MAX_LEN else '') + ' ' * (self.MAX_LEN - bar_len) + '] %.1f%%' % (progress * 100.))
