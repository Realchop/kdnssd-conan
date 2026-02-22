cmake_minimum_required(VERSION 3.27)
project(test_package CXX)

# You need this, which is obvious, but conan won't be instaliing it for you
find_package(Qt6 REQUIRED COMPONENTS Core)

find_package(KF6DNSSD REQUIRED NO_MODULE)

add_executable(example src/example.cpp)
target_link_libraries(example 
    PRIVATE
    Qt6::Core
    KF6::DNSSD
)
