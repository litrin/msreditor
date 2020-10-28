# BSD 2-Clause License
#
# Copyright (c) 2020, Litrin Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os

if os.sys.platform.lower() != "linux":
    raise NotImplementedError("MSR only supports by Linux")

if os.getuid() != 0:
    raise PermissionError("Permission deny, please run this tool by root.")


class MSRContent(bytes):

    @staticmethod
    def from_int(i):
        i = int(i)
        value = i.to_bytes(8, byteorder=os.sys.byteorder)
        return MSRContent(value)

    def __int__(self):
        return int.from_bytes(self, os.sys.byteorder)

    def __str__(self):
        return hex(int(self))

    def __repr__(self):
        return str(self)


class MSR:
    cpu = 0

    def __init__(self, core_number=0):
        """
        Open MSR
        :param core_number: CPU number
        """
        if core_number > os.cpu_count() - 1:
            raise NameError("CPU#%s does not exist." % core_number)
        self.cpu = core_number

    @property
    def msr_file(self):
        filename = "/dev/cpu/%d/msr" % self.cpu
        if not os.path.exists(filename):
            raise FileNotFoundError("Please run cmd: 'sudo modprobe msr' to "
                                    "apply Linux MSR files before use.")
        return filename

    def read(self, offset):
        with open(self.msr_file, "rb") as msr_fd:
            msr_fd.seek(offset)
            value = msr_fd.read(8)

        return MSRContent(value)

    def write(self, offset, value):
        value = MSRContent.from_int(value)
        with open(self.msr_file, "wb") as msr_fd:
            msr_fd.seek(offset)
            msr_fd.write(value)

    def __getitem__(self, item):
        return self.read(item)

    def __setitem__(self, key, value):
        return self.write(key, value)
