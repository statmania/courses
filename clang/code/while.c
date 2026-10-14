#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Even numbers from 1 to 10
// SOme problems are taken from https://www.statmania.info/blog/posts/c-while-loop-practice-problems.html

int main (void){
  int i = 2; // first even
  while (i <= 10){
    printf("%d\n", i);
    i += 2;
  }

  // USe modulus

  // Write a program that uses a while loop to print the multiplication table of 5, from 5 × 1 to 5 × 10.

  int prod = 1;
  int mult;
  printf("The multiplication table is given below:\n");
  while (prod <= 10){
    mult = 5 * prod;
    printf("5  × %d = %d\n", prod, mult);
    prod++;
  }

  // Write a program that reads a number from the user and uses a while loop to compute its factorial. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120.

  // First test 1 to 10

  int num;
  printf("Enter a number\n");
  if (scanf("%d", &num) != 1 || num < 0){
    printf("Please enter a non-negative number.\n");
  };
  int fact = 1;
  i = num;
  while(i > 1){
    fact *= i;
    i--;
  }
  printf("%d! = \n", fact);


  return 0;
}

