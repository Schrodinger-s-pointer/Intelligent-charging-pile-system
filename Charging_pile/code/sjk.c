// #include <gtk/gtk.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "sjk.h"

char* select_date(char* count)
{
    printf("查询最新表中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char *table_name="sqlite_master";
	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select count(*) from \'%s\';",table_name);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("查询最新表出错：%s\n", errmsg);
	if(r!=0)
	{
        int cou=atoi(table[1]);
        printf("cou%d\n",cou);
        if (cou==2)
        {
            cou=1;
        }
        
        sprintf(sql_dl_zh,"select * from \'%s\';",table_name);
	    r = 0,c = 0;
        table = NULL;
	    sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
        strcpy(count,table[5*cou+1]);
        sqlite3_free_table(table);
        sqlite3_close(db);

        return count;
	}
	if(r==0)
	{
        printf("查询最新表失败...\n");
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}

char* select_num(char *addr,char *num)
{
    printf("查询序号中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);


    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    
    char mac_name[30]=""; 
    strcat(mac_name,addr);
    strcat(mac_name,":CD:20:22:55:4F");
    printf("mac_name:%s\n",mac_name);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select * from \'%s\'where mac=\'%s\' order by num desc limit 1;",table_name,mac_name);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("查询序号出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table_num:%s\n", table[10*1+1]);

        strcpy(num,table[10*1+1]);
        sqlite3_free_table(table);
        sqlite3_close(db);

        return num;
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        sqlite3_close(db);
        printf("查询序号失败...\n");
        return 0;
	}
}

int select_power(char *addr)
{
    printf("查询开关状态中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    char num[20]="";
    select_num(addr,num);
    printf("num:%s\n",num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select power from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("查询开关状态出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        char power[10]="";
        int state=-1;
        if(table[1]!=NULL)
        {
            if (strcmp(table[1],"1")==0)
            {
                strcpy(power,table[1]);
                state=atoi(power);
            }
            else
            {   strcpy(power,"0");
                state=atoi(power);
            }
        }
        else
        {
            strcpy(power,"0");
            state=atoi(power);
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return state;
	}
	if(r==0)
	{
        printf("查询开关状态失败...\n");
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}
int check_power(char *addr,char *table_name,char *num)
{
    printf("检查开关状态中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select power from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("检查开关状态出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        char power[10]="";
        int state=-1;
        if(table[1]!=NULL)
        {
            if (strcmp(table[1],"1")==0)
            {
                strcpy(power,table[1]);
                state=atoi(power);
            }
            else
            {   strcpy(power,"0");
                state=atoi(power);
            }
        }
        else
        {
            strcpy(power,"0");
            state=atoi(power);
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return state;
	}
	if(r==0)
	{
        printf("检查开关状态失败...\n");
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}
int check_pay_kwh(char *addr,char *table_name,char *num)
{
    printf("检查已经购买的总电量中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select kwh from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("检查已经购买的总电量出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        char paykwh[10]="";
        int state=-1;
        if(table[1]!=NULL)
        {
                strcpy(paykwh,table[1]);
                state=atoi(paykwh);
        }
        else
        {
            strcpy(paykwh,"0");
            state=atoi(paykwh);
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return state;
	}
	if(r==0)
	{
        printf("检查已经购买的总电量失败...\n");
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}

char* select_voltage(char *addr,char* voltage)
{
    printf("查询电压中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    char num[20]="";
    select_num(addr,num);
    printf("num:%s\n",num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select voltage from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        if(table[1]!=NULL)
        {
            strcpy(voltage,table[1]);
        }
        else
        {
            strcpy(voltage,"0");
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return voltage;
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}

char* select_current(char *addr,char* current)
{
    printf("查询电流中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    char num[20]="";
    select_num(addr,num);
    printf("num:%s\n",num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select current from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        if(table[1]!=NULL)
        {
            strcpy(current,table[1]);
        }
        else
        {
            strcpy(current,"0");
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return current;
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}

char* select_watt(char *addr,char* watt)
{
    printf("查询功率中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    char num[20]="";
    select_num(addr,num);
    printf("num:%s\n",num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select watt from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        if(table[1]!=NULL)
        {
            strcpy(watt,table[1]);
        }
        else
        {
            strcpy(watt,"0");
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return watt;
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}


char* select_quantity(char *addr,char* quantity)
{
    printf("查询电量中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);
    printf("table_name:%s\n",table_name);

    char num[20]="";
    select_num(addr,num);
    printf("num:%s\n",num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select quantity from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("出错：%s\n", errmsg);
	if(r!=0)
	{
        printf("table:%s\n", table[1]);
        if(table[1]!=NULL)
        {
            strcpy(quantity,table[1]);
        }
        else
        {
            strcpy(quantity,"0");
        }
        sqlite3_free_table(table);
        sqlite3_close(db);
        return quantity;
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        sqlite3_close(db);
        return 0;
	}
}





char* select_four(char *addr,char* voltage,char* current,char* watt,char* quantity)
{
    printf("查询四个状态值中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

    char table_name[20]="";
    select_date(table_name);

    char num[20]="";
    select_num(addr,num);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select voltage ,current, watt, quantity from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("出错：%s\n", errmsg);
	if(r!=0)
	{

        printf("voltage:%s\n", table[4*1+0]);
        printf("current:%s\n", table[4*1+1]);
        printf("watt:%s\n", table[4*1+2]);
        printf("quantity:%s\n", table[4*1+3]);


        char *state[4]={voltage,current,watt,quantity};
        for (int i=0;i<4;i++)
        {
        if(table[4*1+i]!=NULL)
        {
            strcpy(state[i],table[4*1+i]);
        }
        else
        {
            strcpy(state[i],"0");
        }

        }
        sqlite3_free_table(table);
        sqlite3_close(db);

        return "1";
	}
	if(r==0)
	{   sqlite3_free_table(table);
        sqlite3_close(db);

        return 0;
	}
}
char* check_four(char *addr,char *table_name,char *num,char* voltage,char* current,char* watt,char* quantity)
{
    printf("检查四个状态值中...\n");
	sqlite3*db;
	sqlite3_open("cd.db",&db);

	char sql_dl_zh[200]  = "";
	sprintf(sql_dl_zh,"select voltage ,current, watt, quantity from \'%s\'where num=\'%s\';",table_name,num);
	char **table = NULL;
	char* errmsg = NULL;
	int r = 0,c =0;
	sqlite3_get_table(db,sql_dl_zh,&table,&r,&c,&errmsg);
	if(errmsg!=NULL)
		printf("检查四个状态值出错：%s\n", errmsg);
	if(r!=0)
	{

        printf("voltage:%s\n", table[4*1+0]);
        printf("current:%s\n", table[4*1+1]);
        printf("watt:%s\n", table[4*1+2]);
        printf("quantity:%s\n", table[4*1+3]);

        char *state[4]={voltage,current,watt,quantity};
        for (int i=0;i<4;i++)
        {
        if(table[4*1+i]!=NULL)
        {
            strcpy(state[i],table[4*1+i]);
           
            
        }
        else
        {
            
            strcpy(state[i],"0");
        }

        }
        sqlite3_free_table(table);
        sqlite3_close(db);

        return "1";
	}
	if(r==0)
	{
        sqlite3_free_table(table);
        printf("检查四个状态值失败...\n" );
        sqlite3_close(db);
        return 0;
	}
}
