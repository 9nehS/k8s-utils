#!/usr/bin/env python

import argparse
import signal
import subprocess
import sys

SIGNAL_RECEIVED = 0
CMD_KUBECTL_GET_POD = 'kubectl get --no-headers=true pods -o custom-columns=:metadata.name'
CMC_KUBECTL_LOGS_PARTIAL = 'kubectl logs -f '
POD_LIST = None


def signal_handler(signal, frame):
    global SIGNAL_RECEIVED
    SIGNAL_RECEIVED = 1


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pod', dest='pod', help='Pod name for logs to be displayed', required=True)
    args = parser.parse_args()
    return args


def pod_name_check(args):
    global POD_LIST
    POD_LIST = subprocess.check_output(CMD_KUBECTL_GET_POD, shell=True)
    pod_name_list = filter(None, POD_LIST.split('\n'))
    return True if args.pod in pod_name_list else False


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    args = get_parser()
    if not pod_name_check(args):
        print "Pod with name '%s' is not in pod list, please check!" % args.pod
        print 'Current pod list:'
        print POD_LIST
        sys.exit(1)

    while True:
        if SIGNAL_RECEIVED == 1:
            # print 'SIGNAL_RECEIVED: 1'
            sys.exit(0)
        # os.system('kubectl logs -f meteor-3592645122-wxbtg')
        p = subprocess.Popen(CMC_KUBECTL_LOGS_PARTIAL + args.pod, shell=True)
        p.wait()
        # print 'SIGNAL_RECEIVED value:', SIGNAL_RECEIVED


if __name__ == '__main__':
    main()
