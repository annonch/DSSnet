#include "pmu.h"
#pragma pack(1)


void swap(char *p, int len)
{
  int i;
  char tmp;
  for(i = 0; i < len/2; i++)
    {
      tmp = p[len-i-1];
      p[len-i-1] = p[i];
      p[i] = tmp;
    }
}


int cfg2(uint16_t idcode, char message_time_quality, uint16_t num_pmu,
	 char* stn, uint16_t idcode2, uint16_t format, uint16_t phnmr,
	 uint16_t annmr, uint16_t dgnmr, char* chnam, void* phunit,
	 void* anunit, void* digunit, uint16_t fnom, uint16_t cfgcnt,
	 uint16_t data_rate, uint32_t time_base, char* pdc_IP, int pdc_port)
{
  uint16_t sync=(uint16_t)43569;
  uint16_t size;
  void *data = malloc(65535);
  char *ptr, *ptr_size;
  ptr=data;

  //field 1 sync
  *(uint16_t*)ptr = sync;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 2 framesize
  // we cant really know at this time
  ptr+=sizeof(uint16_t);

  //field 3 idcode
  *(uint16_t*)ptr = idcode;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);

  //field 4 soc
  struct timespec tms;
  if(clock_gettime(CLOCK_REALTIME,&tms))
    return -1;
  *(uint32_t*)ptr = (uint32_t)tms.tv_sec;
  swap(ptr,sizeof(uint32_t));
  ptr+=sizeof(uint32_t);

  //field 5 fracsec
  ptr += (sizeof(char));
  *(uint16_t*)ptr = (uint16_t)tms.tv_nsec * data_rate;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);
  *ptr = message_time_quality;
  ptr += (sizeof(char));

  //field 6 timebase
  *(uint32_t*)ptr=time_base;
  swap(ptr,sizeof(uint32_t));
  ptr += sizeof(uint32_t);

  //field 7 num_pmu
  *(uint16_t*)ptr=num_pmu;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 8 stn
  strncpy(ptr,stn,16);
  ptr+=sizeof(char)*16;

  //field 9 idcode
  *(uint16_t*)ptr = idcode2;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 10 format
  *(uint16_t*)ptr = format;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 11 phnmr
  *(uint16_t*)ptr = phnmr;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 12 annmr
  *(uint16_t*)ptr = annmr;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 13 dgnmr
  *(uint16_t*)ptr = dgnmr;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 14 channel names
  memcpy(ptr,chnam,16*(phnmr+annmr+(16*dgnmr)));
  ptr += 16*(phnmr+annmr+(16*dgnmr));

  //field 15 phunit
  memcpy(ptr,phunit,4*phnmr);
  int k;
  for(k=0;k<phnmr;k++){
    swap(ptr,sizeof(uint32_t));
    ptr += sizeof(uint32_t);
  }
  //field 16 anunit
  if(annmr){
    memcpy(ptr,anunit,4*annmr);
    for(k=0;k<annmr;k++){
      swap(ptr,sizeof(uint32_t));
      ptr += sizeof(uint32_t);
    }
  }
  if(dgnmr){
    //field 17 digunit
    memcpy(ptr,digunit,4*dgnmr);
    for(k=0;k<dgnmr;k++){
      swap(ptr,sizeof(uint32_t));
      ptr += sizeof(uint32_t);
    }
  }
  //fnom
  *(uint16_t*)ptr = fnom;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);

  //cfgcnt
  *(uint16_t*)ptr = cfgcnt;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);

  *(uint16_t*)ptr = data_rate;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);


  //field 2 size
  size = ptr-(char*)data+2;
  ptr_size = data;
  ptr_size += sizeof(uint16_t);
  *(uint16_t*)ptr_size = size;
  swap(ptr_size,sizeof(uint16_t));
  ptr_size+=sizeof(uint16_t);

  //field 21+ crciit
  uint16_t crc;
  crc=ComputeCRC(data,size-2);
  *(uint16_t*)ptr = crc;
  swap(ptr,2);


  // send data to ip
  struct  sockaddr_in si_other;
  int s, slen=sizeof(si_other);

  if ((s=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP))==-1)
    printf("socket");

  //printf(pdc_IP);

  memset((char *) &si_other, 0, sizeof(si_other));
  si_other.sin_family = AF_INET;
  si_other.sin_port = htons(pdc_port);
  //printf(pdc_IP);
  if (inet_aton(pdc_IP, &si_other.sin_addr)==0) {
    fprintf(stderr, "inet_aton() failed\n");
    exit(1);
  }
  int j;
  for (j=0; j<NPACK; j++) {
    printf("Sending cfg2\n");
    //printf(cfg1r, "This is packet %d\n", j);
    if (sendto(s, data, (size), 0, (struct sockaddr *)&si_other, slen)==-1)
      printf("sendto()");
  }

  close(s);
  free(data);
  // end
  return 0;
}

