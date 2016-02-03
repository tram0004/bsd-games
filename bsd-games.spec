# Ick!  This is only a temporary hack until I have more time
# to rebase the affected patches (#4, and possibly more)

Summary: Collection of text-based games
Name: bsd-games
Version: 2.17
Release: 49%{?dist}
License: BSD and BSD with advertising
Group: Amusements/Games
URL: ftp://metalab.unc.edu/pub/Linux/games/
Source0: ftp://metalab.unc.edu/pub/Linux/games/bsd-games-%{version}.tar.gz
Source1: config.params
# Updated acronym databases
Source2: http://cvsweb.netbsd.org/cgi-bin/cvsweb.cgi/~checkout~/src/share/misc/acronyms
Source3: http://cvsweb.netbsd.org/cgi-bin/cvsweb.cgi/~checkout~/src/share/misc/acronyms.comp
# A collection of patches from Debian.
Patch0: bsd-games-2.17-debian.patch
# Patches from Fedora Core 1
Patch1: bsd-games-2.17-ospeed.patch
Patch2: bsd-games-2.17-getline.patch
Patch3: bsd-games-2.17-utmpstruct.patch
# Additional new patches
Patch4: bsd-games-2.17-setresgid.patch
Patch5: bsd-games-2.17-tetrisgid.patch
Patch6: bsd-games-2.17-hackgid.patch
Patch7: bsd-games-2.17-phantasiagid.patch
# Add patches for man page renames
Patch8: bsd-games-2.17-monop-rename.patch
Patch9: bsd-games-2.17-banner-rename.patch
Patch10: bsd-games-2.17-stdio-c++.patch
Patch11: bsd-games-2.17-nolibtermcap.patch
Patch12: bsd-games-2.17-tetris-rename.patch
Patch13: bsd-games-2.17-gcc43.patch
Patch14: bsd-games-2.17-bogglewords.patch
Patch15: bsd-games-2.17-wtfupdate.patch
Patch16: bsd-games-2.17-backgammonsize.patch
Patch17: bsd-games-2.17-adventurecrc.patch
Patch18: bsd-games-2.17-wtfrpm.patch
Patch19: bsd-games-2.17-adventureinit.patch
Patch20: bsd-games-2.17-backgammonrecursion.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel words flex flex-static bison
Requires(pre): shadow-utils

%description
Bsd-games includes adventure, arithmetic, atc, backgammon, battlestar,
bcd, caesar, canfield, cfscores, cribbage, go-fish, gomoku,
hunt, mille, mpoly, morse, number, phantasia, pig, pom, ppt, primes,
quiz, rain, random, robots, rot13, sail, snake, snscore, teachgammon,
bsd-fbg, trek, worm, worms and wump.

%prep
%setup -q
install -p -m 755 %{SOURCE1} .
%patch0 -p1 -b .debian
%patch1 -p1 -b .ospeed
%patch2 -p1 -b .getline
%patch3 -p1 -b .utmpstruct
%patch4 -p1 -b .setresgid
%patch5 -p1 -b .tetrisgid
%patch6 -p1 -b .hackgid
%patch7 -p1 -b .phantasiagid
%patch8 -p1 -b .monop.rename
%patch9 -p0 -b .banner.rename
%patch10 -p0 -b .cplusplus
%patch11 -p0 -b .nolibtermcap
%patch12 -p0 -b .tetris.rename
%patch13 -p1 -b .gcc43
%patch14 -p0 -b .wordlimit
%patch15 -p0 -b .wtfupdate
%patch16 -p0 -b .backgammonsize
%patch17 -p0 -b .adventurecrc
%patch18 -p1 -b .wtfrpm
%patch19 -p0 -b .adventureinit
%patch20 -p1 -b .backgammonrecursion

%build
# We include a templatized configuration settings file to set
# reasonable defaults, and to tell the configure script not to
# run in interactive mode.
sed -i.bak -e "s#@DESTDIR@#$RPM_BUILD_ROOT#" \
    -e "s#@bindir@#%{_bindir}#" \
    -e "s#@docdir@#%{_docdir}#" \
    -e "s#@sbindir@#%{_sbindir}#" \
    -e "s#@datadir@#%{_datadir}#" \
    -e "s#@libdir@#%{_libdir}#" \
    -e "s#@mandir@#%{_mandir}#" \
    -e "s#@var@#%{_var}#" \
    -e "s#@RPM_OPT_FLAGS@#$RPM_OPT_FLAGS#" \
    config.params 

