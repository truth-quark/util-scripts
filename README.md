# Util-scripts

Dumping ground for utility scripts, typically utilities that are not one offs.

One off & junk code should be stored in other repositories.

## mp3tag

`mp3tag` is a quick & dirty utility to add `id3` tag data to `mp3` files. It's
mostly intended to quickly add tags to music intended for vehicle stereo systems.
Dedicated tagging tools may be better for fixing larger media collections.

NB: some vehicle stereo systems arrange content in **filesystem** order. This
can result in media displaying out of order. Use `fatsort -n` to arrange files in
natural order on storage media.

## rss2sh

`rss2sh` is a convenience script for downloading local copies of podcasts. It
converts RSS feed URLs to shell scripts calling `wget`.
