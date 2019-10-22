package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/korovkin/limiter"
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

func getWordlist(wordlist_file string) (*bufio.Scanner, error) {

	wordlist, err := os.Open(wordlist_file)
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
	max_threads := flag.Int("max-threads", 10, "Threads.")
	flag.Parse()

	if _, err := os.Stat(*wordlist); os.IsNotExist(err) {
		fmt.Println("File does not exist.")
		os.Exit(1)
	}

	if *max_threads > 1000000 {
		fmt.Println("Input threads exceeded.")
		os.Exit(1)
	}

	if *tokenString == "" {
		fmt.Println("JWT is not provided.")
		os.Exit(1)
	}

	scanner, _ := getWordlist(*wordlist)
	for scanner.Scan() {
		limit := limiter.NewConcurrencyLimiter(*max_threads)

		limit.Execute(func() {
			word := strings.TrimSpace(scanner.Text())
			Worker(*tokenString, word)
		})

		limit.Wait()
	}
}
