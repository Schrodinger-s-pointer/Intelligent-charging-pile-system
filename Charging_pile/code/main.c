#include <gtk/gtk.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "sjk.h"
GtkWidget *window_main;

static guint time_tag = 0;
static guint count = 10;

int T_count_1 = 0;
int T_count_2 = 0;
int timer = 0;
char A_1[100] = "00.00A", V_1[100] = "00.00V", W_1[100] = "00.00W", T_1[100] = "00:00:00", Q_1[100] = "00.00kWh";
char A_2[100] = "00.00A", V_2[100] = "00.00V", W_2[100] = "00.00W", T_2[100] = "00:00:00", Q_2[100] = "00.00kWh";
int K_1 = 0;
int K_2 = 0;
GtkWidget *charge_A_value_1;
GtkWidget *charge_V_value_1;
GtkWidget *charge_T_value_1;
GtkWidget *charge_S_value_1;
GtkWidget *charge_W_value_1;
GtkWidget *charge_Q_value_1;
GtkWidget *charge_A_value_2;
GtkWidget *charge_V_value_2;
GtkWidget *charge_T_value_2;
GtkWidget *charge_S_value_2;
GtkWidget *charge_W_value_2;
GtkWidget *charge_Q_value_2;
int lock01 = 0;
int lock02 = 0;
char *addr01 = "01";
char *addr02 = "02";
char table_name01[20] = "";
char num01[20] = "";
char table_name02[20] = "";
char num02[20] = "";
//设置label的字体大小
void set_font_size_rgb(GtkWidget *widget, gint size, char *rgb_name);

gint deal_time(gpointer data)
{

    timer++;

    if (lock01 == 0 && select_power(addr01) == 1)
    {
        select_date(table_name01);
        printf("table_name:%s\n", table_name01);

        select_num(addr01, num01);
        printf("num:%s\n", num01);

        K_1 = check_pay_kwh(addr01, table_name01, num01);
        lock01 = 1;
    }
    else if (check_power(addr01, table_name01, num01) == 1 && lock01 == 1)
    {
        T_count_1++;
        char T_1[15] = {0};
        sprintf(T_1, "%02d:%02d:%02d", T_count_1 / 60 / 60 % 60, T_count_1 / 60 % 60, T_count_1 % 60);
        char T_Value_1[100] = "";
        gtk_label_set_text(GTK_LABEL(charge_T_value_1), T_1);

        if (T_count_1 % 5 > 2||T_count_1<=1)
        {
            check_four(addr01, table_name01, num01, V_1, A_1, W_1, Q_1);
            float kwh = strtod(Q_1, NULL);
            printf("kwh%lf,\n", kwh);
            float w = strtod(W_1, NULL);
            printf("w%lf,\n", w);
            int q = K_1 - kwh;
            printf("K_2%d,\n", K_1);
            printf("q%d,\n", q);
            int t = q / w * 60;
            printf("t%d,\n", t);
            char s_t[10] = {0};
            if (t>0){sprintf(s_t, "%d分", t);}
            else{sprintf(s_t, "计算中");}
            gtk_label_set_text(GTK_LABEL(charge_S_value_1), s_t);

            gtk_label_set_text(GTK_LABEL(charge_A_value_1), A_1);
            gtk_label_set_text(GTK_LABEL(charge_V_value_1), V_1);
            gtk_label_set_text(GTK_LABEL(charge_W_value_1), W_1);
            gtk_label_set_text(GTK_LABEL(charge_Q_value_1), Q_1);
        }
    }

    else if (check_power(addr01, table_name01, num01) == 0)
    {
        T_count_1 = 0;
        lock01 = 0;
        char temp[100] = "空闲中";
        gtk_label_set_text(GTK_LABEL(charge_A_value_1), temp);
        gtk_label_set_text(GTK_LABEL(charge_V_value_1), temp);
        gtk_label_set_text(GTK_LABEL(charge_W_value_1), temp);
        gtk_label_set_text(GTK_LABEL(charge_Q_value_1), temp);
        gtk_label_set_text(GTK_LABEL(charge_S_value_1), temp);
        gtk_label_set_text(GTK_LABEL(charge_T_value_1), "未充电");
    }

    //二号机

    if (lock02 == 0 && select_power(addr02) == 1)
    {
        select_date(table_name02);
        printf("table_name:%s\n", table_name02);

        select_num(addr02, num02);
        printf("num:%s\n", num02);
        K_2 = check_pay_kwh(addr02, table_name02, num02);
        printf("K_2:%d\n", K_2);
        lock02 = 1;
    }
    else if (check_power(addr02, table_name02, num02) == 1 && lock02 == 1)
    {
        T_count_2++;
        char T_2[15] = {0};
        sprintf(T_2, "%02d:%02d:%02d", T_count_2 / 60 / 60 % 60, T_count_2 / 60 % 60, T_count_2 % 60);
        char T_Value_2[100] = "";
        gtk_label_set_text(GTK_LABEL(charge_T_value_2), T_2);

        if (T_count_2 % 5 > 2||T_count_2<=1)
        {
            check_four(addr02, table_name02, num02, V_2, A_2, W_2, Q_2);
            float kwh = strtod(Q_2, NULL);
            printf("kwh%lf,\n", kwh);
            float w = strtod(W_2, NULL);
            printf("w%lf,\n", w);
            int q = K_2 - kwh;
            printf("K_2%d,\n", K_2);
            printf("q%d,\n", q);
            int t = q / w * 60;
            printf("t%d,\n", t);
            char s_t[10] = {0};
            if (t>0){sprintf(s_t, "%d分", t);}
            else{sprintf(s_t, "计算中");}
            gtk_label_set_text(GTK_LABEL(charge_S_value_2), s_t);

            gtk_label_set_text(GTK_LABEL(charge_A_value_2), A_2);
            gtk_label_set_text(GTK_LABEL(charge_V_value_2), V_2);
            gtk_label_set_text(GTK_LABEL(charge_W_value_2), W_2);
            gtk_label_set_text(GTK_LABEL(charge_Q_value_2), Q_2);
        }
    }

    else if (check_power(addr02, table_name02, num02) == 0)
    {
        T_count_2 = 0;
        lock02 = 0;
        char temp[100] = "空闲中";
        gtk_label_set_text(GTK_LABEL(charge_A_value_2), temp);
        gtk_label_set_text(GTK_LABEL(charge_V_value_2), temp);
        gtk_label_set_text(GTK_LABEL(charge_W_value_2), temp);
        gtk_label_set_text(GTK_LABEL(charge_Q_value_2), temp);
        gtk_label_set_text(GTK_LABEL(charge_S_value_2), temp);
        gtk_label_set_text(GTK_LABEL(charge_T_value_2), "未充电");
    }

    return TRUE;
}

