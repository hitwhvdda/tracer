// https://books.google.co.kr/books?id=t2yA8vtfxDsC&pg=PT289&lpg=PT289&dq=full_read+header&source=bl&ots=4k2Dpq3L91&sig=ACfU3U3y7mxXqf4Ocu599v9JvBCu7cT9cw&hl=ko&sa=X&ved=2ahUKEwjiu8-k7uTxAhU7QPUHHbBqCdwQ6AEwD3oECBwQAw#v=onepage&q=full_read%20header&f=false

#include <arpa/inet.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct header {
  unsigned int length;
  unsigned int message_type;
};

char *read_packet(int sockfd) {
  unsigned int len;
  struct header hdr;
  static char buffer[1024];

  if (read(sockfd, (void *)&len, sizeof(hdr)) <= 0) {
    return NULL;
  }

  int length = ntohl(len);

  if (len > (1024 + sizeof(struct header) - 1)) {
    return NULL;
  }

  if (read(sockfd, buffer, length - sizeof(struct header)) <= 0) {
    return NULL;
  }

  buffer[sizeof(buffer) - 1] = '\0';

  return 0;
}
