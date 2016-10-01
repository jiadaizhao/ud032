# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests
import pprint


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    '''
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    pretty_print(results)

    artist_id = results["artists"][1]["id"]
    print "\nARTIST:"
    pretty_print(results["artists"][1])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print "\nONE RELEASE:"
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]

    print "\nALL TITLES:"
    for t in release_titles:
        print t
    '''
    # How many bands named "First Aid Kit"
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    count = 0
    for artist in results['artists']:
        if artist['name'] == "First Aid Kit":
            count += 1
    print "There are", count, "bands named 'First Aid Kit'."

    # Begin-area name for Queen
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    queen = [artist for artist in results["artists"] if artist["name"] == "Queen"]
    print "Begin-area name for Queen is", queen[0]["begin-area"]["name"]

    # Spanish alias for Beatles
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    beatles = [artist for artist in results["artists"] if artist["name"] == "The Beatles"]
    print len(beatles)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint([alias['name'] for alias in beatles[0]['aliases']])

    # Nirvana disambiguation
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    nirvana = [artist for artist in results["artists"] if artist["name"] == "Nirvana"]
    print "Nirvana disambiguation is", nirvana[0]["disambiguation"]

    # When was One Direction was formed
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    onedirection = [artist for artist in results["artists"] if artist["name"] == "One Direction"]
    print "One Direction was formed in", onedirection[0]["life-span"]["begin"]


if __name__ == '__main__':
    main()
