pkgname=gcompress
pkgver=1.0.0
pkgrel=1
pkgdesc="Easy GUI for compressing videos and pictures using FFmpeg"
arch=('any')
url="https://github.com/Jakub-Chrzanowski/gcompress"
license=('MIT')
depends=('python' 'python-gobject' 'gtk4' 'ffmpeg')
source=("gcompress" "gcompress.desktop" "gcompress.svg")
sha256sums=('B9765E7546B526CA171E88C1C2161A5B9EF6E6B15F9C4F6EEC65AD880458AD26'
            '44A64BF0536CD28C2F25CBE91F9A1EC6F9B70761D8368F86BD38AE55317847C9'
            'F350C89C447CA927696F6218351D50C71C92F6A5B781956C63525E71656015F5')

package() {
    install -Dm755 "$srcdir/gcompress" "$pkgdir/usr/bin/gcompress"
    install -Dm644 "$srcdir/gcompress.desktop" "$pkgdir/usr/share/applications/gcompress.desktop"
    install -Dm644 "$srcdir/gcompress.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/gcompress.svg"
}