# Don't use %%configure.  This configure script wasn't generated by
# autoconf and doesn't obey things like --prefix.
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" %{?_smp_mflags}

# Rename one doc file to avoid naming collisions
cp hunt/README README.hunt

%install
rm -rf $RPM_BUILD_ROOT
make RPM_BUILD_ROOT="$RPM_BUILD_ROOT" install

# Change the binary name for monop to prevent a conflict with the mono-devel
# package
mv $RPM_BUILD_ROOT/%{_bindir}/monop $RPM_BUILD_ROOT/%{_bindir}/mpoly
mv $RPM_BUILD_ROOT/%{_mandir}/man6/monop.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/mpoly.6.gz

# Change the binary name for banner to prevent a conflict with a Fedora
# package with the same name
mv $RPM_BUILD_ROOT/%{_bindir}/banner $RPM_BUILD_ROOT/%{_bindir}/vert-banner
mv $RPM_BUILD_ROOT/%{_mandir}/man6/banner.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/vert-banner.6.gz

# Change the binary name for tetris to prevent a conflict with the mono-devel
# package
mv $RPM_BUILD_ROOT/%{_bindir}/tetris-bsd $RPM_BUILD_ROOT/%{_bindir}/bsd-fbg
mv $RPM_BUILD_ROOT/%{_mandir}/man6/tetris-bsd.6.gz $RPM_BUILD_ROOT/%{_mandir}/man6/bsd-fbg.6.gz

# Remove this doc file.  We're copying it to a different location for Fedora.
rm -f $RPM_BUILD_ROOT/%{_docdir}/trek.me

# Updated acronym databases
install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/misc/
install -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/misc/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
for group in gamehack gamesail gamephant; do
    getent group $group >/dev/null || groupadd -r $group
done
exit 0

