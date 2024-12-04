package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"unicode"
)

const (
	ALPHABET_SIZE = 26
	CHAN_SIZE     = 1 << 15
	EXIT_CODE     = 10010
)

func getRegisterIndex(reg string) int {
	runes := []rune(reg)
	if unicode.IsLower(runes[0]) {
		return int(reg[0]) - 97
	}
	return -1
}

type computer struct {
	registers []int
	sendChan  chan int
	recvChan  chan int
	finished  chan int
	id        int
	numSends  int
	iPtr      int
	program   [][]string
	recvLock  *sync.Mutex
}

func NewComputer(startPValue int, program [][]string, finished, sendChan, recvChan chan int, recvMutex *sync.Mutex) *computer {
	registers := make([]int, ALPHABET_SIZE)
	registers[int('p')-97] = startPValue
	return &computer{
		registers,
		sendChan,
		recvChan,
		finished,
		startPValue,
		0,
		0,
		program,
		recvMutex,
	}
}

func (comp *computer) PrintStatus() {
	fmt.Printf("%v %v\n", comp.id, comp.numSends)
}

func (comp *computer) Value(operand string) int {
	regIndex := getRegisterIndex(operand)
	if regIndex >= 0 {
		return comp.registers[regIndex]
	} else {
		val, _ := strconv.Atoi(operand)
		return val
	}
}

func (comp *computer) ExecRecvDeadLocked(reg int) bool {
	acquired := comp.recvLock.TryLock()
	if acquired {
		defer comp.recvLock.Unlock()
		received := <-comp.recvChan
		comp.registers[reg] = received
		if received == EXIT_CODE {
			comp.sendChan <- EXIT_CODE
			return true
		}
		return false
	} else {
		comp.sendChan <- EXIT_CODE
		return true
	}
}

func (comp *computer) Run() {
	numInstructions := len(comp.program)
	for ; comp.iPtr >= 0 && comp.iPtr < numInstructions; comp.iPtr++ {
		if comp.id == 1 {
			fmt.Println(comp.numSends)
		}
		instr := comp.program[comp.iPtr]
		switch instr[0] {
		case "snd":
			comp.sendChan <- comp.Value(instr[1])
			comp.numSends++
		case "rcv":
			x := getRegisterIndex(instr[1])
			if comp.ExecRecvDeadLocked(x) {
				break
			}
		case "set":
			x := getRegisterIndex(instr[1])
			y := comp.Value(instr[2])
			comp.registers[x] = y
		case "add":
			x := getRegisterIndex(instr[1])
			y := comp.Value(instr[2])
			comp.registers[x] += y
		case "mul":
			x := getRegisterIndex(instr[1])
			y := comp.Value(instr[2])
			comp.registers[x] *= y
		case "mod":
			x := getRegisterIndex(instr[1])
			y := comp.Value(instr[2])
			comp.registers[x] %= y
		case "jgz":
			x := comp.Value(instr[1])
			if x > 0 {
				y := comp.Value(instr[2])
				comp.iPtr += y - 1
			}
		}
	}

	fmt.Printf("id = %v\n", comp.id)
	comp.finished <- 0
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	instructions := make([][]string, 0)

	for scanner.Scan() {
		instruction := strings.Split(scanner.Text(), " ")
		instructions = append(instructions, instruction)
	}

	// 0 -> 1
	chan_01 := make(chan int, CHAN_SIZE)
	// 1 -> 0
	chan_10 := make(chan int, CHAN_SIZE)

	finished := make(chan int)

	recvMutex := sync.Mutex{}

	computer0 := NewComputer(0, instructions, finished, chan_01, chan_10, &recvMutex)
	computer1 := NewComputer(1, instructions, finished, chan_10, chan_01, &recvMutex)

	go computer0.Run()
	go computer1.Run()

	<-finished
	<-finished
}
