#include <stdio.h>
#include <sys/time.h>  // for gettimeofday

// ANSI escape code for cyan
#define CYAN  "\033[36m"
#define RESET "\033[0m"

static double now_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1e6;
}

void interrupt_service_routine(void)
{
    printf(CYAN "[ISR] Interrupt detected! Starting simulated processing...\n" RESET);
    fflush(stdout);

    const int total_steps = 5;
    const double step_interval = 0.1; // seconds per step

    double t0 = now_sec();

    for (int step = 1; step <= total_steps; ++step) {
        // Wait until the target time for this step
        double target = t0 + step * step_interval;
        while (now_sec() < target) {
            // tiny busy work to avoid a totally tight loop
            for (volatile int i = 0; i < 10000; ++i) { }
        }

        printf(CYAN "[ISR] Processing step %d/%d...\n" RESET, step, total_steps);
        fflush(stdout);
    }

    printf(CYAN "[ISR] Finished ISR simulation.\n" RESET);
}

int main(void)
{
    interrupt_service_routine();
    printf(CYAN "interrupt processed now needs to be cleared...\n" RESET);
    return 0;
}
