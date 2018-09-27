#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

#define GPIO_23 (1<<23)
#define GPIO_50 (1<<18)
/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr_1;
    volatile unsigned int *gpio_datain_1;
    volatile unsigned int *gpio_oe_addr_1;
    volatile unsigned int *gpio_setdataout_addr_1;
    volatile unsigned int *gpio_cleardataout_addr_1;
    unsigned int reg_1;

    volatile void *gpio_addr_0;
    volatile unsigned int *gpio_datain_0;
    volatile unsigned int *gpio_oe_addr_0;
    volatile unsigned int *gpio_setdataout_addr_0;
    volatile unsigned int *gpio_cleardataout_addr_0;
    unsigned int reg_0;
    
    // Set the signal callback for Ctrl-C
  	signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

// gpio port 1 -> usr3
// gpio port 0 -> usr2
    gpio_addr_1 = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);
    gpio_addr_0 = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO0_START_ADDR);
   
    gpio_datain_1            = gpio_addr_1  + GPIO_DATAIN;
    gpio_oe_addr_1           = gpio_addr_1 + GPIO_OE;
    gpio_setdataout_addr_1   = gpio_addr_1 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_1 = gpio_addr_1 + GPIO_CLEARDATAOUT;

    gpio_datain_0            = gpio_addr_0  + GPIO_DATAIN;
    gpio_oe_addr_0           = gpio_addr_0 + GPIO_OE;
    gpio_setdataout_addr_0   = gpio_addr_0 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr_0 = gpio_addr_0 + GPIO_CLEARDATAOUT;

    // Set USR3 to be an output pin
    reg_1 = *gpio_oe_addr_1;
    reg_1 &= ~USR3;       // Set USR3 bit to 0
    *gpio_oe_addr_1 = reg_1;

    reg_0 = *gpio_oe_addr_0;
    reg_0 &= ~USR2;
    *gpio_oe_addr_0 = reg_0;

 
    while(keepgoing) {
       if((*gpio_datain_0 & GPIO_23)){
         *gpio_setdataout_addr_1 = USR3;
       }else{
             *gpio_cleardataout_addr_1 = USR3;
       }
       if((*gpio_datain_1 & GPIO_50)){
             *gpio_setdataout_addr_1 = USR2;
       }else{
             *gpio_cleardataout_addr_1 = USR2;
       }
    }

    munmap((void *)gpio_addr_1, GPIO1_SIZE);
    munmap((void *)gpio_addr_0, GPIO0_SIZE);
    close(fd);
    return 0;
}
