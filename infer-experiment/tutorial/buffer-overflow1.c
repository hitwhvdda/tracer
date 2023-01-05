// https://owasp.org/www-community/attacks/Buffer_Overflow_via_Environment_Variables

#include <stdio.h>
#include <stdlib.h>

int main(void) {
  char *ptr_h;
  char h[64];

  ptr_h = getenv("HOME");
  if (ptr_h != NULL) {
    sprintf(h, "Your home directory is: %s !", ptr_h);
    printf("%s\n", h);
  }

  return 0;
}
