package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
)

var tokenstring string
var wg sync.WaitGroup

func validateToken(tokenstring string, key string) bool {
	_, err := jwt.Parse(tokenstring, func(token *jwt.Token) (interface{}, error) {
		return []byte(key), nil
	})

	if err == nil {
		return true
	} else {
		return false
	}
}

func worker(key string) {
	if validateToken(tokenstring, key) {
		fmt.Printf("[+] Key Found: %s\n", key)
		os.Exit(0)
	}
}

func runner(ch *chan string) {
	wg.Add(1)
	for word := range *ch {
		worker(word)
	}
	wg.Done()

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
	workers := flag.Int("workers", 100, "Workers count.")

	flag.Parse()

	if _, err := os.Stat(*wordlist); os.IsNotExist(err) {
		fmt.Println("File does not exist.")
		os.Exit(1)
	}
	if *workers < 0 {
		fmt.Println("Invalid workers count.")
		os.Exit(1)
	}

	if *tokenString == "" {
		fmt.Println("JWT is not provided.")
		os.Exit(1)
	}
	scanner, err := getWordlist(*wordlist)
	if err != nil {
		fmt.Printf("Error Reading wordlist. %v\n", err)
		os.Exit(1)
	}

	tokenstring = *tokenString
	ch := make(chan string)

	for i := 0; i < *workers; i++ {
		go runner(&ch)
	}

	for scanner.Scan() {
		word := strings.TrimSpace(scanner.Text())
		ch <- word
	}

	go func() {
		wg.Add(1)
		for {
			if len(ch) == 0 {
				close(ch)
				break
			}
			time.Sleep(100 * time.Millisecond)
		}
		wg.Done()
	}()
	wg.Wait()
	fmt.Println("Key not found...")
}
