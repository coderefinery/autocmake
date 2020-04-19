# (c) https://github.com/dev-cafe/autocmake/blob/master/AUTHORS.md
# licensed under BSD-3: https://github.com/dev-cafe/autocmake/blob/master/LICENSE

#.rst:
#
# Provides safeguards against in-source builds and bad build types.
#
# Variables used::
#
#   PROJECT_SOURCE_DIR
#   PROJECT_BINARY_DIR
#   CMAKE_BUILD_TYPE

if(${PROJECT_SOURCE_DIR} STREQUAL ${PROJECT_BINARY_DIR})
    message(FATAL_ERROR "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there.")
endif()

string(TOLOWER "${CMAKE_BUILD_TYPE}" _cmake_build_type_tolower)

set(_available_types "debug" "release" "minsizerel" "relwithdebinfo")

if(NOT "${_cmake_build_type_tolower}" IN_LIST _available_types)
    message(FATAL_ERROR "Unknown build type \"${CMAKE_BUILD_TYPE}\". Allowed values are: ${_available_types}.")
endif()
