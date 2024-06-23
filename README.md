# essrec
recovers your skyrim saves, like photorec, but only for .ess

# usage
`sudo python essrec.py /dev/sdXN`
where /dev/sdXN - your block device (can be partition or full device)
(can also point to hard drive image, raw or vhd/qcow2/whatever)

found saves are copied to `saves/NUM.ess` (NUM is save number),
make sure that "saves" directory does not exist

if multiple numbers are found, filename would have "_1" appended to it - so usually autosaves are
something like `134.ess_1_1_1_1`

this script will not work on failing hdds, please make a disk image with `ddrescue` if you get i/o errors

tested only on linux

example output (of a successful run):
```
Save 26, Male KhajiitRace AKislota 18lvl at Устенгрев, 008.49.55
found savefile at 1705762816
Save 27, Male KhajiitRace AKislota 19lvl at Устенгрев - Глубины, 009.23.07
found savefile at 1875513344
Save 14, Male KhajiitRace AKislota 15lvl at Скайрим, 006.26.06
found savefile at 2136977408
Save 134, Male KhajiitRace AKislota 43lvl at Дом теплых ветров, 041.15.14
found savefile at 2658910208
Save 51, Male KhajiitRace AKislota 23lvl at Скайрим, 014.14.08
found savefile at 3767611392
Save 4, Male KhajiitRace AKislota 9lvl at Скайрим, 002.56.32
found savefile at 3899244544
Save 121, Male KhajiitRace AKislota 42lvl at Вайтран, 035.27.12
found savefile at 4045172736
Save 2, Male KhajiitRace AKislota 6lvl at Скайрим, 001.35.22
found savefile at 4740820992
Save 127, Male KhajiitRace AKislota 43lvl at Скулдафн - Храм, 037.46.29
```

i used this https://en.m.uesp.net/wiki/Skyrim_Mod:Save_File_Format wiki page while making essrec

it is possible to recover .ess saves because it can be read without known file size, so works when fs
was formatted multiple times

and also, it won't work on ssds with TRIM enabled (but you may still try your luck)
