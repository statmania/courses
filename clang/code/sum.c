#include <stdio.h>

int main(void) {
    int x, y, z;
    printf("Enter the first number\n");
    scanf("%d", &x);
    printf("Enter another number\n");
    scanf("%d", &y);
    printf("Enter the last number\n");
    scanf("%d", &z);

    int sum = x + y + z;
    printf("The sum is %d\n", sum);

    double mean = (x + y + z) / 3.0;
    printf("The mean is %f\n", mean);   // %f, not %d

    return 0;
}
