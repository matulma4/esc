import argparse

def get_ids(fname):
    dictionary = []
    with open(fname) as f:
        for line in f:
            halves = line.split('#')
            data = [a.split(':')[0] for a in halves[0].split(' ')][2:-1]
            for id in data:
                if id not in dictionary:
                    dictionary.append(id)
    return dictionary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ids.")
    parser.add_argument("dataname",help="dataset",type=str)
    parser.add_argument("outname",help="outfile",type=str)
    args = parser.parse_args()
    dct = get_ids(args.dataname)
    with open(args.outname,'w') as f:
        for d in dct:
            f.write(d+"\n")
