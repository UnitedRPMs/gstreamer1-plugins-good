%global gitdate 20200716
%global commit0 20bbeb5e37666c53c254c7b08470ad8a00d97630
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%global         meson_conf      meson --buildtype=release --prefix=/usr --libdir=%{_libdir} --libexecdir=/usr/libexec --bindir=/usr/bin --sbindir=/usr/sbin --includedir=/usr/include --datadir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --localedir=/usr/share/locale --sysconfdir=/etc

%global debug_package %{nil}

%global         majorminor      1.0
%bcond_without	cairo	
%bcond_with  qt5


%define _legacy_common_support 1	

Name:           gstreamer1-plugins-good
Version:        1.19.3
Release:        7%{dist}
Summary:        GStreamer plugins with good code and licensing

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/

Source0: 	https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.xz
#Patch:		gstreamer1-plugins-good-gcc11.patch

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  meson
BuildRequires:	cmake
BuildRequires:	nasm
BuildRequires:  ninja-build
BuildRequires:  flac-devel >= 1.1.4
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.0
BuildRequires:  libshout-devel
BuildRequires:  libsoup-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXfixes-devel
BuildRequires:  orc-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speex-devel
BuildRequires:  taglib-devel
BuildRequires:  wavpack-devel
BuildRequires:  libv4l-devel
BuildRequires:  libvpx-devel >= 1.1.0
BuildRequires:	aalib-devel
BuildRequires:	libcaca-devel
%{?with_cairo:BuildRequires:	cairo-devel >= 1.10.0}
%{?with_cairo:BuildRequires:	cairo-gobject-devel >= 1.10.0}
BuildRequires:	libgudev1-devel
BuildRequires:	zlib-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	gcc-c++
BuildRequires:	make
BuildRequires:  lame-devel
BuildRequires:  twolame-devel
BuildRequires:  mpg123-devel
BuildRequires:  libcaca-devel
# gtk
BuildRequires:  gtk3-devel >= 3.4
BuildRequires:	mesa-libGLES-devel
# qt
%if ! %{with qt5}
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5WaylandClient)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-linguist
BuildRequires:	pkgconfig(Qt5Help)
%endif

%ifnarch s390 s390x
BuildRequires:  libavc1394-devel
BuildRequires:  libdv-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
%endif

# extras
BuildRequires:  jack-audio-connection-kit-devel
#

# documentation
BuildRequires:  gtk-doc
BuildRequires:  python-devel
#

Recommends:	mpg123


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

%package gtk
Summary:         GStreamer "good" plugins gtk plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}
# handle upgrade path
Obsoletes:       gstreamer1-plugins-bad-free-gtk < 1.13.1-2
Provides:        gstreamer1-plugins-bad-free-gtk = %{version}-%{release}
Provides:        gstreamer1-plugins-bad-free-gtk%{?_isa} = %{version}-%{release}
 
%description gtk
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.
 
GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.
 
This package (%{name}-gtk) contains the gtksink output plugin.

%if ! %{with qt5}
%package qt
Summary:         GStreamer "good" plugins qt qml plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description qt
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.
 
GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.
 
This package (%{name}-qt) contains the qtsink output plugin.
%endif

%package extras
Summary:        Extra GStreamer plugins with good code and licensing
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description extras
GStreamer is a streaming media framework, based on graphs of filters
which operate on media data.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

%{name}-extras contains extra "good" plugins
which are not used very much and require additional libraries
to be installed.



%prep
%autosetup -n gst-plugins-good-%{version} -p1
rm -rf common && git clone https://github.com/GStreamer/common.git

sed -i "s/gst-plugin-scanner/gst-plugin-scanner-%{_target_cpu}/" meson.build

%build
%meson_conf _build \
  -D package-name='UnitedRPMs GStreamer-plugins-good package' \
  -D package-origin='https://unitedrpms.github.io' \
  -D doc=disabled \
  -D gtk_doc=disabled \
  -D orc=enabled \
  -D jack=enabled \
  -D bz2=enabled \
  -D zlib=enabled \
  -D rpicamsrc=disabled \
  -D default-visualizer=autoaudiosink \
  -D tests=disabled \
  %if %{with qt5}
  -D qt5=disabled \
  %endif
%ifarch s390 s390x
  -D dv=disabled -D dv1394=disabled \
%endif

 
%meson_build -C _build

%install
%meson_install -C _build 


# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_metainfodir}
cat > %{buildroot}%{_metainfodir}/gstreamer-good.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-good</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs</name>
  <summary>Multimedia playback for APE, AVI, DV, FLAC, FLX, Flash, MKV, MP4, Speex, VP8, VP9 and WAV</summary>
  <description>
    <p>
      This addon includes several good quality codecs that are well tested.
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-good-%{majorminor}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files -f gst-plugins-good-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS
%{_metainfodir}/gstreamer-good.appdata.xml
# Equaliser presets
%dir %{_datadir}/gstreamer-%{majorminor}/presets/
%{_datadir}/gstreamer-%{majorminor}/presets/GstVP8Enc.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstIirEqualizer10Bands.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstIirEqualizer3Bands.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstQTMux.prs

