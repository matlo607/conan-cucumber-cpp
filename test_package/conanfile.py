#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake

class CucumberCppPackageTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    _cmake = None

    def requirements(self):
        self.requires("gtest/1.8.0@bincrafters/stable")

    def build(self):
        self._cmake = CMake(self)
        self._cmake.configure(args=['-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON'])
        self._cmake.build()

    def test(self):
        self._cmake.test()
