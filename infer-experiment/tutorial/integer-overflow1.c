// https://cwe.mitre.org/data/definitions/190.html

#include <stdlib.h>

int main() {
  int nresp = packet_get_int();
  if (nresp > 0) {
    void *response = malloc(nresp * sizeof(char *));
  }
}
