from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, collect_libs
from conan.tools.system.package_manager import Apt

class KdnssdConan(ConanFile):
    name = "kdnssd"
    # TODO:
    # Match this with actual package version automatically
    version = "6.22.0"
    license = "MIT"
    author = "Lazar Jovanović (Realchop)"
    url = "https://github.com/Realchop/kdnssd-conan"
    description = "A C++ wrapper for DNS-SD (Zeroconf)"
    topics = ("dns-sd", "zeroconf", "mdns", "networking")

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libavahi-client-dev", "libavahi-common-dev", "libnss-mdns"])

    def source(self):
        get(self, url="https://github.com/KDE/kdnssd/archive/refs/tags/v6.22.0.tar.gz", strip_root=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()
        

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
            self.cpp_info.set_property("cmake_file_name", "KF6DNSSD")
            
            self.cpp_info.set_property("cmake_target_name", "KF6::DNSSD")
            
            self.cpp_info.libs = ["KF6DNSSD"]

            self.cpp_info.includedirs = ["include/KF6/KDNSSD"]
            
            if self.settings.os == "Linux":
                self.cpp_info.system_libs = [
                                "avahi-client", 
                                "avahi-common",
                                "Qt6Core", 
                                "Qt6Network", 
                                "Qt6DBus" 
                            ]

                self.cpp_info.includedirs.append("/usr/include/qt6")

                self.output.warning("KDNSSD requires 'mdns4_minimal' to be enabled in /etc/nsswitch.conf for hostname resolution.")

