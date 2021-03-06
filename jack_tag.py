### jack_tag: name information (ID3 among others) stuff for
### jack - tag audio from a CD and encode it using 3rd party software
### Copyright (C) 1999-2003  Arne Zellentin <zarne@users.sf.net>

### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import string
import os, sys
import locale

import jack_functions
import jack_ripstuff
import jack_targets
import jack_helpers
import jack_freedb
import jack_utils
import jack_misc
import jack_m3u

from jack_init import ogg
from jack_init import eyed3
from jack_init import flac
from jack_globals import *

track_names = None
locale_names = None
genretxt = None

a_artist = None
a_title = None


def _set_id3_tag(mp3file, version, encoding, a_title, t_name, track_num, t_artist,
                 genre, year, comment, play_count):
    tag = eyed3.id3.Tag()
    tag.parse(mp3file)
    tag.album = a_title
    tag.title = t_name
    tag.track_num = track_num
    tag.artist = t_artist

    old_genre = tag.genre
    if genre != -1:
        tag.genre = genre
    elif old_genre == None:
        tag.genre = 255

    if year != -1:
        tag.release_date = year
    if comment:
        tag.comments.set(comment)
    tag.play_count = play_count

    tag.save(mp3file, version, encoding=encoding)

def tag(freedb_rename):
    global a_artist, a_title

    ext = jack_targets.targets[jack_helpers.helpers[cf['_encoder']]['target']]['file_extension']

    if cf['_vbr'] and not cf['_only_dae']:
        total_length = 0
        total_size = 0
        for i in jack_ripstuff.all_tracks_todo_sorted:
            total_length = total_length + i[LEN]
            total_size = total_size + jack_utils.filesize(i[NAME] + ext)

    if cf['_set_id3tag'] and not jack_targets.targets[jack_helpers.helpers[cf['_encoder']]['target']]['can_posttag']:
        cf['_set_id3tag'] = 0

    # maybe export?
    if jack_freedb.names_available:
        a_artist = track_names[0][0] # unicode
        a_title = track_names[0][1] # unicode
        p_artist = locale_names[0][0] # string
        p_title = locale_names[0][1] # string

    if cf['_set_id3tag'] or freedb_rename:
        jack_m3u.init()
        # use freedb year and genre data if available
        if cf['_id3_year'] == -1 and len(track_names[0]) >= 3:
            cf['_id3_year'] = track_names[0][2]
        if cf['_id3_genre'] == -1 and len(track_names[0]) == 4:
            cf['_id3_genre'] = track_names[0][3]

        print "Tagging",
        for i in jack_ripstuff.all_tracks_todo_sorted:
            sys.stdout.write(".") ; sys.stdout.flush()
            mp3name = i[NAME] + ext
            wavname = i[NAME] + ".wav"
            if track_names[i[NUM]][0]:
                t_artist = track_names[i[NUM]][0]
            else:
                t_artist = a_artist
            t_name = track_names[i[NUM]][1]
            t_comm = ""
            if not cf['_only_dae'] and cf['_set_id3tag']:
                if len(t_name) > 30:
                    if string.find(t_name, "(") != -1 and string.find(t_name, ")") != -1:
                        # we only use the last comment
                        t_comm = string.split(t_name, "(")[-1]
                        if t_comm[-1] == ")":
                            t_comm = t_comm[:-1]
                            if t_comm[-1] == " ":
                                t_comm = t_comm[:-1]
                            t_name2 = string.replace(t_name, " (" + t_comm + ") ", "")
                            t_name2 = string.replace(t_name2, " (" + t_comm + ")", "")
                            t_name2 = string.replace(t_name2, "(" + t_comm + ") ", "")
                            t_name2 = string.replace(t_name2, "(" + t_comm + ")", "")
                        else:
                            t_comm = ""
                if jack_helpers.helpers[cf['_encoder']]['target'] == "mp3":
                    if cf['_write_id3v2']:
                        _set_id3_tag(
                            mp3name, eyed3.id3.ID3_V2_4,  'utf-8', a_title,
                            t_name, (i[NUM],len(jack_ripstuff.all_tracks_orig)),
                            t_artist, cf['_id3_genre'], cf['_id3_year'], None,
                            int(i[LEN] * 1000.0 / 75 + 0.5)
                        )
                    if cf['_write_id3v1']:
                        # encoding ??
                        _set_id3_tag(
                            mp3name, eyed3.id3.ID3_V1_1,  'latin1',
                            a_title, t_name,
                            (i[NUM],len(jack_ripstuff.all_tracks_orig)),
                            t_artist, cf['_id3_genre'], cf['_id3_year'], t_comm,
                            int(i[LEN] * 1000.0 / 75 + 0.5)
                        )
                elif jack_helpers.helpers[cf['_encoder']]['target'] == "flac":
                    if flac:
                        f = flac.FLAC(mp3name)
                        if f.vc is None: f.add_vorbiscomment()
                        f.vc['ALBUM'] = a_title
                        f.vc['TRACKNUMBER'] = str(i[NUM])
                        f.vc['TITLE'] = t_name
                        f.vc['ARTIST'] = t_artist
                        if cf['_id3_genre'] != -1:
                            f.vc['GENRE'] = id3genres[cf['_id3_genre']]
                        if cf['_id3_year'] != -1:
                            f.vc['DATE'] = str(cf['_id3_year'])
                        f.save()
                    else:
                        print
                        print "Please install python-mutagen package."
                        print "Without it, you'll not be able to tag FLAC tracks."
                elif jack_helpers.helpers[cf['_encoder']]['target'] == "ogg":
                    vf = ogg.vorbis.VorbisFile(mp3name)
                    oggi = vf.comment()
                    oggi.clear()
                    oggi.add_tag('ALBUM', a_title.encode("utf-8"))
                    oggi.add_tag('TRACKNUMBER', `i[NUM]`)
                    oggi.add_tag('TITLE', t_name.encode("utf-8"))
                    oggi.add_tag('ARTIST', t_artist.encode("utf-8"))
                    if cf['_id3_genre'] != -1:
                        oggi.add_tag('GENRE', id3genres[cf['_id3_genre']])
                    if cf['_id3_year'] != -1:
                        oggi.add_tag('DATE', `cf['_id3_year']`)
                    oggi.write_to(mp3name)
            if freedb_rename:
                newname = jack_freedb.filenames[i[NUM]]
                try:
                    i[NAME] = unicode(i[NAME], "utf-8")
                except UnicodeDecodeError:
                    i[NAME] = unicode(i[NAME], "latin-1")
                if i[NAME] != newname:
                    p_newname = newname.encode(locale.getpreferredencoding(), "replace")
                    u_newname = newname
                    newname = newname.encode(cf['_charset'], "replace")
                    p_mp3name = i[NAME].encode(locale.getpreferredencoding(), "replace") + ext
                    p_wavname = i[NAME].encode(locale.getpreferredencoding(), "replace") + ".wav"
                    ok = 1
                    if os.path.exists(newname + ext):
                        ok = 0
                        print 'NOT renaming "' + p_mp3name + '" to "' + p_newname + ext + '" because dest. exists.'
                        if cf['_keep_wavs']:
                            print 'NOT renaming "' + p_wavname + '" to "' + p_newname + ".wav" + '" because dest. exists.'
                    elif cf['_keep_wavs'] and os.path.exists(newname + ".wav"):
                        ok = 0
                        print 'NOT renaming "' + p_wavname + '" to "' + p_newname + ".wav" + '" because dest. exists.'
                        print 'NOT renaming "' + p_mp3name + '" to "' + p_newname + ext + '" because WAV dest. exists.'
                    if ok:
                        if not cf['_only_dae']:
                            try:
                                os.rename(mp3name, newname + ext)
                            except OSError:
                                error('Cannot rename "%s" to "%s" (Filename is too long or has unusable characters)' % (p_mp3name, p_newname + ext))
                            jack_m3u.add(newname + ext)
                        if cf['_keep_wavs']:
                            os.rename(wavname, newname + ".wav")
                            jack_m3u.add_wav(newname + ".wav")
                        jack_functions.progress(i[NUM], "ren", "%s-->%s" % (i[NAME], u_newname))
                    elif cf['_silent_mode']:
                        jack_functions.progress(i[NUM], "err", "while renaming track")
        print

    if not cf['_silent_mode']:
        if jack_freedb.names_available:
            print "Done with \"" + p_artist + " - " + p_title + "\"."
        else:
            print "All done.",
        if cf['_set_id3tag'] and cf['_id3_year'] != -1:
            print "Year: %4i" % cf['_id3_year'],
            if cf['_id3_genre'] == -1: print
        if cf['_set_id3tag'] and cf['_id3_genre'] != -1:
            if cf['_id3_genre'] <0 or cf['_id3_genre'] > len(id3genres):
                print "Genre: [unknown]"
            else:
                print "Genre: %s" % id3genres[cf['_id3_genre']]
        if cf['_vbr'] and not cf['_only_dae']:
            print "Avg. bitrate: %03.0fkbit" % ((total_size * 0.008) / (total_length / 75))
        else:
            print

    if jack_m3u.m3u:
        os.environ["JACK_JUST_ENCODED"] = "\n".join(jack_m3u.m3u)
    if jack_m3u.wavm3u:
        os.environ["JACK_JUST_RIPPED"] = "\n".join(jack_m3u.wavm3u)
    jack_m3u.write()
