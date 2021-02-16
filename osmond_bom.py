import argparse

def process_osmond_file(in_file):
    fh = open(in_file, 'r')
    lines = fh.readlines()
    part_count = {}
    for l in lines:
        l_line = l.split()
        if (len(l_line) > 0 and l_line[0] == "Part"):
            part_type = l_line[1]
            # rename to part_name if part_type is void
            if (part_type == "void"):
                part_type = l_line[4]
            value = None
            for p in range(len(l_line)):
                if (l_line[p] == "Value"):
                    value = l_line[p+1]
                    break
            if value != None:
                part_name = part_type + "_" + value
            else:
                part_name = part_type
            if part_name in part_count:
                part_count[part_name] += 1
            else:
                part_count[part_name] = 1
    fh.close()
    return part_count

def write_bom(out_file, part_count):
    fh = open(out_file, 'w')
    for p in part_count:
        fh.write("{}, {} \n".format(p, part_count[p]))
    fh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                description='Generate a BOM from an Osmond PCB file.'
            )
    parser.add_argument('input', metavar='input', type=str,
                    help='input file')
    parser.add_argument('output', metavar='output', type=str,
                    help='output file')

    args = parser.parse_args()
    in_file = args.input
    out_file = args.output

    part_count = process_osmond_file(in_file)
    write_bom(out_file, part_count)
