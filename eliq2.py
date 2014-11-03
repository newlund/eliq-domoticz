#!/usr/bin/env python

import json
import urllib2
import datetime

accesstoken = "<accesstoken>"
idx = "<idx>"
url = "http://<server>:8080"
last = ""

while True:
    try:
        today = str(datetime.date.today())
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        j_obj = json.load(urllib2.urlopen("https://my.eliq.se/api/datanow?accesstoken=" + accesstoken))
        j_obj_day = json.load(urllib2.urlopen("https://my.eliq.se/api/data?accesstoken=" + accesstoken + "&startdate=" + today + "&enddate=" + tomorrow + "&intervaltype=6min"))

    except urllib2.HTTPError:
        print "***HTTPError***"
        continue
    except urllib2.URLError:
        print "***URLError***"
        continue
    except ValueError:
        print "***ValueError***"
        continue
    except TypeError:
        print "***TypeError***"
        continue

    if not last == j_obj['createddate'] + " " + str(j_obj['power']):
        parent = j_obj_day["data"]
        energy_day = 0
        for item in parent:
            energy_day += float(item["energy"])
        try:
            r_obj = json.load(urllib2.urlopen(url + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + str(j_obj['power']) + ";" + str(energy_day)))
        except urllib2.HTTPError:
            print "***HTTPError***"
            continue
        except urllib2.URLError:
            print "***URLError***"
            continue
        except ValueError:
            print "***ValueError***"
            continue
        except TypeError:
            print "***TypeError***"
            continue

        print j_obj['createddate'] + " " + str(j_obj['power']) + " " + str(energy_day)
        print r_obj['status']
        last = j_obj['createddate'] + " " + str(j_obj['power'])