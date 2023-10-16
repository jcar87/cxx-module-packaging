cmake_minimum_required(VERSION 3.28)

project(PackageTest CXX)

find_package(fmt REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example PRIVATE fmt::fmt)
