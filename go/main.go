package main

import (
	"fmt"
	"time"
)

var INITIAL_INDEX int

type Token struct {
	data string
	recipient, ttl int 
}

type Node struct {
	id   int
	input <-chan Token
	output chan<- Token
}

func (node *Node) shareMsg(){
	for {
		msg := <- node.input
	
		if node.id == msg.recipient {
		  fmt.Println("Node #", node.id, " got the msg '", msg.data, "' time to live -", msg.ttl)
		  fmt.Println("Done!")
		  return
		}
	
		if msg.ttl == 0 {
			fmt.Println("There's no lifetime, ttl = ", msg.ttl)
			return
		}
		
		fmt.Println("Node #", node.id, " shares the token")
		msg.ttl--
		node.output <- msg
	  }
}

func run(N int, initToken Token) {
	INITIAL_INDEX = 0
	channels := make([]chan Token, N)

	for i := 0; i < N; i++ {
		channels[i] = make(chan Token)
	}

	nodes := make([]Node, N)

	for i := 0; i < N; i++ {
		if i != (N - 1) {
			nodes[i] = Node{id : i, input : channels[i], output: channels[i + 1]}
			go nodes[i].shareMsg()
		} else {
			nodes[i] = Node{id: i, input: channels[i], output: channels[0]}
			go nodes[i].shareMsg()
		}
	}
	
	channels[INITIAL_INDEX] <- initToken

}

func main() {
	var N, ttl int
	var msg string
	fmt.Println("Enter nodes number")
	fmt.Scanln(&N)

	recipient := -1

	for !(recipient >= 0 && recipient < N) {
		fmt.Println("Choose the recipient node from 0 to ", N)
		fmt.Scanln(&recipient)
	}
	
	fmt.Println("Enter ttl")
	fmt.Scanln(&ttl)
	fmt.Println("Enter message to share")
	fmt.Scanln(&msg)


	initToken := Token{data: msg, recipient: recipient, ttl: ttl}
	fmt.Println("Init node #", INITIAL_INDEX)

	run(N, initToken)

	time.Sleep(time.Minute)
}