void load_image(GtkWidget *image, const char *file_path, const int w, const int h)
{
    gtk_image_clear(GTK_IMAGE(image));                                                       // 清除图像
    GdkPixbuf *src_pixbuf = gdk_pixbuf_new_from_file(file_path, NULL);                       // 创建图片资源
    GdkPixbuf *dest_pixbuf = gdk_pixbuf_scale_simple(src_pixbuf, w, h, GDK_INTERP_BILINEAR); // 指定大小
    gtk_image_set_from_pixbuf(GTK_IMAGE(image), dest_pixbuf);                                // 图片控件重新设置一张图片(pixbuf)
    g_object_unref(src_pixbuf);                                                              // 释放资源
    g_object_unref(dest_pixbuf);                                                             // 释放资源
}

void my_window_init()
{
    window_main = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_widget_set_size_request(window_main, 1024, 600);
    gtk_window_set_title(GTK_WINDOW(window_main), "充电页面");
    g_signal_connect(window_main, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    GtkWidget *table = gtk_table_new(10, 10, TRUE);
    gtk_container_add(GTK_CONTAINER(window_main), table);

     GtkWidget *label_title_1 = gtk_label_new("1号充电桩        |        2号充电桩");
     set_font_size_rgb(label_title_1, 18, "#FFCCCC");
     gtk_table_attach_defaults(GTK_TABLE(table), label_title_1, 0, 10, 1, 2);

     GtkWidget *label_title_2 = gtk_label_new("扫码开启充电之旅");
     set_font_size_rgb(label_title_2, 18, "#FFCCCC");
     gtk_table_attach_defaults(GTK_TABLE(table), label_title_2, 0, 10, 8, 9);

     GtkWidget *charge_A_1 = gtk_label_new("充电电流");
     set_font_size_rgb(charge_A_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_A_1, 0, 2, 2, 3);

     GtkWidget *charge_V_1 = gtk_label_new("充电电压");
     set_font_size_rgb(charge_V_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_V_1, 2, 3, 2, 3);

     GtkWidget *charge_T_1 = gtk_label_new("充电时间");
     set_font_size_rgb(charge_T_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_T_1, 0, 2, 6, 7);

     GtkWidget *charge_S_1 = gtk_label_new("剩余时间");
     set_font_size_rgb(charge_S_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_S_1, 2, 3, 6, 7);

     GtkWidget *charge_W_1 = gtk_label_new("充电功率");
     set_font_size_rgb(charge_W_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_W_1, 2, 3, 4, 5);

     GtkWidget *charge_Q_1 = gtk_label_new("充电电量");
     set_font_size_rgb(charge_Q_1, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_Q_1, 0, 2, 4, 5);

     GtkWidget *charge_A_2 = gtk_label_new("充电电流");
     set_font_size_rgb(charge_A_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_A_2, 8, 10, 2, 3);

     GtkWidget *charge_V_2 = gtk_label_new("充电电压");
     set_font_size_rgb(charge_V_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_V_2, 7, 8, 2, 3);

     GtkWidget *charge_T_2 = gtk_label_new("充电时间");
     set_font_size_rgb(charge_T_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_T_2, 8, 10, 6, 7);

     GtkWidget *charge_S_2 = gtk_label_new("剩余时间");
     set_font_size_rgb(charge_S_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_S_2, 7, 8, 6, 7);

     GtkWidget *charge_W_2 = gtk_label_new("充电功率");
     set_font_size_rgb(charge_W_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_W_2, 7, 8, 4, 5);

     GtkWidget *charge_Q_2 = gtk_label_new("充电电量");
     set_font_size_rgb(charge_Q_2, 18, "#99CCFF");
     gtk_table_attach_defaults(GTK_TABLE(table), charge_Q_2, 8, 10, 4, 5);

    // 输入

    charge_A_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_A_value_1, 18, "#B25132");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_A_value_1, 0, 2, 2, 4);

    charge_V_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_V_value_1, 18, "#B25132");

    gtk_table_attach_defaults(GTK_TABLE(table), charge_V_value_1, 2, 3, 2, 4);

    charge_T_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_T_value_1, 18, "#B25132");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_T_value_1, 0, 2, 6, 8);

    charge_S_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_S_value_1, 18, "#B25132");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_S_value_1, 2, 3, 6, 8);

    charge_W_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_W_value_1, 18, "#B25132");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_W_value_1, 2, 3, 4, 6);

    charge_Q_value_1 = gtk_label_new("");
    set_font_size_rgb(charge_Q_value_1, 18, "#B25132");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_Q_value_1, 0, 2, 4, 6);

    // 输入sql值

    charge_A_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_A_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_A_value_2, 8, 10, 2, 4);

    charge_V_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_V_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_V_value_2, 7, 8, 2, 4);

    charge_T_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_T_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_T_value_2, 8, 10, 6, 8);

    charge_S_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_S_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_S_value_2, 7, 8, 6, 8);

    charge_W_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_W_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_W_value_2, 7, 8, 4, 6);

    charge_Q_value_2 = gtk_label_new("");
    set_font_size_rgb(charge_Q_value_2, 18, "#1618B2");
    gtk_table_attach_defaults(GTK_TABLE(table), charge_Q_value_2, 8, 10, 4, 6);

    GtkWidget *image_code = gtk_image_new_from_pixbuf(NULL);
    load_image(image_code, "./image/code.png", 250, 250); // 修改二维码  *
    // load_image(image_code, "./image/code.png", 250, 312); // 修改二维码  *
    gtk_table_attach_defaults(GTK_TABLE(table), image_code, 1, 9, 2, 9);

    GtkWidget *image_back = gtk_image_new_from_pixbuf(NULL);
    load_image(image_back, "./image/bjtp.png", 1024, 600); // 修改背景    *
    gtk_table_attach_defaults(GTK_TABLE(table), image_back, 0, 10, 0, 10);
}

int main(int argc, char **argv)
{
    //初始化 gtk
    gtk_init(&argc, &argv);
    my_window_init();
    //全部都显示
    time_tag = g_timeout_add(1000, (GSourceFunc)deal_time, NULL);
    gtk_widget_show_all(window_main);
    gtk_main();

    return 0;
}

//设置label的字体大小
void set_font_size_rgb(GtkWidget *widget, gint size, char *rgb_name)
{
    PangoFontDescription *font;
    gint fontSize = size;
    GdkColor color;
    gdk_color_parse(rgb_name, &color);

    gtk_widget_modify_text(GTK_WIDGET(widget), GTK_STATE_NORMAL, &color);
    gtk_widget_modify_bg(GTK_WIDGET(widget), GTK_STATE_NORMAL, &color); //背景色
    gtk_widget_modify_fg(GTK_WIDGET(widget), GTK_STATE_NORMAL, &color); //前景色

    font = pango_font_description_from_string("Sans");             //"Sans"字体名
    pango_font_description_set_size(font, fontSize * PANGO_SCALE); //设置字体大小

    //设置label的字体
    gtk_widget_modify_font(GTK_WIDGET(widget), font);
    pango_font_description_free(font);
}
