# jwt-mimicker.py
# Returns the decoded value of a JWT.
import json
import jwt
import sys


def main():
    if len(sys.argv) <= 1:
        sys.stdout.write("\t-::: jwt-decoder.py :::-\n")
        sys.stdout.write("# Returns the decoded value  of a JWT.\n")
        sys.stdout.write("\nUsage: %s [jwt-token]\n" % (sys.argv[0]))
        sys.stdout.flush()
        exit(0)

    jwt_token = sys.argv[1]
    jwt_token_header = jwt.get_unverified_header(jwt_token)
    jwt_token_value = jwt.decode(jwt_token, verify=False)
    sys.stdout.write("\n\n")
    sys.stdout.write("[#] JWT Header:\n%s\n\n" %
                     (json.dumps(jwt_token_header)))
    sys.stdout.write("[#] JWT Value:\n%s\n" % (json.dumps(jwt_token_value)))
    sys.stdout.flush()
    exit(0)


if __name__ == "__main__":
    main()
