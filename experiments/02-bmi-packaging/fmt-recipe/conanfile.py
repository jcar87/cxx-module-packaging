from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, get, rmdir
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.microsoft import is_msvc

import os

class fmtRecipe(ConanFile):
    name = "fmt"
    version = "10.1.0-module"
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    implements = ["auto_shared_fpic"]

    def source(self):

        url = "https://github.com/jcar87/fmt/archive/28fbcaa72b6224f7824672a39f80c6130e28f317.zip"
        checksum = "54fec1ab9848a0c3e0dde92ebfff6a9b9aef73aec8c32c5a945786b8b4b99d0b"
        get(self, url=url, sha256=checksum, strip_root=True)

    def layout(self):
        cmake_layout(self)

    def validate(self):
        check_min_cppstd(self, "20")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["FMT_TEST"] = "OFF"
        tc.cache_variables["FMT_INSTALL"] = "ON"
        tc.cache_variables["FMT_FUZZ"] = "OFF"
        tc.cache_variables["CMAKE_VISIBILITY_INLINES_HIDDEN"] = "OFF"
        tc.cache_variables["CMAKE_CXX_VISIBILITY_PRESET"] = "default"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # copy the BMI into the bmi subfolder
        #msvc
        copy(self, "fmt*.ifc", src=os.path.join(self.build_folder, "fmt.dir", "Release"), dst=os.path.join(self.package_folder, "bmi"))
        #clang
        copy(self, "fmt.pcm", src=os.path.join(self.build_folder, "CMakeFiles", "fmt.dir"), dst=os.path.join(self.package_folder, "bmi"))
        #gcc
        copy(self, "fmt.gcm", src=os.path.join(self.build_folder, "CMakeFiles", "fmt.dir"), dst=os.path.join(self.package_folder, "bmi"))

        # remove anything that is not the BMI or the library file
        rmdir(self, os.path.join(self.package_folder, "include"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cxx"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        self.cpp_info.includedirs = []
        self.cpp_info.set_property("experimental_modules", ["fmt"])
        if is_msvc(self):
            bmi_dir = os.path.join(self.package_folder, "bmi").replace('\\','/')
            self.cpp_info.cxxflags = ["/reference fmt=fmt.cc.ifc", f"/ifcSearchDir{bmi_dir}"]
        elif self.settings.compiler == "clang":
            self.cpp_info.cxxflags = [f"-fmodule-file=fmt={self.package_folder}/bmi/fmt.pcm"]


    

    
