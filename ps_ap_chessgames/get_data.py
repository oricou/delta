import os
import requests
import csv
import bz2
import re
import sys
from collections import OrderedDict

DB_URL = (
    "https://database.lichess.org/standard/lichess_db_standard_rated_2013-11.pgn.bz2"
)


def download_db(db_url, dst_path):
    print("Downloading database...")
    os.makedirs(os.path.dirname(dst_path))
    dst = open(dst_path, "wb")
    response = requests.get(db_url, stream=True)
    total_length = response.headers.get("content-length")

    if total_length is None:
        dst.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            dst.write(data)

            done = int(50 * dl / total_length)
            done_str = "=" * done
            remain_str = " " * (50 - done)
            sys.stdout.write(f"\r[{done_str}{remain_str}] {(done * 2)} %")
            sys.stdout.flush()

    print("\n")


def parse_pgn_line(line):
    key_value = re.match(r'\[(\w+) "([^"]*)"]', line)
    if not key_value:
        line = line[:-1]
        return ("Moves", line) if line else None
    return (key_value.group(1), key_value.group(2))


def pgn_bz2_to_csv(bz2_path, csv_path):
    db_file = bz2.open(bz2_path)

    header = [
        # "Event",
        # "Site",
        # "Round",
        # "Date",
        # "White",
        # "Black",
        "Result",
        # "UTCDate",
        # "UTCTime",
        "WhiteElo",
        "BlackElo",
        # "WhiteRatingDiff",
        # "BlackRatingDiff",
        # "ECO",
        "Opening",
        "TimeControl",
        "Termination",
        # "BlackTitle",
        # "WhiteTitle",
        # "Moves",
    ]
    db_dict = OrderedDict([(key, None) for key in header])
    csv_file = open(csv_path, "w", encoding="UTF8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    line = db_file.readline()
    lines_written = 0
    while line:
        key_value = parse_pgn_line(line.decode("utf-8"))
        if key_value:
            if key_value[0] in header and key_value[1] != "?":
                db_dict[key_value[0]] = key_value[1]
            if key_value[0] == "Moves":
                csv_writer.writerow(list(db_dict.values()))
                db_dict = OrderedDict([(key, None) for key in header])
                lines_written += 1
                sys.stdout.write(
                    f"\rParsing database to csv: {lines_written} lines written"
                )
                sys.stdout.flush()
        line = db_file.readline()
    print()

    csv_file.close()
    db_file.close()


if __name__ == "__main__":
    dst_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    bz2_name = DB_URL[DB_URL.rfind("/") + 1 :]
    bz2_path = os.path.join(dst_directory, bz2_name)
    csv_name = bz2_name.replace(".pgn.bz2", ".csv")
    csv_path = os.path.join(dst_directory, csv_name)

    if os.path.exists(csv_path):
        print('"data/' + csv_name + '"', "already exists. Data extraction canceled.")
    else:
        if not os.path.exists(bz2_path):
            download_db(DB_URL, bz2_path)
        else:
            print(
                '"data/' + bz2_name + '"',
                "already exists. Starting data extraction from this file...",
            )
        pgn_bz2_to_csv(bz2_path, csv_path)
