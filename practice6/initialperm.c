#include <stdio.h>
#include<string.h>

//Total = 8+64+2+64+64=202 bytes D:

void imprimepermutacion(unsigned int array[]);
//https://www.avrfreaks.net/forum/convert-unsigned-char-ascii
int main(){
	//Palabra original
	unsigned char m[]={'D','i','a','m','a','n','t','e'};//8 bytes
	unsigned char minv[]={0xff,0x40,0xe9,0x9e,0x00,0xfe,0x2a,0x20};//8 bytes 
	//Matriz de permutación
	unsigned char matrix[]={58,50,42,34,26,18,10,2,
							60,52,44,36,28,20,12,4, 
							62,54,46,38,30,22,14,6,
							64,56,48,40,32,24,16,8,
							57,49,41,33,25,17,9,1,
							59,51,43,35,27,19,11,3,
							61,53,45,37,29,21,13,5,
							63,55,47,39,31,23,15,7};//64 bytes
							
	unsigned char matrixinv[]={40,8,48,16,56,24,64,32,
							   39,7,47,15,55,23,63,31, 
							   38,6,46,14,54,22,62,30,
							   37,5,45,13,53,21,61,29,
							   36,4,44,12,52,20,60,28,
							   35,3,43,11,51,19,59,27,
							   34,2,42,10,50,18,58,26,
							   33,1,41,9,49,17,57,25};//64 bytes
	//Contadores y contenedores
	unsigned char i=0,num=0 /*,res=0,mod=0,rec=0*/;//1 byte c/u (2 total)
	
	//Arreglo donde va la cadena permutada, sin representación
	unsigned char temp[64]={0};//64 bytes
	
	//Arreglo para impresión hexadecimal
	unsigned int initialperm[16]={0};//64 bytes
	
	//Arreglo para impresión hexadecimal
	unsigned int initialperminv[16]={0};//64 bytes
	
	//Impresión de diamante en hexadecimal
	printf("Diamante = 0x");
	for(i;i<8;i++){
		printf(" %x", m[i]);
	}
	printf("\n");
	i=0;
	
	//Impresión de la permutación
	printf("Permutacion\n");
	printf("--------------------\n");
	for(i;i<64;i++){//32
		//res=matrix[i]/8;
		//mod=matrix[i]%8;
		//printf("Res %d\n", res);
		//printf("Mod %d\n", mod);
		//printf("-----------------------");
		//https://stackoverflow.com/questions/18327439/printing-binary-representation-of-a-char-in-c
		if(matrix[i]%8==0){
			temp[i] = !!((m[(matrix[i]/8)-1] << (7)) & 0x80);	
		}else{
			temp[i] = !!((m[matrix[i]/8] << ((matrix[i]%8)-1)) & 0x80);
		}
		//temp[i]=rec;				
		printf("%d", temp[i]);
		if(i%8==3)printf("-");
		if(i%8==7)printf("\n");
	}
	printf("--------------------\n");
	
	//"Conversión" en dígitos de 4 bits para su posterior representación en hexadecimal
	i=4;
	for(i;i<65;i+=4){//Se ejecuta 16 veces
		initialperm[num]=((int)temp[i-4])*1000+((int)temp[i-3])*100+((int)temp[i-2])*10+((int)temp[i-1]);
		num++;
	}
	
	//Impresión del resultado en hexadecimal
	printf("IP(Diamante)= 0x ");
	imprimepermutacion(initialperm);
	//unsigned int tam=sizeof(rec);
	//printf("%d",tam);
	printf("\n");
	
	i=0;
	printf("IP(IP-1)\n");
	printf("--------------------\n");
	for(i;i<64;i++){//32
		if(matrixinv[i]%8==0){
			temp[i] = !!((minv[(matrixinv[i]/8)-1] << (7)) & 0x80);	
		}else{
			temp[i] = !!((minv[matrixinv[i]/8] << ((matrixinv[i]%8)-1)) & 0x80);
		}
		//temp[i]=rec;				
		printf("%d", temp[i]);
		if(i%8==3)printf("-");
		if(i%8==7)printf("\n");
	}
	printf("--------------------\n");
		//"Conversión" en dígitos de 4 bits para su posterior representación en hexadecimal
	i=4;
	num=0;
	for(i;i<65;i+=4){//Se ejecuta 16 veces
		initialperminv[num]=((int)temp[i-4])*1000+((int)temp[i-3])*100+((int)temp[i-2])*10+((int)temp[i-1]);
		num++;
	}
	printf("IP(IP-1)= 0x ");
	imprimepermutacion(initialperminv);
	//unsigned int tam=sizeof(rec);
	//printf("%d",tam);
	printf("\n");
	
	return 0;	
}

//Para propósitos generales
void imprimepermutacion(unsigned int array[]){
	unsigned char i=0;
	for(i;i<16;i++){
		if(array[i]==0){printf("0");
    	}else if(array[i]==1){printf("1");
    	}else if(array[i]==10){printf("2");
    	}else if(array[i]==11){printf("3");
    	}else if(array[i]==100){printf("4");
    	}else if(array[i]==101){printf("5");
    	}else if(array[i]==110){printf("6");
    	}else if(array[i]==111){printf("7");
    	}else if(array[i]==1000){printf("8");
    	}else if(array[i]==1001){printf("9");
    	}else if(array[i]==1010){printf("a");
    	}else if(array[i]==1011){printf("b");
    	}else if(array[i]==1100){printf("c");
    	}else if(array[i]==1101){printf("d");
    	}else if(array[i]==1110){printf("e");
    	}else if(array[i]==1111){printf("f");
    	}
    	if(i%2==1)printf(" ");
	}
	printf("\n");	
}
