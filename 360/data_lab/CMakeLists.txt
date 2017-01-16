cmake_minimum_required(VERSION 3.6)
project(data_lab)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        datalab-handout/bits.c
        datalab-handout/bits.h
        datalab-handout/btest.c
        datalab-handout/btest.h
        datalab-handout/decl.c
        datalab-handout/fshow.c
        datalab-handout/ishow.c
        datalab-handout/tests.c)

add_executable(data_lab ${SOURCE_FILES})