# non-core plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstalphacolor.so
%{_libdir}/gstreamer-%{majorminor}/libgstalpha.so
%{_libdir}/gstreamer-%{majorminor}/libgstapetag.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofx.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioparsers.so
%{_libdir}/gstreamer-%{majorminor}/libgstauparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstautodetect.so
%{_libdir}/gstreamer-%{majorminor}/libgstavi.so
%{_libdir}/gstreamer-%{majorminor}/libgstcutter.so
%{_libdir}/gstreamer-%{majorminor}/libgstdebug.so
%{_libdir}/gstreamer-%{majorminor}/libgstdeinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtmf.so
%{_libdir}/gstreamer-%{majorminor}/libgsteffectv.so
%{_libdir}/gstreamer-%{majorminor}/libgstequalizer.so
%{_libdir}/gstreamer-%{majorminor}/libgstflv.so
%{_libdir}/gstreamer-%{majorminor}/libgstflxdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom2k1.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom.so
%{_libdir}/gstreamer-%{majorminor}/libgsticydemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3demux.so
%{_libdir}/gstreamer-%{majorminor}/libgstimagefreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterleave.so
%{_libdir}/gstreamer-%{majorminor}/libgstisomp4.so
%{_libdir}/gstreamer-%{majorminor}/libgstlevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstmatroska.so
%{_libdir}/gstreamer-%{majorminor}/libgstmulaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultifile.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultipart.so
%{_libdir}/gstreamer-%{majorminor}/libgstnavigationtest.so
%{_libdir}/gstreamer-%{majorminor}/libgstoss4.so
%{_libdir}/gstreamer-%{majorminor}/libgstreplaygain.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtsp.so
%{_libdir}/gstreamer-%{majorminor}/libgstshapewipe.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmpte.so
%{_libdir}/gstreamer-%{majorminor}/libgstspectrum.so
%{_libdir}/gstreamer-%{majorminor}/libgstudp.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideobox.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideocrop.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofilter.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideomixer.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4menc.so
%{?with_cairo:%{_libdir}/gstreamer-%{majorminor}/libgstcairo.so} 

# gstreamer-plugins with external dependencies but in the main package
%{_libdir}/gstreamer-%{majorminor}/libgstflac.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdkpixbuf.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstossaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstpng.so
%{_libdir}/gstreamer-%{majorminor}/libgstpulseaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanager.so
%{_libdir}/gstreamer-%{majorminor}/libgstshout2.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoup.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeex.so
%{_libdir}/gstreamer-%{majorminor}/libgsttaglib.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideo4linux2.so
%{_libdir}/gstreamer-%{majorminor}/libgstvpx.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavpack.so

%{_libdir}/gstreamer-%{majorminor}/libgstlame.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpg123.so
%{_libdir}/gstreamer-%{majorminor}/libgsttwolame.so

%{_libdir}/gstreamer-%{majorminor}/libgstaasink.so
%{_libdir}/gstreamer-%{majorminor}/libgstcacasink.so
%{_libdir}/gstreamer-%{majorminor}/libgstmonoscope.so

%files gtk
# Plugins with external dependencies
# Now the gtk plugin is here (previous in gstreamer1-plugins-bad-free)
%{_libdir}/gstreamer-%{majorminor}/libgstgtk.so

%if ! %{with qt5}
%files qt
%{_libdir}/gstreamer-%{majorminor}/libgstqmlgl.so
%endif

%ifnarch s390 s390x
%{_libdir}/gstreamer-%{majorminor}/libgstdv.so
%{_libdir}/gstreamer-%{majorminor}/libgst1394.so
%endif

%files extras
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so



%changelog

* Wed Nov 17 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.3-7
- Updated to 1.19.3

* Mon Oct 04 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.2-7.git20bbeb5
- Updated to 1.19.2

* Sun Jun 20 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.19.1-7.git0dcb2aa
- Updated to 1.19.1

* Mon Apr 19 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.4-7.git941312f
- Updated to 1.18.4

* Sat Feb 13 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.3-8.gite816c6c
- Rebuilt

* Mon Jan 25 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.3-7.gite816c6c
- Updated to 1.18.3

* Mon Dec 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.2-7.gitcc896a7
- Updated to 1.18.2

* Thu Oct 29 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-7.git7c44cdb
- Updated to 1.18.1

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.0-7.git6ef694c
- Updated to 1.18.0

* Tue Aug 25 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-7.git6419368
- Updated to 1.17.90

* Fri Jul 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.2-7.git629b8bf
- Updated to 1.17.2

* Wed Dec 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-7.gitce07235
- Updated to 1.16.2-7.gitce07235

