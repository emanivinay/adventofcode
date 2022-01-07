package main

import "fmt"

func puzzle(values []int, gap int) int {
  N := len(values)
  ret := 0
  for i := 0;i + gap < N; i++ {
    if values[i] < values[i + gap] {
      ret++
    }
  }

  return ret
}

func main() {
  values := make([]int, 0)

  for {
    var val int

    _, err := fmt.Scanf("%d", &val)
    if err != nil {
      break
    }

    values = append(values, val)
  }

  fmt.Println("%d %d", puzzle(values, 1), puzzle(values, 3))
}
