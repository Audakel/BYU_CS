#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>
#include <ncurses.h>
#include <fcntl.h>
#include <signal.h>

// Homework #6
// -
// Easy Reader Controller
// CS 3 6 0  Winter 2 0 1 7
// Purpose:
// To gain familiarity with fork()
// and exec()POSIX functions and familiarity with signals
// through the use of sigaction(), kill(), waitpid(), and custom handlers.
int key_hit(int pid);
void fork_();


void fork_(){
	char path[] = {"./reader"};
	char* txt = malloc(sizeof(char)*100);

	char welcome[] = "---Welcome to the speed reader controller!\n\
Use the following hot keys to control your experience\n \
        [s]tart new book\n \
        [p]ause playback\n \
        [r]esume playback\n \
        [+] speed up\n \
        [-] slow down\n \
        [q]uit \n\
Please enter the path to a text file to read\n";


	printf("%s\n", welcome);
	scanf("%99s", txt);
    char* parmList[] = {path, txt, NULL};

    pid_t pid = fork();

    if (pid < 0){
       printf("%s\n", "bad fork");
    }

    if (pid == 0) {
		execv(path, parmList);
    }
    else {
		while(1){
			key_hit(pid);
			continue;
		}
    }

	free(txt);

}


int key_hit(int pid){
	struct termios oldt, newt;
	int ch;
	int oldf;

	tcgetattr(STDIN_FILENO, &oldt);
	newt = oldt;
	newt.c_lflag &= ~(ICANON | ECHO);
	tcsetattr(STDIN_FILENO, TCSANOW, &newt);
	oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
	fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

	ch = getchar();

	tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
	fcntl(STDIN_FILENO, F_SETFL, oldf);

	switch(ch){
		case 's' :
			kill(pid, SIGKILL);
			fork_();
			break;
		case 'q' :
			kill(pid, SIGKILL);
			break;
		case 'p' :
			kill(pid, SIGSTOP);
			break;
		case 'r' :
			kill(pid, SIGCONT);
			break;
		case '+' :
			kill(pid, SIGUSR1);
			break;
		case '-' :
			kill(pid, SIGUSR2);
			break;
		default:
			return 0;
	}
	
	return 1;
}


int main(){
    fork_();
	return 0;
}
