# msreditor
Read/write MSR (Model Specific Register) by python.

A MSR is any of various control registers in the x86 instruction set used for debugging, program execution tracing, computer performance monitoring, and toggling certain CPU features. 
Use `man msr` for detail.

This library requires:
- Python under x86/x86_64 Linux OS.
- Root user permission.
- Already loaded msr module by command: `sudo modprobe msr` 

# Installation
Download and decompress this package
```
sudo python3 setup.py build
sudo python3 setup.py install
```

# Reference code
```
from msreditor import MSR

if __name__ == "__main__":

    a = MSR(0)  # open msr of CPU 0
    orig = a[0x38f]  # read msr offset 0x38f
    print(orig)
    if int(orig) == 0x70000000f:
        a[0x38f] = 0
    else:
        a[0x38f] = 0x70000000f  # update value of 0x38f
    print(a[0x38f])

```
