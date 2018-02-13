project(CucumberPackageTest)

message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message(STATUS "CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")
message(STATUS "CMAKE_RUNTIME_OUTPUT_DIRECTORY: ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

find_program (CONANBIN conan)
if(CONANBIN)
    message (STATUS "conan C++ package manager: installed")
    find_file (CONANFILE "${CMAKE_SOURCE_DIR}/conanfile.txt")
    if (CONANFILE)
        message (STATUS "conanfile.txt: found")
    endif()
endif()

if (EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    message(STATUS "conan_basic_setups()")
    conan_basic_setup(TARGETS)
endif()

set(THREADS_PREFER_PTHREAD_FLAG on)
find_package(GTest REQUIRED)
find_package(Boost REQUIRED)

enable_testing()

set(TARGET_NAME test_package)
add_executable(${TARGET_NAME} test_package.cpp)
target_link_libraries(${TARGET_NAME} PRIVATE CONAN_PKG::cucumber-cpp GTest::GTest GTest::Main)

include(CTest)

add_test(conan_test "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${TARGET_NAME}")
