cmake_minimum_required(VERSION 3.16)
project(SPF_MirrorSeatControls LANGUAGES CXX ASM_MASM)
set(CMAKE_CXX_STANDARD 20)
add_library(SPF_MirrorSeatControls SHARED MirrorControls.cpp SlotHooks.asm)
target_include_directories(SPF_MirrorSeatControls PRIVATE SPF_API)
target_link_libraries(SPF_MirrorSeatControls PRIVATE bcrypt winmm)
target_compile_definitions(SPF_MirrorSeatControls PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
target_compile_options(SPF_MirrorSeatControls PRIVATE $<$<COMPILE_LANGUAGE:CXX>:/W4> $<$<COMPILE_LANGUAGE:CXX>:/EHsc>)
enable_testing()
add_executable(MirrorSeatControlsTests Tests.cpp SlotHooks.asm TestHooks.asm)
target_include_directories(MirrorSeatControlsTests PRIVATE SPF_API)
target_link_libraries(MirrorSeatControlsTests PRIVATE bcrypt winmm)
target_compile_definitions(MirrorSeatControlsTests PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
add_test(NAME MirrorRegression COMMAND MirrorSeatControlsTests "${CMAKE_CURRENT_SOURCE_DIR}/sounds/off.wav")

add_custom_command(TARGET SPF_MirrorSeatControls POST_BUILD
 COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_BINARY_DIR}/package/SPF_MirrorSeatControls"
 COMMAND ${CMAKE_COMMAND} -E copy "$<TARGET_FILE:SPF_MirrorSeatControls>" "${CMAKE_BINARY_DIR}/package/SPF_MirrorSeatControls/"
 COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_SOURCE_DIR}/sounds" "${CMAKE_BINARY_DIR}/package/SPF_MirrorSeatControls/sounds")
