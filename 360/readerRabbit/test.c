#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>
// Homework #6
// -
// Easy Reader Controller
// CS 3 6 0  Winter 2 0 1 7
// Purpose:
// To gain familiarity with fork()
// and exec()POSIX functions and familiarity with signals
// through the use of sigaction(), kill(), waitpid(), and custom handlers.


int main(){
	pid_t pid;
	char path[] = {"./reader"};
	
	char* txt = malloc(sizeof(char)*100);
	printf("%s\n", "Enter a file name: ");
	scanf("%99s", txt);

    char* parmList[] = {path, txt, NULL};

    if ((pid = fork()) == -1)
       perror("fork error");
    else if (pid == 0) {
       execv(path, parmList);

		struct termios info;
		tcgetattr(0, &info);          /* get current terminal attirbutes; 0 is the file descriptor for stdin */
		info.c_lflag &= ~ICANON;      /* disable canonical mode */
		info.c_cc[VMIN] = 1;          // wait until at least one keystroke available 
		info.c_cc[VTIME] = 0;         /* no timeout */
		tcsetattr(0, TCSANOW, &info); /* set immediately */

		int ch;
		while((ch = getchar()) != 'q' /* ascii q */) {
			if (ch < 0) {
				if (ferror(stdin)) { /* there was an error... */ }
				clearerr(stdin);
			/* do other stuff */
			} else {
				/* some key OTHER than q was hit, do something about it? */
				
				
			}
		}

		exit();

		printf("Return not expected. Must be an execv error.n");
    }

    free(txt);

	tcgetattr(0, &info);
	info.c_lflag |= ICANON;
	tcsetattr(0, TCSANOW, &info);

	return 0;
}
