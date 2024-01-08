# Util-scripts

Dumping ground for utility scripts, potentially one off code, or even junk code that might be worth keeping...

## mp3tag

`mp3tag` is a quick & dirty utility to add `id3` tag data to `mp3` files. It's
mostly intended to quickly add tags to music intended for vehicle stereo systems.
Dedicated tagging tools may be better for fixing larger media collections.

NB: some vehicle stereo systems arrange content in **filesystem** order. This
can result in media displaying out of order. Use `fatsort -n` to arrange files in
natural order on storage media.
