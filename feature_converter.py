import argparse
def load_ids(fname):
    return [id[:-1] for id in open(fname)]

def convert_features(dct, fname, outname):
    with open(fname) as f:
        with open(outname,'w') as g:
            for line in f:
                halves = line.split('#')
                data = [a.split(':')[0] for a in halves[0].split(' ')][2:-1]
                missing = list(set(dct) - set(data))
                for m in missing:
                    halves[0] += m+":0.0 "
                g.write(halves[0]+"#"+halves[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ids.")
    parser.add_argument("dataname",help="dataset",type=str)
    parser.add_argument("ftrname",help="ftrset",type=str)
    parser.add_argument("outname",help="outfile",type=str)
    args = parser.parse_args()
    dct = load_ids(args.dataname)
    convert_features(dct,args.ftrname,args.outname)