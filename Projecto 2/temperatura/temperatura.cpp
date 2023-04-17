#include <cstdio>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/gpio.h"
#include "../../dependencies/pico-onewire/api/one_wire.h"



int main() {
    stdio_init_all();
    One_wire one_wire(15); // GP15 - Pin 20 
    one_wire.init();
    rom_address_t address{};
    while (true) {
        one_wire.single_device_read_rom(address);
        printf("Device Address: %02x%02x%02x%02x%02x%02x%02x%02x\n", address.rom[0], address.rom[1], address.rom[2], address.rom[3], address.rom[4], address.rom[5], address.rom[6], address.rom[7]);
        one_wire.convert_temperature(address, true, false);
        printf("Temperature: %3.1foC\n", one_wire.temperature(address));
        sleep_ms(1000);
    }

    return 0;
}