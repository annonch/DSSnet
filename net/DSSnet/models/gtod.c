#include <sys/time.h>
#include <stdio.h>

long double gt(){

  struct timeval tv;
  
  time_t curtime;
  suseconds_t ms;
  long double res;

  gettimeofday(&tv, NULL);
  
  curtime=tv.tv_sec;
  ms=tv.tv_usec;

  //printf("%ld\n",(long)curtime);
  //printf("%ld\n",(long)ms);
  res = ((long double) curtime + (long double)ms/1000000.0);
  //printf("%Lf\n", res);
  return res;
}

int  main(){
  gt();
  return 0;
}
