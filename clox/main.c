#include <stdio.h>

#include "chunk.h"
#include "common.h"
#include "debug.h"
#include "vm.h"

int main(int argc, const char* argv[]) {
    initVM();
    Chunk chunk;
    initChunk(&chunk);
    int c1 = addConstant(&chunk, 2.3);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, c1, 123);

    int c2 = addConstant(&chunk, 7.6);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, c2, 123);

    writeChunk(&chunk, OP_ADD, 123);

    int c3 = addConstant(&chunk, 0.9);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, c3, 123);

    writeChunk(&chunk, OP_SUBSTRACT, 123);

    int c4 = addConstant(&chunk, 3);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, c4, 123);

    writeChunk(&chunk, OP_DIVIDE, 123);

    writeChunk(&chunk, OP_NEGATE, 123);
    writeChunk(&chunk, OP_RETURN, 123);


    //disassembleChunk(&chunk, "test chunk");
    interpret(&chunk);
    freeVM();
    freeChunk(&chunk);

    return 0;
}
