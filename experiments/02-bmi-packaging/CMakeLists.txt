cmake_minimum_required(VERSION 3.28)

project(hello-fmt LANGUAGES CXX)

if(NOT DEFINED CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 20)
  set(CMAKE_CXX_EXTENSIONS OFF)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

find_package(fmt REQUIRED)

add_executable(hello_world hello_world.cpp)
target_link_libraries(hello_world PRIVATE fmt::fmt)
