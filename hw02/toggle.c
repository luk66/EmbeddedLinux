#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <libsoc_gpio.h>
#include <libsoc_debug.h>
#define GPIO_OUTPUT 50
int main(void) {
  gpio *gpio_output;
  libsoc_set_debug(1);
  gpio_output = libsoc_gpio_request(GPIO_OUTPUT, LS_SHARED);
  libsoc_gpio_set_direction(gpio_output, OUTPUT);
  libsoc_set_debug(0);
  for(int i=0; i< 1000000; i++){
    libsoc_gpio_set_level(gpio_output, HIGH);
    usleep(100000);
    libsoc_gpio_set_level(gpio_output, LOW);
    usleep(100000);
  }
  if (gpio_output) {
    libsoc_gpio_free(gpio_output); }
 return EXIT_SUCCESS;
}
