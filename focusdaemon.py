#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import pynotify
import sys
import argparse
import time
import datetime

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
            n = send_notification(headline, text % (seconds -i))
        else:
            n.update(headline, text % (seconds -i))
            n.show()
        time.sleep(1)

def send_notification(header, text):
    """
        sends a notification and return the object for later use (updates etc)
    """
    if not pynotify.init("Basics"):
        return None
    n = pynotify.Notification(header, text) 
    n.show()
    print datetime.datetime.now().isoformat(), header, text
    return n

def _get_time_in(minutes, seperator=":"):
    """
        return the clocktime in the given minutes from now
    """
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=minutes)
    end = now + delta
    return seperator.join(map(lambda x: str(x).zfill(2), [end.hour, end.minute]))

def loop(args):

    send_notification("Worktime!", "At %s in %s minutes begins your next freetime." % (_get_time_in(args.workingtime),args.workingtime)) 
    while True:
        time.sleep(args.workingtime*60)
        send_notification("Freetime!", "Freetime begins. You have %s minutes left" % args.freetime)
        time.sleep((args.freetime-1)*60)
        countdown()
        send_notification("Worktime!", "At %s in %s minutes begins your next freetime." % (_get_time_in(args.workingtime),args.workingtime)) 

def main():
    if not pynotify.init("Basics"):
        return
    args = parse_arguements()
    args.workingtime = args.workingtime[0]
    args.freetime = args.freetime[0]

    loop(args)

if __name__ == "__main__":
    main()