int data(uint16_t idcode, char message_time_quality, uint16_t num_pmu,
	 char* stn, uint16_t idcode2, uint16_t format, uint16_t phnmr,
	 uint16_t annmr, uint16_t dgnmr, char* chnam, void* phunit,
	 void* anunit, void* digunit, uint16_t fnom, uint16_t cfgcnt,
	 uint16_t data_rate, uint32_t time_base, char* pdc_IP,
         int pdc_port,
         uint16_t stat, void* phasor_data, void* analog_data,
         void* digital_data, void* freq_data, void* dfreq_data)
{
  uint16_t sync=(uint16_t)0xAA01;
  uint16_t size;
  void *data = malloc(65535);
  char *ptr;
  ptr=data;

  /* format flags */
  int format_freq_dfreq = format & 0x08;
  int format_analog = format & 0x04;
  int format_phasors = format & 0x02;

  // field 1 sync
  *(uint16_t*)ptr = sync;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 2 framesize
  size = 16;
  if(format_phasors){
    size += 8 * phnmr;
  }
  else{
    size += 4 * phnmr;
  }
  if(format_freq_dfreq){
    size += 8;
  }
  else{
    size += 4;
  }
  if(format_analog){
    size += 4 * annmr;
  }
  else{
    size += 2 * annmr;
  }
  size += 2 * dgnmr;
  size += 2;

  *(uint16_t*)ptr = size;
  swap(ptr,sizeof(uint16_t));
  ptr += sizeof(uint16_t);

  //field 3 idcode
  *(uint16_t*)ptr = idcode;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);

  //field 4 soc
  struct timespec tms;
  if(clock_gettime(CLOCK_REALTIME,&tms))
    return -1;
  *(uint32_t*)ptr = (uint32_t)tms.tv_sec;
  swap(ptr,sizeof(uint32_t));
  ptr+=sizeof(uint32_t);

  //field 5 fracsec
  ptr += (sizeof(char));
  *(uint16_t*)ptr = (uint16_t)tms.tv_nsec * data_rate;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);
  *ptr = message_time_quality;
  ptr += (sizeof(char));

  //field 6 stat
  *(uint16_t*)ptr = stat;
  swap(ptr,sizeof(uint16_t));
  ptr+=sizeof(uint16_t);

  int i;

  //field 7 phasors
  if(format_phasors){
    memcpy(ptr,phasor_data,8*phnmr);
    for(i=0;i<phnmr*2;i++){
      swap(ptr,4);
      ptr += 4;
    }
  }
  else {
    memcpy(ptr,phasor_data,4*phnmr);
    for(i=0;i<phnmr*2;i++){
      swap(ptr,2);
      ptr += 2;
    }
  }

  //field 8 freq field 9 dfreq
  if(format_freq_dfreq) {
    memcpy(ptr,freq_data,4);
    swap(ptr,sizeof(uint32_t));
    ptr+=sizeof(uint32_t);
    memcpy(ptr,dfreq_data,4);
    swap(ptr,sizeof(uint32_t));
    ptr+=sizeof(uint32_t);
  }
  else{
    memcpy(ptr,freq_data,2);
    swap(ptr,sizeof(uint16_t));
    ptr+=sizeof(uint16_t);
    memcpy(ptr,dfreq_data,2);
    swap(ptr,sizeof(uint16_t));
    ptr+=sizeof(uint16_t);
  }

  //field 10 analog
  if(annmr){
    if(format_analog){
      memcpy(ptr,analog_data,4*annmr);
      for(i=0;i<annmr;i++){
	swap(ptr,4);
	ptr += 4;
      }
    }
    else {
      memcpy(ptr,analog_data,2*annmr);
      for(i=0;i<annmr;i++){
	swap(ptr,sizeof(uint16_t));
	ptr += sizeof(uint16_t);
      }
    }
  }

  //field 11 digital
  if(dgnmr) {
    memcpy(ptr,digital_data,2*dgnmr);
    for(i=0;i<dgnmr;i++){
      swap(ptr,sizeof(uint16_t));
      ptr += sizeof(uint16_t);
    }
  }

  //field 12 + crciit
  uint16_t crc;
  crc=ComputeCRC(data,size-2);
  *(uint16_t*)ptr = crc;
  swap(ptr,2);


  // send data to ip
  struct  sockaddr_in si_other;
  int s, slen=sizeof(si_other);

  if ((s=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP))==-1)
    printf("socket");


  memset((char *) &si_other, 0, sizeof(si_other));
  si_other.sin_family = AF_INET;
  si_other.sin_port = htons(pdc_port);
  if (inet_aton(pdc_IP, &si_other.sin_addr)==0) {
    fprintf(stderr, "inet_aton() failed\n");
    exit(1);
  }

  for (i=0; i<NPACK; i++) {
    printf("Sending data packet\n");
    //printf(cfg1r, "This is packet %d\n", i);
    if (sendto(s, data, (size), 0, (struct sockaddr *)&si_other, slen)==-1)
      printf("sendto()");
  }

  close(s);
  // end
  // free
  free(data);
  return 0;
}

