// os345signal.c - signals
// ***********************************************************************
// **   DISCLAMER ** DISCLAMER ** DISCLAMER ** DISCLAMER ** DISCLAMER   **
// **                                                                   **
// ** The code given here is the basis for the CS345 projects.          **
// ** It comes "as is" and "unwarranted."  As such, when you use part   **
// ** or all of the code, it becomes "yours" and you are responsible to **
// ** understand any algorithm or method presented.  Likewise, any      **
// ** errors or problems become your responsibility to fix.             **
// **                                                                   **
// ** NOTES:                                                            **
// ** -Comments beginning with "// ??" may require some implementation. **
// ** -Tab stops are set at every 3 spaces.                             **
// ** -The function API's in "OS345.h" should not be altered.           **
// **                                                                   **
// **   DISCLAMER ** DISCLAMER ** DISCLAMER ** DISCLAMER ** DISCLAMER   **
// ***********************************************************************
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <setjmp.h>
#include <assert.h>
#include "os345.h"
#include "os345signals.h"

extern TCB tcb[];                            // task control block
extern int curTask;                            // current task #


// itoa(x, s, 2)
// ***********************************************************************
// ***********************************************************************
//	Call all pending task signal handlers
//
//	return 1 if task is NOT to be scheduled.
//
int signals(void) {
    if (tcb[curTask].signal) {
        if (tcb[curTask].signal & mySIGINT) {
            tcb[curTask].signal &= ~mySIGINT;
            (*tcb[curTask].sigIntHandler)();
        }

        if (tcb[curTask].signal & mySIGCONT) {
            tcb[curTask].signal &= ~mySIGCONT;
            (*tcb[curTask].sigContHandler)();
        }

        if (tcb[curTask].signal & mySIGTERM) {
            tcb[curTask].signal &= ~mySIGTERM;
            (*tcb[curTask].sigTermHandler)();
        }

        if (tcb[curTask].signal & mySIGSTOP) {
            tcb[curTask].signal &= ~mySIGSTOP;
            (*tcb[curTask].sigTstpHandler)();
        }

        if (DEBUG_SIGNALS) {
            char* before = malloc(9 * sizeof(char));
            char* after = malloc(9 * sizeof(char));
            free(before);
            free(after);
        }
    }
    return 0;
}


// **********************************************************************
// **********************************************************************
//	Register task signal handlers
//
int sigAction(void (*sigHandler)(void), int sig) {
    switch (sig) {
        case mySIGINT: {
            tcb[curTask].sigIntHandler = sigHandler;        // mySIGINT handler
            return 0;
        }
        case mySIGTERM:{
            tcb[curTask].sigTermHandler = sigHandler;
            return 0;
        }
        case mySIGSTOP:{
            tcb[curTask].sigTstpHandler = sigHandler;
            return 0;
        }
        case mySIGCONT:{
            tcb[curTask].sigContHandler = sigHandler;
            return 0;
        }
    }
    return 1;
}


// **********************************************************************
//	sigSignal - send signal to task(s)
//
//	taskId = task (-1 = all tasks)
//	sig = signal
//
int sigSignal(int taskId, int sig) {
    // check for task
    if ((taskId >= 0) && tcb[taskId].name) {
        tcb[taskId].signal |= sig;
        return 0;
    } else if (taskId == -1) {
        for (taskId = 0; taskId < MAX_TASKS; taskId++) {
            sigSignal(taskId, sig);
        }
        return 0;
    }
    // error
    return 1;
}


// **********************************************************************
// **********************************************************************
//	Default signal handlers
//
void defaultSigIntHandler(void)            // task mySIGINT handler
{
    printf("\ndefaultSigIntHandler");
    return;
}

void defaultSigContHandler(void){
    printf("\nDefaultSigContHandler");
    return;
}

void defaultSigTstpHandler(void){
    printf("\ndefaultTstpHandler");
    sigSignal(-1, mySIGSTOP);
    return;
}

void defaultSigTermHandler(void){
    printf("\nDefaultSigTermHandler");
    killTask(curTask);
    return;
}
void createTaskSigHandlers(int tid) {
    tcb[tid].signal = 0;
    if (tid) {
        // inherit parent signal handlers
        tcb[tid].sigIntHandler = tcb[curTask].sigIntHandler;            // mySIGINT handler
        tcb[tid].sigContHandler = tcb[curTask].sigContHandler;
        tcb[tid].sigTstpHandler = tcb[curTask].sigTstpHandler;
        tcb[tid].sigTermHandler = tcb[curTask].sigTermHandler;
    } else {
        // otherwise use defaults
        tcb[tid].sigIntHandler = defaultSigIntHandler;            // task mySIGINT handler
        tcb[tid].sigContHandler= defaultSigContHandler;            // task mySIGINT handler
        tcb[tid].sigTstpHandler= defaultSigTstpHandler;            // task mySIGINT handler
        tcb[tid].sigTermHandler= defaultSigTermHandler;            // task mySIGINT handler
    }
}
