cmake_minimum_required(VERSION 3.14)


# Set app name(s) and version(s)
set(APP_1_NAME "temperatura")
set(APP_1_VERSION_NUMBER "1.0.1")


# Make project data accessible to compiler
add_compile_definitions(APP_NAME="${APP_1_NAME}")
add_compile_definitions(APP_VERSION="${APP_1_VERSION_NUMBER}")
add_compile_definitions(BUILD_NUM=${BUILD_NUMBER})

# Include app source code file(s)
add_executable(${APP_1_NAME}
    temperatura.cpp
)

target_compile_definitions(${APP_1_NAME} PRIVATE
        WIFI_SSID=\"${WIFI_SSID}\"
        WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
        NO_SYS=0)
target_include_directories(${APP_1_NAME} PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
        ${CMAKE_CURRENT_LIST_DIR}/../..)


list(APPEND DEPS pico_stdlib pico_cyw43_arch_none pico_one_wire)

target_link_libraries(${APP_1_NAME} ${DEPS})


# Enable/disable STDIO via USB and UART
pico_enable_stdio_usb(${APP_1_NAME} 1)
pico_enable_stdio_uart(${APP_1_NAME} 0)

# Enable extra build products
pico_add_extra_outputs(${APP_1_NAME})
