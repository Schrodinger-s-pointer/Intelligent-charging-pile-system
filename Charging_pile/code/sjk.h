#ifndef __SJK_H_
#define __SJK_H_ 
#include "sqlite3.h"

char* select_date(char* count);
char* select_num(char *addr,char *num);
int select_power(char *addr);
int check_power(char *addr,char *table_name,char *num);
int check_pay_kwh(char *addr,char *table_name,char *num);
char* select_voltage(char *addr,char* voltage);
char* select_current(char *addr,char* current);
char* select_watt(char *addr,char* watt);
char* select_quantity(char *addr,char* quantity);
char* select_four(char *addr,char* voltage,char* current,char* watt,char* quantity);
char* check_four(char *addr,char *table_name,char *num,char* voltage,char* current,char* watt,char* quantity);

#endif