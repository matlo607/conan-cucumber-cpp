#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


class CucumberCppConan(ConanFile):
    name = "cucumber-cpp"
    version = "0.5+"
    description = "Cucumber-Cpp, formerly known \
                   as CukeBins, allows Cucumber to support \
                   step definitions written in C++."
    license = "https://github.com/cucumber/cucumber-cpp/blob/master/LICENSE.txt"
    url = "https://github.com/matlo607/cucumber-cpp.git"
    settings = "os", "compiler", "arch", "build_type"
    options = {
        "shared": [True, False],
        "include_pdbs": [True, False],
        "fPIC": [True, False],
        "tests": [True, False]
    }
    default_options = (
        "shared=False",
        "include_pdbs=True",
        "fPIC=True",
        "tests=True"
    )
    repo = "https://github.com/matlo607/cucumber-cpp.git"
    source_dir = "{name}-{version}".format(name=name, version=version)
    scm = {
        "type": "git",
        "subfolder": source_dir,
        "url": repo,
        "revision": "feature-cmake-support-conan"
    }
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    def build_requirements(self):
        if self.options.tests:
            self.build_requires("gtest/1.8.0@bincrafters/stable")
            self.options['gtest'].build_gmock = True

    def requirements(self):
        self.requires("boost/1.66.0@conan/stable")

    def source(self):
        # use CMakeLists.txt provided by the conan recipe
        #with tools.chdir(self.source_dir):
        #    os.rename('CMakeLists.txt', 'CMakeListsOriginal.cmake')
        #shutil.move('CMakeLists.txt', self.source_dir)
        pass

    def configure(self):
        self.options['boost'].skip_lib_rename = True

        if self.settings.compiler != "Visual Studio":
            try:  # It might have already been removed if required by more than 1 package
                del self.options.include_pdbs
            except Exception:
                pass

    def _cat(self, filepath):
        with open(filepath, "r") as f:
            text = f.read()
            print(text)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.source_dir)):
            ruby_path = []
            if self.options.tests:
                self.output.info("Installing Ruby prerequisites")
                self._cat("Gemfile")
                bundle_dir = os.path.join(self.source_folder, self.source_dir, 'vendor', 'bundle')
                ruby_path = os.path.join(bundle_dir, 'bin')
                if not os.path.isdir("vendor"): # was maybe pre-fetched in the source method
                    self.run("bundle install --binstubs={} --path={}".format(ruby_path, bundle_dir))
            with tools.environment_append({"PATH": [ruby_path]}):
                cmake = CMake(self)
                if self.settings.os != "Windows" and self.options.fPIC:
                    cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
                if self.settings.compiler == "Visual Studio":
                    # Boost 1.66.0 was not tested with the latest Visual Studio 2017 update
                    cmake.definitions["CONAN_CXX_FLAGS"] = " ".join((cmake.definitions["CONAN_CXX_FLAGS"], "-DBOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"))
                    # Statically link Boost on Windows does not seem to work anymore with the latest CMake versions
                    cmake.definitions["CUKE_USE_STATIC_BOOST"] = "ON"
                if self.options.tests:
                    # The BoostDriverTest requires the dll version of unit_test_framework
                    cmake.definitions["CUKE_DISABLE_BOOST_TEST"] = "ON"
                cmake.definitions["CUKE_DISABLE_QT"] = "ON"
                cmake.verbose = True
                cmake.configure(source_dir=os.path.join(self.source_folder, self.source_dir))
                cmake.build()
                if self.options.tests:
                    cmake.test()
                cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib', 'lib64']
        self.cpp_info.libs = ["cucumber-cpp", "cucumber-cpp-nomain"]
