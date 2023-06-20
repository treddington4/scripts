#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct device {
    const char *name;
    struct device *next_sibling;
    struct device *first_child;
    uint16_t info;
} device_t;

device_t device_root;

/*
Part 1 -

Let's pretend we're building the firmware for a brand-new system
on a chip. The manufacturer has supplied us with a "device tree",
which describes what peripherals are available to the processor
(see the definition of `device_root` below).

Please implement `enumerate_devices`. It should print something
that looks like this (note that indentation is important):

root
    gpbus
        gp0
        gp1
        gp2
    m1
        m2
            data
            prog
    nv
    
You are allowed to modify `enumerate_devices`s parameters and
return value, and may solve the problem using iteration or recursion.
*/

void enumerate_devices(device_t *device, uint8_t level) {   
  if (NULL != device)
  {
      int nextLevel = level+1;
      for (int i=0; i < level; i++)
      {
          printf("    ");
      }
      printf("%s\n", device->name);

      enumerate_devices(device->first_child, nextLevel);
      enumerate_devices(device->next_sibling, level);

  }  
}


/*
Part 2 -

The manufacturer has sent us some new documentation. It explains
how to interpret the `info` value:

-- BEGIN SNIPPET --

15 14 | 13 12 11 10 9  | 8  7  6  5 | 4  3  2  1  0
type  | param          | attrib     | unused
type: 0=”flash” 1=”memory” 2=”gpio” 3=”bus”
param:
    when type=”flash”  .. number of 1kB pages
         type=”memory” .. total size in kB
         type=”gpio”   .. pin number
         type=”bus”    .. no meaning
attrib:
    when type=”flash”  .. no meaning
    when type=”memory” ..
         bit 8 .. 1=readable
         bit 7 .. 1=writable
         bit 6 .. 1=executable
         bit 5 .. 0=word-aligned, 1=dword-aligned
    when type=”gpio” ..
         bit 8 .. 1=input-capable
         bit 7 .. 1=output-capable
         bit 6, 5 .. unused
    when type=”bus” .. no meaning

-- END SNIPPET --

Starting with your implementation of `enumerate_devices`, please
implement `enumerate_devices_ext`. It addition to printing each
device's name (as before), if the device is a *memory device*, it
should print any information we have about the memory device.
*/
#define BIT(b) (1<<(b))

typedef union _info {
    uint16_t value;
    struct INFO{
        uint16_t reserved: 5;
        uint16_t attrib: 4;
        uint16_t param : 5;
        uint16_t type : 2;
    } info;
} dev_info;

void enumerate_devices_ext(device_t *device, uint8_t level) {  
  if (NULL != device)
  {

      int nextLevel = level+1;
      for (int i=0; i < level; i++)
      {
          printf("    ");
      }
      printf("\t v:%s", device->name);
      // printf("%d", (device->info));

      dev_info v;
      v.value = device->info;
            int type = (device->info) >>14; // 0xC000
      printf("%d, %d", v.info.type, type);

      switch (type)
      {
        case 0: //flash
          break;
        case 1: //memory
        {
          int size = ((device->info) ^ 0xC000) >> 9; 
          printf("\t%d kB", size);
          // print total size in kB
          // print attribute
          
          printf((0 != (device->info & BIT(8))?"\treadable":""));
          printf((0 != (device->info & BIT(7))?"\twritable":""));
          printf((0 != (device->info & BIT(6))?"\texecutable":""));
          printf((0 != (device->info & BIT(5))?"\tdword-aligned":"\tword-aligned"));
        }
        break;
        default:
        //error
        break;
      }
      printf("\n");

      enumerate_devices_ext(device->first_child, nextLevel);
      enumerate_devices_ext(device->next_sibling, level);

  }  
}


/*
Part 3 -

Your coworkers need a function that helps them find GPIOs.

For example:

find_gpios(1, 1, -1, callback_fn)

    .. should call callback_fn(device) for each GPIO
       that can be either an input or an output.

find_gpios(1, 0, -1, callback_fn)

    .. should call callback_fn(device) for each GPIO
       that can be an input.

find_gpios(1, 0, 4, callback_fn)

    .. should call callback_fn() for the GPIO on pin 4, but only
       if it can act as an input.
*/

void find_gpios(int is_input, int is_output, int which_pin, void(*cb)(device_t *)) {   
}

int main() {
    // enumerate_devices(&device_root,0);
    enumerate_devices_ext(&device_root, 0);
    return 0;
}

/*************************
 *     Device Tree       *
 *************************/

device_t device_prog = {
    .name = "prog",
    .next_sibling = NULL,
    .first_child = NULL,
    .info = 0b0100100101000000
};

device_t device_data= {
    .name = "data",
    .next_sibling = &device_prog,
    .first_child = NULL,
    .info = 0b0110000110000000
};

device_t device_m2 = {
    .name = "m2",
    .next_sibling = NULL,
    .first_child = &device_data,
    .info = 0b1100000000000000
};

device_t device_gp2 = {
    .name = "gp2",
    .next_sibling = NULL,
    .first_child = NULL,
    .info = 0b1000011010000000
};

device_t device_gp1 = {
    .name = "gp1",
    .next_sibling = &device_gp2,
    .first_child = NULL,
    .info = 0b1000010100000000
};

device_t device_gp0 = {
    .name = "gp0",
    .next_sibling = &device_gp1,
    .first_child = NULL,
    .info = 0b1000001110000000
};

device_t device_nv = {
    .name = "nv",
    .next_sibling = NULL,
    .first_child = NULL,
    .info = 0b0010000000000000
};

device_t device_m1 = {
    .name = "m1",
    .next_sibling = &device_nv,
    .first_child = &device_m2,
    .info = 0b1100000000000000
};

device_t device_gpbus = {
    .name = "gpbus",
    .next_sibling = &device_m1,
    .first_child = &device_gp0,
    .info = 0b1100000000000000
};

device_t device_root = {
    .name = "root",
    .next_sibling = NULL,
    .first_child = &device_gpbus,
    .info = 0
};