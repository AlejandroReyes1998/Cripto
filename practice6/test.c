#include <string.h>
#include <stdio.h>
int main(){
    unsigned char A[100],B[100],C[100];
    A[0] =  '1';
    B[0] =  '0';
    C[0] =  '0';
    memcpy(A + 1, B, 1);
    memcpy(A + 1, C, 1);
    printf(A);
    return 0;
}
