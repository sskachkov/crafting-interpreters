#ifndef clox_debug_h
#define clox_debug_h

#include <stdio.h>
#include "chunk.h"


void disassembleChunk(Chunk* chunk, const char* name);
void disassembleChunkCustomOut(Chunk *chunk, const char *name, FILE * outStream);

int disassembleInstruction(Chunk* chunk, int offset);
int disassembleInstructionCustomOut(Chunk* chunk, int offset, FILE * outStream);

#endif