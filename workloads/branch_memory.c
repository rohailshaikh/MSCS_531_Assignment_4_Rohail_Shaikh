#include <stdint.h>
#include <stdio.h>

#define SIZE 8192
#define REPEATS 120

static volatile uint32_t data[SIZE];

int main(void) {
    uint32_t state = 1;
    int64_t total = 0;

    for (int i = 0; i < SIZE; ++i) {
        state = state * 1664525u + 1013904223u;
        data[i] = state;
    }

    for (int repeat = 0; repeat < REPEATS; ++repeat) {
        for (int i = 0; i < SIZE; ++i) {
            if (data[i] & 1u) {
                total += data[i];
            } else {
                total -= data[i];
            }
        }
    }

    printf("branch-memory result: %lld\n", (long long)total);
    return 0;
}

