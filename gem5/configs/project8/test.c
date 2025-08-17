#include <gem5/m5ops.h>

int main(){
    m5_start();
    printf("hello world\n");
    
    m5_exit(10000);
}