* Wed Oct 02 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.1-7.gitd7d290b
- Updated to 1.16.1-7.gitd7d290b

* Sat Sep 14 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-8.git646dc1e
- Fix type compatibility issue with glibc 2.30

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-7.git646dc1e
- Updated to 1.16.0-7.git646dc1e

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-7.git48b46e3
- Updated to 1.15.2-7.git48b46e3

* Fri Jan 18 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.1-7.gite579614
- Updated to 1.15.1-7.gite579614

* Wed Oct 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.4-7.gitd88d1b0
- Updated to 1.14.4-7.gitd88d1b0

* Mon Sep 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-7.git9333e82
- Updated to 1.14.3-7.git9333e82

* Fri Jul 20 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.2-7.git4733e97
- Updated to 1.14.2-7.git4733e97

* Mon May 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.1-7.gitf1eed72
- Updated to 1.14.1-7.gitf1eed72

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.0-7.git6854a23
- Updated to 1.14.0-7.git6854a23

* Fri Mar 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.91-7.git14f45c7
- Updated to 1.13.91-7.git14f45c7

* Sun Mar 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.90-7.git0da4d40  
- Updated to 1.13.90-7.git0da4d40

* Wed Nov 08 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.4-7.git2249383
- Updated to 1.12.4-7.git2249383

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.3-7.git4ce0249
- Updated to 1.12.3-7.git4ce0249

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-2.git188ab74
- Updated to 1.12.2-2.git188ab74

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.1-2.git687d43c
- Updated to 1.12.1-2.git687d43c

* Thu May 25 2017 David Vásquez <davidva AT tutanota DOT com> 1.12.0-2.git27f40ec
- Updated to 1.12.0-2.git27f40ec

* Sat Apr 29 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.91-2.git4ae022e
- Updated to 1.11.91-2.git4ae022e

* Thu Apr 20 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.90-2
- Updated to 1.11.90-2

* Mon Feb 27 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-2.20170224git994b1ac
- Solved compatibility with official package

* Fri Feb 24 2017 David Vásquez <davidva AT tutanota DOT com> 1.11.2-1.20170224git994b1ac
- Updated to 1.11.2-1.20170224git994b1ac

* Fri Jan 27 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 1.11.1-1
- Updated to 1.11.1

* Sat Oct 15 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.90-1
- Updated to 1.9.90

* Thu Oct 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.2-1
- Updated to 1.9.2

* Fri Jul 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.9.1-1
- Updated to 1.9.1

* Thu Jun 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.2-1
- Updated to 1.8.2-1

* Wed Apr 20 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 1.8.1-1
- Updated to 1.8.1

* Wed Jan 20 2016 Wim Taymans <wtaymans@redhat.com> - 1.6.3-1
- Update to 1.6.3

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Use license macro for COPYING

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1.5.90-2
- Add optional data to AppStream metadata.

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Sat Jul 18 2015 Francesco Frassinelli <fraph24@gmail.com> - 1.5.2-2
- Add missing dependencies required by ximagesrc. (#1136317)

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 8 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- Remove obsolete patches

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-5
- Rebuilt for GCC 5 C++11 ABI change

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.4.5-4
- rebuild against libvpx 1.4.0

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.4.5-3
- Register as an AppStream component.

* Fri Mar 06 2015 David Woodhouse <dwmw2@infradead.org> - 1.4.5-2
- Don't force RTP jitterbuffer clock-rate (#1199579)

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2.
- Drop old patches

* Fri Aug 29 2014 Hans de Goede <hdegoede@redhat.com> - 1.4.1-2
- Fix v4l2-src not working with some v4l2 devices (bgo#735660)

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0.

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91.

* Tue Jun 17 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.4-1
- Update to 1.2.4.
- Drop old patches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.3-2
- Rebuild for libvpx ABI break. See #1068664
- fix doc build

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Tue Jan 14 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.2-2
- Disable the cairo plugin, we don't package it.

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Sun Mar 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.

* Wed Feb  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-3
- Add gdk-pixbuf2-devel build dep. It was pulled in by something else for gst 0.10

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.0.5-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- Drop speexdec patch. Fixed upstream.
- Drop vp8 patches. Fixed upstream.

* Wed Nov  7 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.2-3
- Fixes for GNOME #687464 and #687793

* Fri Nov  2 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.2-2
- Fixes for vp8dec including GNOME #687376

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- Drop upstream patches since they are included in latest release.

* Wed Oct 24 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.1-2
- Fix target-bitrate for vp8enc

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Tue Oct  2 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-3
- Add required version for vpx-devel. (#862157)

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Fri Sep 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-2
- Add vp8 plugin to package from gst1-plugins-bad. (#859505)

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.
- Drop v4l2-buffer patch. Fixed upstream.

* Wed Aug 15 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Add batch to fix build with recent kernels, the v4l2_buffer input field was removed.
- Use %%global instead of %%define.

* Wed Jul 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec.
