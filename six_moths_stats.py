#!/usr/bin/python2
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (c) 2013 Alberto Ruiz <aruiz@gnome.org>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
"""
from dulwich.repo import Repo
from datetime import datetime
import sys
import os
import json

from gnome_releases import RELEASES

class SixMonthLog:
    pass

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

        self.repos = repos

        #self._find_date_boundaries ()

    def _find_date_boundaries (self):
        for repo in self.repos:
            repo = Repo(repo)
            master = repo.get_refs()['refs/heads/master']
            for i in repo.get_walker ([master]):
                if self.date_oldest == None or self.date_oldest > i.commit.commit_time:
                    self.date_oldest = i.commit.commit_time
                if self.date_newest == None or self.date_newest < i.commit.commit_time:
                    self.date_newest = i.commit.commit_time
                del i
            del repo

    def _find_period (self, periods, time):
        prev = periods[0]
        for p in periods[1:]:
            if time < p:
                break
            prev = p
        return prev

    def list_all_contributors (self):
        tmp = 1
        tot = len(self.repos)
        all_contribs = []
        for repo in self.repos:
            print >> sys.stderr, "[%d/%d Analyzing %s]" % (tmp, tot, repo)
            tmp += 1
            repo = Repo(repo)
            master = repo.get_refs()['refs/heads/master']
            for i in repo.get_walker ([master]):
                if "<" in i.commit.author:
                    split = i.commit.author.split("<")
                    author = split[0]
                    email = split[1]
                    author = author.strip ()
                    email = email.strip ()
                    email = email[:-1]
                else:
                    author = i.commit.author
                    email = ""

                all_contribs.append((author, email))
            del repo

        tmp = []
        for c in all_contribs:
            if c in tmp:
                continue
            tmp.append(c)
        return tmp


    def build_stats_by_periods (self, periods, filter_fn=None):
        assert (len(periods) > 0)
        assert (reduce(lambda x,y: x and y, map(lambda x: isinstance(x,int), periods)))

        lower = self.date_oldest
        upper = self.date_newest

        periods.sort()
        periods = dict.fromkeys(periods, [])

        tmp = 1
        tot = len(self.repos)
        for repo in self.repos:
            print >> sys.stderr, "[%d/%d Analyzing %s]" % (tmp, tot, repo)
            tmp += 1
            repo = Repo(repo)
            master = repo.get_refs()['refs/heads/master']
            for i in repo.get_walker ([master]):
                keys = periods.keys()
                keys.sort()
                lower = keys[0]
                upper = keys[-1]
                if i.commit.commit_time < lower or i.commit.commit_time > upper:
                    continue
                if filter_fn != None and not filter_fn (i):
                    continue

                period = self._find_period (periods.keys(), i.commit.commit_time)
                author = i.commit.author.split("<")[0].strip()

                periods[period].append(author)
                del i
            del repo
    
        for period in periods.keys():
            periods[period] = self._plain_to_count(periods[period])

        return periods

    def _plain_to_count(self, authors):
        count = {}
        for author in authors:
            if author in count.keys():
                continue

            count[author] = authors.count(author)
        return count

def to_epoch (dt):
    return int((dt - datetime.fromtimestamp (0)).total_seconds())

def filter_out_translations (obj):
    def check_for_po (i):
        if i.new != None and i.new.path != None and i.new.path.endswith (".po"):
            return False
        if i.old != None and i.old.path != None and i.old.path.endswith (".po"):
            return False
        return True
    for i in obj.changes():
        if isinstance(i, list):
            for c in i:
                return check_for_po (c)
        return check_for_po (i)
    return True

def main ():
    st = SixMonthStats (sys.argv[1:])
    periods = []
    releases = RELEASES.keys()

    for r in releases:
        periods.append(to_epoch (RELEASES[r]))

    periods.sort()
    stats = st.build_stats_by_periods (periods, filter_out_translations)
    print json.dumps(stats)
    return

if __name__ == '__main__':
  main ()
