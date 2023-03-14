import csv


site_set = set()

with open('code_site_single.csv', mode='a', newline='', encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    with open('code_site.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            site = line[1]
            if site in site_set:
                continue
            site_set.add(site)
            writer.writerow(line)
