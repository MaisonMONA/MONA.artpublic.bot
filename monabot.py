import pywikibot
import inspect
import json

with open('wikidata_ids.json', 'r') as file_contents:

    artist_ids = json.load(file_contents)

    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    for artist_id in artist_ids:
        item = pywikibot.ItemPage(repo, artist_id)
        
        print("Adding P136 claim to "+artist_id)
        if 'P136' not in item.claims:
            claim = pywikibot.Claim(repo, 'P136') #Adding artistic genre of oeuvre (P136)
            target = pywikibot.ItemPage(repo, 'Q557141') #Connecting P136 with 'Public art' (Q557141)
            claim.setTarget(target)
            item.addClaim(claim, summary="Bot: Adding claim Public Art as artist's genre to "+artist_id)

            source = ???
            claim.addSource(source, summary='Bot: Adding sources to artistic genre of oeuvre (P136).')
        else:
            print(" "+artist_id+" already has claim for P136\n")
