#!/usr/bin/env python3
import sys, os, struct, collections, json
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
P3D_MAGIC = b'P3D\xff'
def p3d_walk(buf, off, end, out, depth=0, maxdepth=40):
    n = 0
    while off + 12 <= end and n < 100000:
        cid, hlen, dlen = struct.unpack_from('<III', buf, off)
        if dlen < 12 or off + dlen > end: break
        out.append((cid, hlen, dlen, off, depth))
        if hlen < dlen and hlen >= 12 and depth < maxdepth:
            p3d_walk(buf, off + hlen, off + dlen, out, depth + 1, maxdepth)
        off += dlen; n += 1
def parse_p3d(path):
    with open(path,'rb') as f: buf=f.read()
    if buf[:4]!=P3D_MAGIC: return None
    _,hsize,fsize=struct.unpack_from('<III',buf,0)
    out=[]; p3d_walk(buf,hsize,min(fsize,len(buf)),out)
    return out,hsize,fsize,len(buf)
p3d_ids=collections.Counter(); p3d_container_ids=collections.Counter()
p3d_files=0;p3d_fail=0;ext_census=collections.Counter();top_level_ids=collections.Counter()
for dirpath,dirs,files in os.walk(ROOT):
    for fn in files:
        ext=os.path.splitext(fn)[1].lower().lstrip('.'); ext_census[ext]+=1
        path=os.path.join(dirpath,fn)
        if ext=='p3d':
            try:
                res=parse_p3d(path)
                if res is None: continue
                out,hsize,fsize,actual=res; p3d_files+=1
                for cid,hlen,dlen,off,depth in out:
                    p3d_ids[cid]+=1
                    if hlen<dlen: p3d_container_ids[cid]+=1
                    if depth==0: top_level_ids[cid]+=1
            except Exception as e: p3d_fail+=1
print("=== EXTENSION CENSUS ===")
for e,c in ext_census.most_common(40): print(f"{c:6d}  .{e}")
print(f"\n=== P3D: {p3d_files} parsed, {p3d_fail} failed; distinct IDs {len(p3d_ids)}, container IDs {len(p3d_container_ids)} ===")
print("\n=== TOP-LEVEL chunk IDs ===")
for cid,c in top_level_ids.most_common(30): print(f"0x{cid:08X}  x{c}")
print("\n=== MOST COMMON chunk IDs ===")
for cid,c in p3d_ids.most_common(45):
    print(f"0x{cid:08X}  [{'C' if cid in p3d_container_ids else 'L'}]  x{c}")
with open('/sessions/optimistic-blissful-noether/mnt/outputs/p3d_chunk_ids.json','w') as f:
    json.dump({f"0x{k:08X}":{"count":v,"container":k in p3d_container_ids,"container_count":p3d_container_ids.get(k,0)} for k,v in p3d_ids.most_common()},f,indent=1)
print(f"\nWrote {len(p3d_ids)} IDs to p3d_chunk_ids.json")
