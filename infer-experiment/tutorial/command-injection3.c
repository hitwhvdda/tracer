// https://owasp.org/www-community/attacks/Command_Injection

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define INITCMD "init"

int main() {
  char *home = getenv("APPHOME");
  char *cmd = (char *)malloc(strlen(home) + strlen(INITCMD));
  if (cmd) {
    strcpy(cmd, home);
    strcat(cmd, INITCMD);
    execl(cmd, NULL);
  }
}
