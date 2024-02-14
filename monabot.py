import pywikibot
import inspect
import json

with open('wikidata_ids.json', 'r') as file_contents:

    artist_ids = json.load(file_contents)

    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    limit = 10
    counter = 0
    
    for artist_id in artist_ids:
        if counter < limit:
            item = pywikibot.ItemPage(repo, artist_id)
            
            print("Adding P136 claim to "+artist_id)
            if 'P136' not in item.claims:
                claim = pywikibot.Claim(repo, 'P136') #Adding artistic genre of oeuvre (P136)
                target = pywikibot.ItemPage(repo, 'Q557141') #Connecting P136 with 'Public art' (Q557141)
                claim.setTarget(target)
                item.addClaim(claim, summary="Bot: Adding claim Public Art as artist's genre to "+artist_id+".")
    
                url = pywikibot.Claim(repo, 'P854') #P854, reference URL
                url.setTarget("https://picasso.iro.umontreal.ca/~mona/api/v3/artists")
                claim.addSource(url, summary='Bot: Adding sources to artistic genre of oeuvre (P136).')
            else:
                print(" "+artist_id+" already has claim for P136\n")
        else:
            print("Did not modify "+artist_id+"; hit modification limit.")
