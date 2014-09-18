#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import pynotify
import sys
import argparse
import time

def parse_arguements():
    """
    parse the given arguements.
    """
    parser = argparse.ArgumentParser(description="""Shows notification via libnotify in the given periods. Will repead until finished.""")
    parser.add_argument('workingtime', 
        nargs=1,
        type=int,
        help="time to focus on work in minutes.")
    parser.add_argument('freetime', 
        nargs=1, 
        type=int,
        help="Time to prokrastinate in minutes")
    return parser.parse_args()

def countdown(seconds=60):
    headline = "Freetime will end"
    text = "Freetime will end in %s seconds"
    n = None
    for i in xrange(seconds):
        if n is None:
            n = pynotify.Notification(headline, text % (seconds -i))
        else:
            n.update(headline, text % (seconds -i))
        n.show()
        time.sleep(1)

def loop(args):
    n = pynotify.Notification("Worktime!", "In %s minutes begins your next freetime." % args.workingtime) 
    n.show()
    while True:
        time.sleep(args.workingtime*60)
        n = pynotify.Notification("Freetime!", "Freetime begins. You have %s minutes left" % args.freetime)
        n.show()
        time.sleep((args.freetime-1)*60)
        countdown()
        n = pynotify.Notification("Worktime!", "Freetime ends. In %s minutes begins your next freetime." % args.workingtime) 
        n.show()

def main():
    if not pynotify.init("Basics"):
        return
    args = parse_arguements()
    args.workingtime = args.workingtime[0]
    args.freetime = args.freetime[0]

    loop(args)

if __name__ == "__main__":
    main()