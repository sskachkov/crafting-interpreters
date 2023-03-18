#include <stdlib.h>
#include <stdio.h>
#include "chunk.h"
#include "memory.h"


void initChunk(Chunk* chunk) {
    chunk->count = 0;
    chunk->capacity = 0;
    chunk->code = NULL;
    chunk->linesCount = 0;
    chunk->linesCapacity = 0;
    chunk->lines = NULL;
    initValueArray(&chunk->constants);
}

void freeChunk(Chunk* chunk) {
    FREE_ARRAY(uint8_t, chunk->code, chunk->capacity);
    FREE_ARRAY(uint8_t, chunk->lines, chunk->capacity);
    freeValueArray(&chunk->constants);
    initChunk(chunk);
}

void appendLineData(Chunk* chunk, int line) {
    if (chunk->linesCapacity < chunk->linesCount + 1) {
        int oldCap = chunk->linesCapacity;
        chunk->linesCapacity = GROW_CAPACITY(oldCap);
        chunk->lines = GROW_ARRAY(LineRec, chunk->lines, oldCap, chunk->linesCapacity);
    }
    LineRec lr = {.instruction = chunk->count - 1, .line = line};
    chunk->lines[chunk->linesCount] = lr;
    chunk->linesCount++;
    
}

void writeConstant(Chunk* chunk, Value value, int line) {
    int constant = addConstant(chunk, value);
    if (constant < 3) {
        writeChunk(chunk, OP_CONSTANT, line);
        writeChunk(chunk, constant, line);
    } else {
        writeChunk(chunk, OP_CONSTANT_LONG, line);
        int x1 = (constant) & 0xff;
        int x2 = (constant >> (8)) & 0xff;
        int x3 = (constant >> (16)) & 0xff;
        //printf("\n%d %d %d %d \n",constant, x1, x2, x3);
        writeChunk(chunk, x3, line);
        writeChunk(chunk, x2, line);
        writeChunk(chunk, x1, line);
    }
    writeChunk(chunk, OP_RETURN, line);
}

void writeChunk(Chunk* chunk, uint8_t byte, int line) {
    if (chunk->capacity < chunk->count + 1) {
        int oldCap = chunk->capacity;
        chunk->capacity = GROW_CAPACITY(oldCap);
        chunk->code = GROW_ARRAY(uint8_t, chunk->code, oldCap, chunk->capacity);
    }

    chunk->code[chunk->count] = byte;
    chunk->count++;
    if (chunk->count == 1 || chunk->lines[chunk->linesCount - 1].line != line) {
        appendLineData(chunk, line);
    } else {
        chunk->lines[chunk->linesCount - 1].instruction = chunk->count - 1;
    }

}


void updateLines(Chunk* chunk, int line) {
    if (chunk->count == 1) {
        appendLineData(chunk, line);
    }
}

int getInstructionLine(Chunk* chunk, int offset) {
    for (int i = 0; i < chunk->linesCount; i++) {
        if (chunk->lines[i].instruction >= offset) {
            return chunk->lines[i].line;
        }
    }
    return -1;
}

int addConstant(Chunk* chunk, Value value) {
    writeValueArray(&chunk->constants, value);
    ValueArray v = chunk->constants;
    return chunk->constants.count - 1;
}