/*
int main(){
  // uint16_t idcode, num_pmu, idcode2, format, phnmr,annmr,dgnmr,fnom,cfgcnt, data_rate;
  char message_time_quality;
  int pdc_port;

  const uint16_t idcode = 1000;
  const uint16_t idcode2 = 1000;
  const uint16_t num_pmu=1;
  const uint16_t format=0x0F;
  const uint16_t phnmr=4;
  const uint16_t annmr=0;
  const uint16_t dgnmr=0;
  const uint16_t fnom=0;
  uint32_t time_base, phunit[phnmr], anunit[annmr],digunit[dgnmr];
  const uint16_t cfgcnt=0;
  const uint16_t data_rate=30;
  message_time_quality=0x0;
  phunit[0]=0;
  phunit[1]=0;
  phunit[2]=0;
  phunit[3]=0x01000000;

  //anunit=0;
  //digunit=0;
  time_base=1;
  char stn[16];
  char chnam[] = "VA              VB              VC              IA              ";
  char pdc_IP[12];
  strncpy(stn,"Base Station 1",16);
  strncpy(pdc_IP,"10.47.142.26  ",14);
  pdc_port = 4712;
  printf("calling cfg2\n");


  cfg2(idcode,message_time_quality,num_pmu,stn,idcode2,
       format,phnmr,annmr,dgnmr,chnam,phunit,anunit,
       digunit,fnom,cfgcnt,data_rate,time_base,pdc_IP,pdc_port);


  uint16_t stat;

  // format flags
  //int format_freq_dfreq = format & 0x08;
  int format_analog = format & 0x04;
  int format_phasors = format & 0x02;


  float phasor_data[2*phnmr];


  uint16_t analog_data[2*annmr];
  uint16_t freq_data[2];
  uint16_t dfreq_data[2];
  uint16_t digital_data[dgnmr];

  //my data

  stat=0;

  phasor_data[0] = 0;
  phasor_data[1] = 0;
  phasor_data[2] = 0;
  phasor_data[3] = 0;
  phasor_data[4] = 0;
  phasor_data[5] = 0;
  phasor_data[6] = 0;
  phasor_data[7] = 0;

  phasor_data[0] = 7199.36;
  phasor_data[1] = 0.1;
  phasor_data[2] = 7199.37;
  phasor_data[3] = -3.14*2/3;
  phasor_data[4] = 7199.36;
  phasor_data[5] = 3.14*2/3;
  phasor_data[6] = 334.51;
  phasor_data[7] = -0.6225;


  //digital_data;
  *(float*)freq_data=0;
  *(float*)dfreq_data=0;

  data(idcode,message_time_quality,num_pmu,stn,idcode2,
       format,phnmr,annmr,dgnmr,chnam,phunit,anunit,
       digunit,fnom,cfgcnt,data_rate,time_base,pdc_IP,pdc_port,
       stat, phasor_data, analog_data, digital_data, freq_data,
       dfreq_data   );
  return 0;

}
*/

void cfg2_python(int pdc_port_p,int idcode_p, int message_time_quality_p, int format_p,
                     char* stn_p, int phnmr_p, int annmr_p, int dgnmr_p,
                     char* chnam_p, char* phunit_p, char* anunit_p,
                     char* digunit_p, int fnom_p, int cfgcnt_p, int data_rate_p,
                     int time_base_p, char* pdc_IP_p) {

  //printf("hi\n");

  uint16_t idcode_c = (uint16_t)idcode_p;
  char message_time_quality_c = (char)message_time_quality_p;
  uint16_t format_c = (uint16_t)format_p;

  //printf("hi2\n");

  void* stn_c = malloc(16);
  memcpy(stn_c, stn_p,16);

  uint16_t phnmr_c = (uint16_t)phnmr_p;
  uint16_t annmr_c = (uint16_t)annmr_p;
  uint16_t dgnmr_c = (uint16_t)dgnmr_p;

  //printf("hi3\n");


  void* chnam_c = malloc(16 * (phnmr_p + annmr_p + 16 * dgnmr_p));
  memcpy(chnam_c,chnam_p,16 * (phnmr_p + annmr_p + 16 * dgnmr_p));

  void* phunit_c = malloc(phnmr_p*4);
  memcpy(phunit_c,phunit_p,phnmr_p*4);

  void* anunit_c = malloc(annmr_p*4);
  memcpy(anunit_c,anunit_p,annmr_p*4);

  void* digunit_c = malloc(dgnmr_p*4);
  memcpy(digunit_c,digunit_p,dgnmr_p);

  //printf("hi4\n");


  uint16_t fnom_c = (uint16_t)fnom_p;
  uint16_t cfgcnt_c = (uint16_t)cfgcnt_p;
  uint16_t data_rate_c = (uint16_t)data_rate_p;

  uint32_t time_base_c = time_base_p;

  void* pdc_IP_c = malloc(15);
  memcpy(pdc_IP_c,pdc_IP_p,15);

  int pdc_port_c = pdc_port_p;

  //printf("hi5\n");

  //send the message
  cfg2(idcode_c, message_time_quality_c, 1,
       stn_c, idcode_c, format_c, phnmr_c,
       annmr_c, dgnmr_c, chnam_c, phunit_c,
       anunit_c, digunit_c, fnom_c, cfgcnt_c,
       data_rate_c, time_base_c, pdc_IP_c, pdc_port_c);

  free(stn_c);
  free(chnam_c);
  free(pdc_IP_c);
  free(phunit_c);
  free(anunit_c);
  free(digunit_c);


}




