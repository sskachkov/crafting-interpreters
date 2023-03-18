#include <stdio.h>

#include "unity/unity.h"
#include "debug.h"

void setUp(void) {
}

void tearDown(void) {
}

void test_debug_instruction_lines(void) {
    char dataInMemory [1024];
    FILE * fd = fmemopen(dataInMemory, sizeof(dataInMemory), "w");

    Chunk chunk;
    initChunk(&chunk);
    int c1 = addConstant(&chunk, 1.3);
    int c2 = addConstant(&chunk, 23.11);
    int c3 = addConstant(&chunk, 9.11);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, c1, 123);
    writeChunk(&chunk, OP_RETURN, 123);

    writeChunk(&chunk, OP_CONSTANT, 124);
    writeChunk(&chunk, c2, 124);
    writeChunk(&chunk, OP_RETURN, 124);
    writeChunk(&chunk, OP_RETURN, 125);


    TEST_ASSERT_EQUAL_INT32(123, getInstructionLine(&chunk, 0));
    TEST_ASSERT_EQUAL_INT32(123, getInstructionLine(&chunk, 2));
    TEST_ASSERT_EQUAL_INT32(124, getInstructionLine(&chunk, 3));
    TEST_ASSERT_EQUAL_INT32(124, getInstructionLine(&chunk, 5));
    TEST_ASSERT_EQUAL_INT32(125, getInstructionLine(&chunk, 6));
    
    //disassembleChunkCustomOut(&chunk, "test chunk", fd);
    freeChunk(&chunk);
}


int main(void) {
    UnityBegin("tests");
    RUN_TEST(test_debug_instruction_lines);
    return UnityEnd();
}