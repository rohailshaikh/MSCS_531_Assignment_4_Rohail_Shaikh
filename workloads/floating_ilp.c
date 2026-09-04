#include <stdio.h>

int main(void) {
    double a = 1.0, b = 2.0, c = 3.0, d = 4.0;

    for (int i = 0; i < 150000; ++i) {
        a = a * 1.000001 + 0.25;
        b = b * 1.000002 + 0.50;
        c = c * 1.000003 + 0.75;
        d = d * 1.000004 + 1.00;
    }

    printf("floating result: %.3f\n", a + b + c + d);
    return 0;
}

