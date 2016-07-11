#include <stdint.h>

/* 
Compute CRC-CCITT. *Message is a pointer to the first character in the 
message; MessLen is the number of characters in the message (not 
counting the 
CRC on the end) */ 
uint16_t ComputeCRC(unsigned char *Message, unsigned char MessLen) 
{ 
   uint16_t crc=0xFFFF; 
   uint16_t temp; 
   uint16_t quick; 
   int     i; 
   for(i=0;i<MessLen;i++) 
   { 
      temp = (crc>>8) ^ Message[i]; 
      crc <<= 8; 
      quick = temp ^ (temp >> 4); 
      crc ^= quick; 
      quick <<=5; 
      crc ^= quick; 
      quick <<= 7; 
      crc ^= quick; 
   } 
   return crc; 
} 
