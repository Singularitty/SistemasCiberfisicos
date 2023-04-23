#include <cstdio>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/gpio.h"
#include "../../dependencies/pico-onewire/api/one_wire.h"


float avg_temp(float temp[]) {
    float avg = 0;
    for (int i = 0; i < 10; i++) {
        avg += temp[i];
    }
    return avg / 10;
}

int main() {
    stdio_init_all();
    One_wire one_wire(15); // GP15 - Pin 20 
    one_wire.init();
    rom_address_t address{};
    float instant_temp;
    float temps[10];
    int n = 0;
    while (true) {
        one_wire.single_device_read_rom(address);
        //printf("Device Address: %02x%02x%02x%02x%02x%02x%02x%02x\n", address.rom[0], address.rom[1], address.rom[2], address.rom[3], address.rom[4], address.rom[5], address.rom[6], address.rom[7]);
        one_wire.convert_temperature(address, true, false);
        instant_temp = one_wire.temperature(address);
        printf("Instant Temperature: %3.1foC\n", instant_temp);

        if (n == 10) {
            n = 0;
            printf("Average Temperature of 10s: %3.1foC\n", avg_temp(temps));
        }
        temps[n] = instant_temp;
        n += 1;
        sleep_ms(1000);
    }

    return 0;
}