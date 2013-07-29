#!/usr/bin/python2
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Copyright (c) 2013 Alberto Ruiz <aruiz@gnome.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
  * Neither the name of Pioneers of the Inevitable, Songbird, nor the names
    of its contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
from dulwich.repo import Repo
import sys
import os

class SixMonthStats:
    def __init__ (self, repos):
        self.repos = []
        self.date_oldest = None
        self.date_newest = None

        for repodir in sys.argv[1:]:
            try:
                assert (os.path.isdir(repodir))
            except:
                raise Exception("%s is not a valid directory" % repodir)

            self.repos.append (Repo(repodir))

        self.find_date_boundaries ()

    def find_date_boundaries (self):
        for repo in self.repos:
            master = repo.get_refs()['refs/heads/master']
            print repo.get_walker ([master])


def main ():
  st = SixMonthStats (sys.argv[1:])

if __name__ == '__main__':
  main ()
