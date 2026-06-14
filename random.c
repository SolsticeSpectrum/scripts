#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/ioctl.h>

#define SLEEP_MS 100
#define NUM_COLORS 7
#define COLOR_PROBABILITY 5

const char* colors[NUM_COLORS] = {
    "\x1B[31m",  // Red
    "\x1B[32m",  // Green
    "\x1B[33m",  // Yellow
    "\x1B[34m",  // Blue
    "\x1B[35m",  // Magenta
    "\x1B[36m",  // Cyan
    "\x1B[37m"   // White
};

int main() {
    srand(time(NULL));

    while (1) {
        struct winsize w;
        ioctl(0, TIOCGWINSZ, &w);

        int rows = w.ws_row;
        int cols = w.ws_col;

        int num_elements = rows * cols;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                int random_num = rand() % 10;
                const char* color;

                if (rand() % 100 < COLOR_PROBABILITY) {
                    int color_index = rand() % NUM_COLORS;  // Multi color
                    color = colors[color_index];
                    //color = "\x1B[32m";  // Green
                } else {
                    color = "\x1B[90m";  // Gray
                }

                printf("\033[%d;%dH%s%d\033[0m", i + 1, j + 1, color, random_num);
            }
        }

        fflush(stdout);
        usleep(SLEEP_MS*1000);
    }

    return 0;
}
