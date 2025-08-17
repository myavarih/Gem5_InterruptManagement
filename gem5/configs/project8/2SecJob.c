#include <stdio.h>
#include <sys/time.h>

#define MAGENTA "\033[35m"
#define RESET   "\033[0m"

static double now_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1e6;
}

int main(void) {
    printf(MAGENTA "Processing steps...\n" RESET);
    fflush(stdout);

    double t0 = now_sec();
    double step_interval = 3.0 / 20.0;  // 0.15 seconds per step
    int steps = 0;

    while (steps < 10) {
        double t = now_sec() - t0;
        if (t >= steps * step_interval) {
            printf(MAGENTA "Step %d\n" RESET, steps + 1);
            fflush(stdout);
            steps++;
        }
        // prevent a tight busy loop
        for (volatile int i = 0; i < 10000; ++i) { }
    }

    printf(MAGENTA "Done!\n" RESET);
    return 0;
}
