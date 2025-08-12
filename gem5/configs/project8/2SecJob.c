#include <stdio.h>
#include <time.h>

#define MAGENTA "\033[35m"
#define RESET "\033[0m"

int main() {
    clock_t start_time = clock();
    double elapsed_time = 0.0;
    int dots = 0;

    printf(MAGENTA "Processing" RESET);

    // Loop for ~2 seconds showing animated dots in magenta
    while (elapsed_time < 2.0) {
        elapsed_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;

        int new_dots = (int)(elapsed_time / 0.4);
        if (new_dots > dots) {
            for (int i = 0; i < new_dots - dots; i++) {
                printf(MAGENTA "." RESET);
                fflush(stdout);
            }
            dots = new_dots;
        }
    }

    printf("\n" MAGENTA "Done! That took about %.2f seconds.\n" RESET, elapsed_time);
    return 0;
}
