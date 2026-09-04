#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint64_t a = 1, b = 3, c = 5, d = 7;

    for (uint64_t i = 0; i < 200000; ++i) {
        a = a * 3 + i;
        b = b * 5 + i;
        c = c * 7 + i;
        d = d * 11 + i;
    }

    printf("integer result: %" PRIu64 "\n", a + b + c + d);
    return 0;
}

