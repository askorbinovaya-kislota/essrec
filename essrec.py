import struct;
import os;
import sys;
import mmap;

def uint8(r):
    return r.read(1)[0];
def uint16(r):
    return int.from_bytes(r.read(2), byteorder="little");
def uint32(r):
    return int.from_bytes(r.read(4), byteorder="little");
def int32(r):
    return int.from_bytes(r.read(4), byteorder="little", signed=True);
def float32(r):
    return struct.unpack("<f", r.read(4))[0];
def wstring(r):
    length = uint16(r);
    return r.read(length).decode("utf-8");
def filetime(r):
    f = {};
    f["lowDateTime"] = int32(r);
    f["highDateTime"] = int32(r);
    return f;

def header(r):
    h = {};
    h["version"] = uint32(r);
    h["saveNumber"] = uint32(r);
    h["playerName"] = wstring(r);
    h["playerLevel"] = uint32(r);
    h["playerLocation"] = wstring(r);
    h["gameDate"] = wstring(r);
    h["playerRaceEditorId"] = wstring(r);
    h["playerSex"] = uint16(r);
    h["playerCurExp"] = float32(r);
    h["playerLvlUpExp"] = float32(r);
    h["filetime"] = filetime(r);
    h["shotWidth"] = uint32(r);
    h["shotHeight"] = uint32(r);
    h["compressionType"] = uint16(r);
    return h;

def savegame(r):
    s = {};
    s["magic"] = b"TESV_SAVEGAME";
    s["headerSize"] = uint32(r);
    s["header"] = header(r);
    # screenshot data
    ver = s["header"]["version"];
    if ver >= 7 and ver <= 9:
        # skyrim LE
        r.seek(3 * s["header"]["shotWidth"] * s["header"]["shotHeight"], os.SEEK_CUR);
    elif ver == 12:
        # skyrim SE
        r.seek(4 * s["header"]["shotWidth"] * s["header"]["shotHeight"], os.SEEK_CUR);
    else:
        raise Exception("game version " + str(ver) + " not supported");
    if s["header"]["compressionType"] == 0:
        raise Exception("uncompressed saves not supported yet");
    s["uncompressedLen"] = uint32(r);
    s["compressedLen"] = uint32(r);
    r.seek(s["compressedLen"], os.SEEK_CUR);
    return s;

def printsaveinfo(saveheader):
    savenum = saveheader["saveNumber"];
    gender = "Female" if saveheader["playerSex"] else "Male";
    race = saveheader["playerRaceEditorId"];
    playername = saveheader["playerName"];
    playerlevel = saveheader["playerLevel"];
    playerloc = saveheader["playerLocation"];
    date = saveheader["gameDate"];
    print(f"Save {savenum}, {gender} {race} {playername} {playerlevel}lvl at {playerloc}, {date}");

outdir = "./saves";
if os.path.exists(outdir):
    raise Exception("outdir exists, please delete " + outdir);
os.mkdir(outdir);

drive = sys.argv[1];
f = open(drive, "rb");
file_len = f.seek(0, os.SEEK_END);
mm = mmap.mmap(f.fileno(), file_len, prot=mmap.PROT_READ);
offset = mm.find(b"TESV_SAVEGAME");
while offset != -1:
    print("found savefile at", offset);
    # dumping
    f.seek(offset + 13); # offset + header
    try:
        save = savegame(f);
    except Exception as e:
        print(f"failed to parse a save: {e}");
        offset = mm.find(b"TESV_SAVEGAME", offset + 13);
        continue;
    printsaveinfo(save["header"]);
    saveend = f.tell();
    savenum = save["header"]["saveNumber"];
    filename = f"{outdir}/{savenum}.ess";
    while os.path.exists(filename): filename += "_1";
    savefile = open(filename, "wb");
    f.seek(offset);
    savefile.write(f.read(saveend - offset));
    savefile.close();
    offset = mm.find(b"TESV_SAVEGAME", offset + 13);

mm.close();
f.close();
