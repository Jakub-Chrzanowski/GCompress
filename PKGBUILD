# Maintainer: (lokalna paczka, budowana samodzielnie przez użytkownika)
pkgname=gcompress
pkgver=1.0.0
pkgrel=1
pkgdesc="Easy GUI for compressing videos and pictures using FFmpeg"
arch=('any')
url="https://github.com/Jakub-Chrzanowski/gcompress"
license=('MIT')
depends=('python' 'python-gobject' 'gtk4' 'ffmpeg')
source=("gcompress" "gcompress.desktop" "gcompress.svg")
sha256sums=('18a4c75dd4ba08430a626b13756e65c4f6e794f4907ef88cfae2775edd153ab8'
            'ea844b937ad0eaf28ff77ace9f21e30b6b7234b9fe3137e89298c300b6381a7a'
            'ec26be6e95115166682bb18943ea234c00ca6d2bee35b585faae49e6fe209d1f')

package() {
    install -Dm755 "$srcdir/gcompress" "$pkgdir/usr/bin/gcompress"
    install -Dm644 "$srcdir/gcompress.desktop" "$pkgdir/usr/share/applications/gcompress.desktop"
    install -Dm644 "$srcdir/gcompress.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/gcompress.svg"
}
