# Explicitly list the sources specific to each target.
EXECUTABLE_SOURCES := main.c
TESTSUITE_SOURCES := test.c unity/unity.c

# Filter out all specific sources from the common wildcard-ed sources.
COMMON_SOURCES := $(filter-out $(TESTSUITE_SOURCES) $(EXECUTABLE_SOURCES),$(wildcard *.c))
all : clean test bin

.PHONY: test


test:
	cc $(TESTSUITE_SOURCES) $(COMMON_SOURCES) -o testClox
	./testClox

bin: $(EXECUTABLE_SOURCES) $(COMMON_SOURCES)
	cc -g $(EXECUTABLE_SOURCES) $(COMMON_SOURCES) -o clox


clean:
	rm -f testClox clox *.o