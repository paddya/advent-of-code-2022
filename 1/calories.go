package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	contents, _ := os.ReadFile(os.Args[1])
	blocks := strings.Split(string(contents), "\n\n")

	sums := []int{}
	for _, block := range blocks {
		lines := strings.Split(block, "\n")
		sum := 0
		for _, l := range lines {
			num, _ := strconv.Atoi(l)
			sum += num
		}
		sums = append(sums, sum)
	}

	sort.Slice(sums, func(i int, j int) bool {
		return sums[i] > sums[j]
	})

	fmt.Println(sums[0])
	fmt.Println(sums[0] + sums[1] + sums[2])
}
