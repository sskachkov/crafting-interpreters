#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"

typedef enum {
    OP_CONSTANT,
    OP_CONSTANT_LONG,
    OP_NIL,
    OP_TRUE,
    OP_FALSE,
    OP_EQUAL,
    OP_GREATER,
    OP_LESS,
    OP_ADD,
    OP_SUBSTRACT,
    OP_MULTIPLY,
    OP_DIVIDE,
    OP_RETURN,
    OP_NOT,
    OP_NEGATE
} OpCode;

typedef struct {
    int instruction;
    int line;
} LineRec;


typedef struct {
    int count;
    int capacity;
    uint8_t* code;
    int linesCount;
    int linesCapacity;
    LineRec* lines;
    ValueArray constants;
} Chunk;


void initChunk(Chunk* chunk);

void freeChunk(Chunk* chunk);

void writeChunk(Chunk* chunk, uint8_t byte, int line);

int addConstant(Chunk* chunk, Value value);

void writeConstant(Chunk* chunk, Value value, int line);

int getInstructionLine(Chunk* chunk, int offset);

#endif