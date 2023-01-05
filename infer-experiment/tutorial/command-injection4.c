// https://owasp.org/www-community/attacks/Command_Injection

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  char command[256];

  if (argc != 2) {
    printf("Error: Please enter a program to time!\n");
    return -1;
  }

  memset(&command, 0, sizeof(command));

  strcat(command, "time ./");
  strcat(command, argv[1]);

  system(command);
  return 0;
}
