//
// Authors: Colin Cassidy and Zach Smith
// Created: 11/10/2025
// Last Updated:
// 
// Description: 
//     Collects data from DAQ during test and writes it to a .bin file. Also 
//     sends periodic updates to port 5000, to be interpreted by NORTHSTAR.
// 



#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>

//define channel struct
typedef struct {
    double ch[16];
} Sample16;

//setup binary ring buffer
#define RING_SIZE 32768
Sample16 ring[RING_SIZE];
_Atomic size_t head = 0;
_Atomic size_t tail = 0;

//DAQ callback
void daq_callback(double *channel_values) {
    size_t h = head;
    size_t next = (h+1) & (RING_SIZE-1);
    if (next != tail) {
        memcpy(ring[h].ch, channel_values, 16*sizeof(double));
        head = next;
    }
}

//logger thread
while (running) {
    if (tail != head) {
        fwrite(&ring[tail], sizeof(Sample16), 1, data_file);
        tail = (tail+1) & (RING_SIZE-1);
    }
}