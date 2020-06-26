# Jack - Rip and encode CDs with one command

Jack has been developed with one main goal: making OGGs (or MP3s)
without having to worry. There is nearly no way that an incomplete rip
goes unnoticed, e.g. jack compares WAV and OGG file sizes when
continuing from a previous run. Jack also checks your HD space before
doing anything (even keeps some MB free).

Jack is different from other such tools in a number of ways:
- it supports different rippers and encoders
- it is very configurable
- it doesn't need X
- it can "rip" virtual CD images like the ones created by cdrdao
- when using cdparanoia, cdparanoia's status information is displayed and archived for all tracks, so you can see if something went wrong
- it uses sophisticated disk space management, i.e. it schedules its ripping/encoding processes depending on available space.
- gnudb query, file renaming and id3/ogg-tagging
- it can resume work after it has been interrupted. If all tracks have been ripped, it doesn't even need the CD anymore, even if you want to do a gnudb query.
- it can do a gnudb query based on OGGs alone, like if you don't remember from which CD those OGGs came from.
- gnudb submissions

## News

Jack is back! After a small 15 year hiatus, development has resumed.

Many thanks to the [friendly Debian maintainers](https://github.com/zzarne/jack/blob/master/debian/copyright) who kept Jack alive all these years!

Support for Python versions before 3 has been dropped.

## Goals

Current development goals include:
- Test and complete support for Python 3
- Get Jack back into distributions which no longer support Python 2
- Get Jack into PyPI
- Get the character encodings right. It's been a mess in old Python and Jack
- Rework the helpers and plugins into separate Python modules