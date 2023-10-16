from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import get
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

import os

class fmtRecipe(ConanFile):
    name = "fmt"
    version = "10.1.1-module"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):
        url = "https://github.com/jcar87/fmt/archive/abdb7e0cccd8945d1b31e0c4bc95abbe03b1f915.zip"
        checksum = "2b0ffaac1f0a114851f69846e062f8759c5a5e8b77f719435e2dca74e1b4fe35"
        get(self, url=url, sha256=checksum, strip_root=True)

    def layout(self):
        cmake_layout(self)

    def validate(self):
        check_min_cppstd(self, "20")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["FMT_INSTALL"] = "ON"
        tc.cache_variables["FMT_MODULE"] = "ON"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["fmt"]

        # Skip the Conan-generated files by CMakeDeps,
        # and use the fmt-config.cmake bundled with fmt
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs = ["."]
