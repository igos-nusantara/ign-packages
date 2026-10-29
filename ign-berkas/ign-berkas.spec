Name:           ign-berkas
Epoch:          1
Version:        26
Release:        4
Summary:        Koleksi berkas khas IGOS Nusantara 26
Group:          System Environment/Base
License:        GPLv3+
URL:            http://igos-nusantara.or.id
Source0:        ign-berkas.tar.bz2
BuildArch:      noarch

%description
Paket ini berisi kumpulan berkas konfigurasi, gambar, dan aset lainnya 
khusus untuk IGOS Nusantara 26 yang berbasis AlmaLinux 10.

%prep
# Mengekstrak Source0 (ign-berkas.tar.gz)
%setup -q -n ign-berkas

%install
# Membuat direktori tujuan di dalam buildroot
mkdir -p %{buildroot}/usr/share/ign-berkas

# Menyalin seluruh isi direktori saat ini ke tujuan
cp -p -r * %{buildroot}/usr/share/ign-berkas/

%files
# Menentukan kepemilikan dan lokasi file dalam sistem
%dir /usr/share/ign-berkas
/usr/share/ign-berkas/*

%changelog
* Sun Feb 15 2026 Admin IGOS Nusantara <admin@igos-nusantara.or.id> - 1.0-1
- Rilis awal paket ign-berkas untuk IGN 26 RC