void data_python(int pdc_port_p, int idcode_p, int message_time_quality_p, int format_p,
                 char* stn_p, int phnmr_p, int annmr_p, int dgnmr_p,
                 char* chnam_p, char* phunit_p, char* anunit_p,
                 char* digunit_p, int fnom_p, int cfgcnt_p, int data_rate_p,
                 int time_base_p, char* pdc_IP_p,
                 char* phasor_data_p, char* analog_data_p,
                 char* digital_data_p, float freq_data_p, float dfreq_data_p){

  const uint16_t stat_c = 0;

  uint16_t idcode_c = (uint16_t)idcode_p;
  char message_time_quality_c = (char)message_time_quality_p;
  uint16_t format_c = (uint16_t)format_p;

  //printf("hi2\n");

  void* stn_c = malloc(16);
  memcpy(stn_c, stn_p,16);

  uint16_t phnmr_c = (uint16_t)phnmr_p;
  uint16_t annmr_c = (uint16_t)annmr_p;
  uint16_t dgnmr_c = (uint16_t)dgnmr_p;

  //printf("hi3\n");


  void* chnam_c = malloc(16 * (phnmr_p + annmr_p + 16 * dgnmr_p));
  memcpy(chnam_c,chnam_p,16 * (phnmr_p + annmr_p + 16 * dgnmr_p));

  void* phunit_c = malloc(phnmr_p*4);
  memcpy(phunit_c,phunit_p,phnmr_p*4);

  void* anunit_c = malloc(annmr_p*4);
  memcpy(anunit_c,anunit_p,annmr_p*4);

  void* digunit_c = malloc(dgnmr_p*4);
  memcpy(digunit_c,digunit_p,dgnmr_p);

  //printf("hi3.5\n");

  void* phasor_data_c = malloc(phnmr_p*8);
  memcpy(phasor_data_c,phasor_data_p,phnmr_p*8);

  //printf("hi3.58\n");

  void* analog_data_c = malloc(annmr_p*4);
  memcpy(analog_data_c,analog_data_p,annmr_p*4);

  void* digital_data_c = malloc(dgnmr_p*4);
  memcpy(digital_data_c,digital_data_p,dgnmr_p*4);

  //printf("hi3.75\n");

  float freq_data_c = freq_data_p;
  float dfreq_data_c = dfreq_data_p;

  //printf("hi4\n");

  uint16_t fnom_c = (uint16_t)fnom_p;
  uint16_t cfgcnt_c = (uint16_t)cfgcnt_p;
  uint16_t data_rate_c = (uint16_t)data_rate_p;

  uint32_t time_base_c = time_base_p;

  void* pdc_IP_c = malloc(15);
  memcpy(pdc_IP_c,pdc_IP_p,15);

  int pdc_port_c = pdc_port_p;

  //printf("hi5\n");

  //send the message
  data(idcode_c, message_time_quality_c, 1,
       stn_c, idcode_c, format_c, phnmr_c,
       annmr_c, dgnmr_c, chnam_c, phunit_c,
       anunit_c, digunit_c, fnom_c, cfgcnt_c,
       data_rate_c, time_base_c, pdc_IP_c, pdc_port_c,
       stat_c, phasor_data_c, analog_data_c, digital_data_c,
       &freq_data_c, &dfreq_data_c);

  free(stn_c);
  free(chnam_c);
  free(pdc_IP_c);
  free(phunit_c);
  free(anunit_c);
  free(digunit_c);
  free(phasor_data_c);
  free(analog_data_c);
  free(digital_data_c);
  //free(freq_data_c);
  //free(dfreq_data_c);
}
