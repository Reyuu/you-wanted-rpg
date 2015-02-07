#ansi must be enabled!
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"


def disable():
    del HEADER
    del OKBLUE
    del OKGREEN
    del WARNING
    del FAIL
    del ENDC


def green(msg):  # green
    print OKGREEN + msg + ENDC


def blue(msg):  # blue
    print OKBLUE + msg + ENDC


def yellow(msg):  # yellow
    print WARNING + msg + ENDC


def red(msg):  # red
    print FAIL + msg + ENDC