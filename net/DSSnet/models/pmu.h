#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/uio.h>
#include <arpa/inet.h>
#include <sys/types.h>

#include "crc.c"


#define SRV_IP "10.47.142.26"
#define NPACK 1
#define PORT 4712

//void data(int numPMU, uint16_t  id, int rate,int *phnmr, int *annmr,int *dgnmr, uint16_t *stat, uint32_t *phasors, uint16_t *freq, uint16_t *dfreq, uint16_t *analog, uint16_t *digital);
