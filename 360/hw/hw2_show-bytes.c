#include <stdio.h>

typedef unsigned char *byte_pointer;

void show_bytes( byte_pointer start, int len )
{
	int i;
	for( i=0; i<len; i++ )
		printf(" %.2x", start[i]);
	printf( "\n" );
}

void show_int( int x )
{
	show_bytes( (byte_pointer)&x, sizeof(int) );
}

void show_float( float x )
{
	show_bytes( (byte_pointer)&x, sizeof(float));
}

void show_pointer( void *x )
{
	show_bytes( (byte_pointer) &x, sizeof(void *));
}

void test_show_bytes( int val )
{
	int ival = val;
	float fval = (float) ival;
	int *pval = &ival;

	printf("\tAs int: " ) ;
    show_int( ival );
	printf("\tAs float: " ) ;
	show_float( fval );
	printf("\tAs pointer: " ) ;
	show_pointer( pval );
}

int main( int argc, char * argv[] )
{
    printf("Decimal value 666:\n");
	test_show_bytes( 666 );

    printf("Hex value 0x666:\n");
	test_show_bytes( 0x666 );

    printf("Hex value 0x666:\n");
	test_show_bytes( 0x666 );
}