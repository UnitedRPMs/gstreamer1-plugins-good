%global gitdate 20170920
%global commit0 4ce0249911fb4dda1a7e643a91490a10f2a6d415
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%global         majorminor      1.0


Name:           gstreamer1-plugins-good
Version:        1.12.3
Release:        7%{?gver}%{dist}
Summary:        GStreamer plugins with good code and licensing

License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/

Source0: 	https://github.com/GStreamer/gst-plugins-good/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

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
BuildRequires:	cairo-devel
BuildRequires:	libgudev1-devel
BuildRequires:	zlib-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:	git
BuildRequires:	autoconf-archive
BuildRequires:	intltool
BuildRequires:	libtool


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
%autosetup -n gst-plugins-good-%{commit0} 
rm -rf common && git clone git://anongit.freedesktop.org/gstreamer/common  

%build

NOCONFIGURE=1 ./autogen.sh

%if 0%{?fedora} >= 26
CFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wall -Wno-error" CXXFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wall -Wno-error" CPPFLAGS="-Wdate-time -D_FORTIFY_SOURCE=2" LDFLAGS="-Wl,-z,relro -Wl,-z,defs -Wl,-O1 -Wl,--as-needed"
%endif

%configure \
  --with-package-name='Fedora GStreamer-plugins-good package' \
  --with-package-origin='https://unitedrpms.github.io/' \
  --enable-experimental \
  --enable-gtk-doc \
  --enable-orc \
  --enable-jack \
  --enable-bz2 \
  --with-default-visualizer=autoaudiosink \
  --enable-silent-rules \
  --enable-zlib 

  # https://bugzilla.gnome.org/show_bug.cgi?id=655517
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool


make %{?_smp_mflags} V=0


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-good.appdata.xml <<EOF
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
%{_datadir}/appdata/*.appdata.xml
%doc %{_datadir}/gtk-doc/html/gst-plugins-good-plugins-%{majorminor}

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
%{_libdir}/gstreamer-%{majorminor}/libgstcairo.so

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

%{_libdir}/gstreamer-%{majorminor}/libgstaasink.so
%{_libdir}/gstreamer-%{majorminor}/libgstcacasink.so
%{_libdir}/gstreamer-%{majorminor}/libgstmonoscope.so


%ifnarch s390 s390x
%{_libdir}/gstreamer-%{majorminor}/libgstdv.so
%{_libdir}/gstreamer-%{majorminor}/libgst1394.so
%endif

%files extras
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so



%changelog

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
