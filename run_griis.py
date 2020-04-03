import iso_code_lookup as iso
import requests
import re
import csv

outp = open('griis_check3.csv', mode='w', newline='')
griiswriter = csv.writer(outp, delimiter=';')


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            print('is dict')
            for k, v in obj.items():
                print('in if loop')
                print(k, ':', v)
                if k == key:
                    print('IN append str ')
                    arr.append(v)

                elif isinstance(v, (dict, list)):
                    print('in dict/list loop')
                    extract(v, arr, key)
        elif isinstance(obj, list):
            print('in list loop')
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def runner(eml, keyword, regex_pattern):
    rson = requests.get(eml)
    rson = rson.json()
    rsonus = rson[keyword]
    print('rsonus', rsonus)

    res = extract_values(rsonus, 'keywords')
    print('RUNNER', res)
    # vals = extract_values(res, 'keywords')
    # pt = re.compile('^[A-Za-z]{1,25}(_[A-Z].){1,3}')
    pt = re.compile(regex_pattern)
    # print('vals --- ', vals)
    for j in res:
        print(j[0])
        hit = pt.match(j[0])
        if hit:
            print(j[0], " is MATCH")
            yield j
        else:
            print('Miss...')



# pattern = '^[A-Za-z]{1,25}(_[A-Z].){1,3}'
# pattern = '^[Cc]ountry_([A-Z-]){2,8}'
# pattern = '^[A-Za-z]{1,25}([-_A-Z]){2,9}'
# pattern = '^[A-Za-z]{1,25}([-_A-Za-z]){2,9}'

api = 'https://api.gbif.org/v1/dataset/'
pattern = '^[A-Za-z]{1,10}_([-A-Za-z]){2,9}'

with open('C:\Misc\stuff\griis_2020.csv', mode='r') as griis_csv:
    griisreader = csv.reader(griis_csv, delimiter=';')
    next(griis_csv)
    for row in griis_csv:
        holder = []
        spl = row.split(';')
        print(spl[0], type(spl[0]))
        uuid = spl[0].strip('\"')
        eml = '{}{}'.format(api, uuid)
        print(eml)
        res = runner(eml, 'keywordCollections', pattern)
        for j in res:
            print('RES: {} datasetkey={}'.format(j, uuid))
            griiswriter.writerow([uuid, j])
            holder.append(j)
        if len(holder) == 0:
            griiswriter.writerow([uuid, 'non-standard format/unknown ISO code'])


