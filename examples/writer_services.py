import csv
import aiofiles
from io import StringIO
from typing import Iterator
from itertools import chain
from octoscrape.config import common_config


async def write_to_csv(worker_name: str, data_iter:Iterator[dict[str, str]], *, delimiter=";"):
    file_path = common_config.PathToCsvDir / f"{worker_name}.csv"

    file_exists = file_path.exists()

    output = StringIO()
    writer = csv.writer(output, delimiter=delimiter)

    # form a string in the correct order
    data = next(data_iter)
    keys = sorted(list(data.keys()))

    # if the file is new, write the headers
    if not file_exists:
        writer.writerow(keys)

    writer.writerows((d.get(column, "") for column in keys) 
                     for d in chain((data,), data_iter))

    # asynchronously write data to the file
    async with aiofiles.open(file_path, mode='a', encoding='utf-8', newline='') as f:
        await f.write(output.getvalue())