%files
%defattr(-,root,root)
%{_bindir}/adventure
%{_bindir}/arithmetic
%attr(2755,root,games) %{_bindir}/atc
%{_bindir}/backgammon
%{_bindir}/teachgammon
%attr(2755,root,games) %{_bindir}/battlestar
%{_bindir}/boggle
%{_bindir}/bcd
%{_bindir}/caesar
%{_bindir}/dab
%{_bindir}/rot13
%attr(2755,root,games) %{_bindir}/canfield
%{_bindir}/cfscores
%attr(2755,root,games) %{_bindir}/cribbage
%{_bindir}/go-fish
%{_bindir}/gomoku
%attr(2755,root,gamehack) %{_bindir}/hack
%{_bindir}/hangman
%{_bindir}/hunt
%{_bindir}/mille
%{_bindir}/mpoly
%{_bindir}/morse
%{_bindir}/number
%attr(2755,root,gamephant) %{_bindir}/phantasia
%{_bindir}/pig
%{_bindir}/pom
%{_bindir}/ppt
%{_bindir}/primes
%{_bindir}/quiz
%{_bindir}/rain
%{_bindir}/random
%attr(2755,root,games) %{_bindir}/robots
%attr(2755,root,gamesail) %{_bindir}/sail
%attr(2755,root,games) %{_bindir}/snake
%{_bindir}/snscore
%attr(2755,root,games) %{_bindir}/bsd-fbg
%{_bindir}/trek
%{_bindir}/vert-banner
%{_bindir}/worm
%{_bindir}/worms
%{_bindir}/wtf
%{_bindir}/wump
%{_datadir}/%{name}
%{_datadir}/misc/acronyms
%{_datadir}/misc/acronyms.comp
%{_mandir}/man6/*
%{_sbindir}/huntd
%config(noreplace) %attr(664,root,games) %{_var}/games/atc_score
%config(noreplace) %attr(664,root,games) %{_var}/games/battlestar.log
%config(noreplace) %attr(664,root,games) %{_var}/games/cfscores
%config(noreplace) %attr(664,root,games) %{_var}/games/criblog
%dir %attr(0775,root,gamehack) %{_var}/games/hack
%config(noreplace) %attr(664,root,gamehack) %{_var}/games/hack/*
%dir %attr(775,root,gamephant) %{_var}/games/phantasia
%config(noreplace) %attr(664,root,gamephant) %{_var}/games/phantasia/*
%dir %attr(775,root,gamesail) %{_var}/games/sail
%config(noreplace) %attr(664,root,games) %{_var}/games/robots_roll
%config(noreplace) %attr(664,root,gamesail) %{_var}/games/saillog
%config(noreplace) %attr(664,root,games) %{_var}/games/snake.log
%config(noreplace) %attr(664,root,games) %{_var}/games/snakerawscores
%config(noreplace) %attr(664,root,games) %{_var}/games/bsd-fbg.scores
%doc AUTHORS COPYING ChangeLog ChangeLog.0 THANKS YEAR2000 README.hunt trek/USD.doc/trek.me

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.17-47
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Jeff Makey <jeff@makey.net> - 2.17-45
- Fix infinite recursion in backgammon. (BZ #1092874)
- Fix bogus dates in changelog.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Jeff Makey <jeff@makey.net> - 2.17-43
- Update acronym databases. (BZ #1032327)

* Tue Aug 27 2013 Jeff Makey <jeff@makey.net> - 2.17-42
- Fix segmentation fault in adventure initialization. (BZ #997933)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Jaromir Capik <jcapik@redhat.com> - 2.17-40
- wtf: Removing duplicate prefix when rpm -q succeeds

* Thu Apr 25 2013 Jan Pokorny <jpokorny@redhat.com> - 2.17-39
- Make wtf fetch package info from rpm instead of pkg_info
  (BZ #956648)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 Jeff Makey <jeff@makey.net> - 2.17-36
- Fix segmentation fault on 64-bit systems when saving adventure game.
  (BZ #710936)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.17-34
- Fix Requires(pre) syntax for group creation.
- Create groups as specified in packaging guidelines.

* Tue May  3 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.17-33
- Update acronym databases, fix URLs to them (#529921).

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 2.17-31
- Add BR: flex-static (Fix FTBFS: BZ 660856).

* Sun Apr 18 2010 Wart <wart@kobold.org> 2.17-30
- Add patch to fix core dump in backgammon when screen is < 24 lines tall

* Tue Oct 20 2009 Wart <wart@kobold.org> 2.17-29
- Updated acronym databases (BZ #529921)
- Allow more words in a boggle game (BZ #500187)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Wart <wart@kobold.org> 2.17-26
- Minor tweaks to patches to get them to work with no fuzz

* Mon Oct 20 2008 Wart <wart@kobold.org> 2.17-25
- Fix robots high score file permissions (BZ# 467726)

* Wed Oct 8 2008 Wart <wart@kobold.org> 2.17-24
- Temporarily set patch fuzz factor until patches can be rebased.

* Sat Feb 9 2008 Wart <wart@kobold.org> 2.17-23
- Add patch and rebuild for gcc 4.3

* Tue Nov 20 2007 Wart <wart@kobold.org> 2.17-22
- Create setgid groups as system groups (BZ# 389191)

* Fri Aug 17 2007 Wart <wart@kobold.org> 2.17-21
- License tag clarification
- Minor rpmlint cleanup

* Mon Apr 30 2007 Wart <wart@kobold.org> 2.17-20
- Fix one more place where tetris must be renamed to bsd-fbg

* Mon Apr 30 2007 Wart <wart@kobold.org> 2.17-19
- Rename tetris to avoid legal quandries

* Tue Mar 6 2007 Wart <wart@kobold.org> 2.17-18
- Remove BR: libtermcap-devel
- Change includes of <termcap.h> to <ncurses/termcap.h>

* Tue Jan 30 2007 Wart <wart@kobold.org> 2.17-17
- Patch to add extern "C" block to prevent c++ compiler error.

* Sat Nov 18 2006 Wart <wart@kobold.org> 2.17-16
- Drop the useless game 'wargames'

* Sat Oct 14 2006 Wart <wart@kobold.org> 2.17-15
- Reintroduce the 'banner' program as 'vert-banner' (BZ #209018)

* Mon Aug 28 2006 Wart <wart@kobold.org> 2.17-14
- Rebuild for Fedora Extras

* Wed May 31 2006 Wart <wart@kobold.org> 2.17-13
- Added missing BR: bison

* Wed May 31 2006 Wart <wart@kobold.org> 2.17-12
- Added missing BR: flex

* Tue May 2 2006 Wart <wart@kobold.org> 2.17-11
- Rename monop man page to match the renamed executable.

* Mon May 1 2006 Wart <wart@kobold.org> 2.17-10
- Remove banner (conflict with a similar package in FE)

* Sat Apr 29 2006 Wart <wart@kobold.org> 2.17-9
- Simplify files section
- Remove unnecessary comment
- Mark scoreboard files as %%config

* Fri Apr 28 2006 Wart <wart@kobold.org> 2.17-8
- Fix directory ownership of _datadir/bsd-games
- Change license to BSD

* Thu Apr 27 2006 Wart <wart@kobold.org> 2.17-7
- Remove dm for Fedora
- Turn off setgid bit for cfscores
- Limit setgid code segments in hack
- Limit setgid code segments in phantasia

* Wed Apr 26 2006 Wart <wart@kobold.org> 2.17-6
- Remove bones file modifications from hack and run with a custom group
  instead.

* Mon Apr 24 2006 Wart <wart@kobold.org> 2.17-5
- Modified bones file handling to allow us to drop setgid earlier.

* Sat Apr 22 2006 Wart <wart@kobold.org> 2.17-4
- Added dist tag to release number
- Added patch to limit potential security holes in tetris-bsd
- Added patch set from Debian's package, which includes a security patch
  for CVE-2006-1744
- Rename monop to mpoly to avoid conflict with the mono-devel package.

* Fri Apr 14 2006 Wart <wart@kobold.org> 2.17-3
- Updated setresgid patch to disable potential security holes from
  user-specified scoreboard files.
- Move hack save games to $HOME, but can be moved using HACKDIR or the
  '-d' command line option.

* Sat Apr 8 2006 Wart <wart@kobold.org> 2.17-2
- Added patch to change use of setregid to setresgid almost everywhere.
- Added missing BuildRequires

* Mon Apr 3 2006 Wart <wart@kobold.org> 2.17-1
- Updated to 2.17 with new configuration system
- Updated patches for 2.17
- Updated spec file for Fedora Extras

* Fri Feb 16 2001 Tim Powers <timp@redhat.com>
- fixed getline() redefinition, it is included in stdio.h now, so 
  getline had to be renamed. Also, -D_GNU_SOURCE
- fix bug 27850, where certain games need to be setgid games, and 
  their scorefiles etc. need to belong to group games

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- fix bug #15013, bad dir permissions

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- don't use internal rpm programs 
- kill countmail, no longer require frm from elm

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- fixed man page location to be in %%{_mandir}
- fixed so that regular users can build

* Fri May 5 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0
- compress man pages

* Thu Feb 10 2000 Tim Powers <timp@redhat.com>
- strip binaries.

* Sun Nov 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9

* Mon Nov 1 1999 Tim Powers <timp@redhat.com>
- updated source to 2.8
- fixed problem with ospeed being defined in the source instead of including
  termcap.h (new ospeed patch)
- using files list in %%files section instead of entering
  _every_single_filename_.

* Sat Aug 21 1999 Bill Nottingham <notting@redhat.com>
- fix countmail (#3722). I must be bored.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- make dm setgid games, not setuid root...

* Fri Jul 9 1999 Tim Powers <timp@redhat.com>
- updated source to 2.7
- updated patches to fix bugs and the braindead configure script, 
  dropped a few of the older patches that made it into this release
- replaced -make install with make install-strip
- built for 6.1

* Wed May 12 1999 Bill Nottingham <notting@redhat.com>
- pick up some more files

* Thu Apr 01 1999 Michael Maher <mike@redhat.com>
- only a fool would add a dependency to this package on a 
  day like today.

* Thu Mar 18 1999 Michael Maher <mike@redhat.com>
- fixed bug 1550

* Mon Feb 08 1999 Michael Maher <mike@redhat.com>
- moved pacakge to PowerTools.

* Thu Jun 18 1998 Alan Cox <alan@redhat.com>
- Chris Evans pointed out a hole in sail I missed.

* Wed Jun 17 1998 Alan Cox <alan@redhat.com>
- Stopped people using cribbage to be able to cheat game score files.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixed the config patch so that it will build on non /usr/src/redhat build
  trees

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to bsd-games 2.1
- started over on package
