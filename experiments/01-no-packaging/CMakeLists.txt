cmake_minimum_required(VERSION 3.28)

project(hello-fmt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# Fetch and build {fmt} as part of this project
set(FMT_MODULE ON)
FetchContent_Declare(fmt
  GIT_REPOSITORY https://github.com/jcar87/fmt.git
  GIT_TAG        de938909398ee6a94c8a1df22eb6f767b38a20b3 # trunk 2023-10-12 (~10.1.1) built as module
  OVERRIDE_FIND_PACKAGE
)

FetchContent_MakeAvailable(fmt)

find_package(fmt REQUIRED)

add_executable(hello_world hello_world.cpp)
target_link_libraries(hello_world PRIVATE fmt::fmt)
