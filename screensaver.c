#include <linux/fb.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>  // Include the string.h header for memset

int main() {
    int fb_fd = 0;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    long screensize = 0;
    char *fb_ptr = 0;

    fb_fd = open("/dev/fb0", O_RDWR);
    if (fb_fd == -1) {
        perror("Unable to open framebuffer");
        exit(EXIT_FAILURE);
    }

    if (ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo)) {
        perror("Failed to get fixed information");
        exit(EXIT_FAILURE);
    }

    if (ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo)) {
        perror("Failed to get variable information");
        exit(EXIT_FAILURE);
    }

    screensize = vinfo.yres_virtual * finfo.line_length;

    fb_ptr = (char *)mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, 0);
    if ((int)fb_ptr == -1) {
        perror("Failed to map framebuffer to memory");
        exit(EXIT_FAILURE);
    }

    // Clear the framebuffer to black
    memset(fb_ptr, 0, screensize);

    // Display a simple pattern
    int x, y;
    for (x = 0; x < vinfo.xres_virtual; x++) {
        for (y = 0; y < vinfo.yres_virtual; y++) {
            long location = (x + vinfo.xoffset) * (vinfo.bits_per_pixel / 8) +
                            (y + vinfo.yoffset) * finfo.line_length;
            int color = x * 255 / vinfo.xres_virtual;
            *((unsigned int *)(fb_ptr + location)) = (color << 16) | (color << 8) | color;
        }
    }

    munmap(fb_ptr, screensize);
    close(fb_fd);

    return 0;
}
