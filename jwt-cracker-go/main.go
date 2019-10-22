package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"

	jwt "github.com/dgrijalva/jwt-go"
)

func ValidateToken(tokenstring string, key string) bool {

	_, err := jwt.Parse(tokenstring, func(token *jwt.Token) (interface{}, error) {
		return []byte(key), nil
	})

	if err == nil {
		return true
	} else {
		return false
	}

}

func Worker(tokenstring string, key string) {
	if ValidateToken(tokenstring, key) {
		fmt.Println("[+] Key Found: " + key)
		os.Exit(0)
	}
}

func getWordlist(wordlistFile string) (*bufio.Scanner, error) {

	wordlist, err := os.Open(wordlistFile)
	if err != nil {
		return nil, fmt.Errorf("failed to open wordlist: %v", err)
	}

	_, err = wordlist.Seek(0, 0)
	if err != nil {
		return nil, fmt.Errorf("failed to rewind wordlist: %v", err)
	}
	return bufio.NewScanner(wordlist), nil
}

func main() {
	wordlist := flag.String("wordlist", "", "Wordlist.")
	tokenString := flag.String("token", "", "JWT Token.")
	flag.Parse()

	if _, err := os.Stat(*wordlist); os.IsNotExist(err) {
		fmt.Println("File does not exist.")
		os.Exit(1)
	}

	if *tokenString == "" {
		fmt.Println("JWT is not provided.")
		os.Exit(1)
	}

	scanner, _ := getWordlist(*wordlist)
	for scanner.Scan() {
		word := strings.TrimSpace(scanner.Text())
		Worker(*tokenString, word)

	}
        fmt.Println("Key not found...")
	os.Exit(0)
}
