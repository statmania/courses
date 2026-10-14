# include <stdio.h>

int main (void){
    int x, y, z, sum;
    printf("Enter the first number\n");
    scanf("%d", &x);
    printf("Enter another number\n");
    scanf("%d", &y);
    printf("Enter the last number\n");
    scanf("%d", &z);
    sum = x + y + z;
    printf("The sum is %d\n", sum);

    return 0;
}
