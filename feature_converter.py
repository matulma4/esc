import argparse
def load_ids(fname):
    return [id[:-1] for id in open(fname)]

def convert_features(fname, outname, ftr):
    with open(fname) as f:
        with open(outname,'w') as g:
            for line in f:
                halves = line.split('#')
                data = [a.split(':') for a in halves[0].split(' ')]
                new_line = data[0][0]+" "+data[1][0]+":"+data[1][1]+" "
                for f in data[2:-1]:
                    if int(f[0]) != ftr:
                        new_line += f[0]+":"+f[1]+" "
                g.write(new_line+"#"+halves[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ids.")
    # parser.add_argument("dataname",help="dataset",type=str)
    parser.add_argument("ftrname",help="ftrset",type=str)
    parser.add_argument("outname",help="outfile",type=str)
    parser.add_argument("ftr",help="feature",type=int)
    args = parser.parse_args()
    # dct = load_ids(args.dataname)
    convert_features(args.ftrname,args.outname,args.ftr)