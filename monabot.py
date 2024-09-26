import pywikibot
import inspect
import json

def create_item(site, label_dict, descr_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary="Bot: Setting labels")
    new_item.editDescriptions(descr_dict, summary="Bot: Setting descriptions.")
    return new_item.getID()

with open("journee_wikimedia_2.json", "r") as file_contents:

    artworks = json.load(file_contents)

    #site = pywikibot.Site("test", "wikidata")
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    for artwork in artworks:

        # LABEL AND DESCRIPTIONS
        label_dict = {}
        descr_dict = {}
        if artwork["title_fr"]:
            label_dict["fr"] = artwork["title_fr"]
            if artwork["category"]:
                descr_dict["fr"] = artwork["category"] + " par " + artwork["artist_name"]
            else:
                descr_dict["fr"] = "Oeuvre d'art public par " + artwork["artist_name"]
        if artwork["title_en"]:
            label_dict["en"] = artwork["title_en"]
            #if artwork["category"]:
            #    descr_dict["en"] = artwork["category"] + " by " + artwork["artist_name"]
            #else:
            #    descr_dict["en"] = "Public artwork by " + artwork["artist_name"]
            descr_dict["en"] = "Public artwork by " + artwork["artist_name"]

        if artwork["artwork_id"] != 1605:   # filter out the artwork David created
            if artwork["wikidata_qid"]:
                artwork_qid = artwork["wikidata_qid"]
            else:
                artwork_qid = create_item(site, label_dict, descr_dict) # NOTE: will not update labels or descriptions on artworks already in wikidata
            item = pywikibot.ItemPage(repo, artwork_qid)

            # LOCATION
            coordinateclaim = pywikibot.Claim(repo, u'P625')
            coordinateclaim.setTarget(pywikibot.Coordinate(lat=artwork["latitude"], lon=artwork["longitude"], precision=0.000001, site=site))
            url = pywikibot.Claim(repo, "P854") # P854, reference URL
            url.setTarget("https://picasso.iro.umontreal.ca/~mona/api/v3/artwork/" + artwork["artwork_id"])
            coordinateclaim.addSource(url, summary="Bot: Adding source for location of artwork")
            item.addClaim(coordinateclaim, summary=u'Bot: Adding coordinate claim')

            # "INSTANCE OF"
            #if artwork["category"] == "Murale":
            #    target = "Q219423"
            #elif artwork["category"] == "Sculpture":
            #    target = "Q860861"
            #else:
            #    target = "Q838948"
            target = "Q838948"
            claim = pywikibot.Claim(repo, "P31")   #P31, instance of
            claim.setTarget(pywikibot.ItemPage(repo, target)) #Murale, sculpture ou work of art
            item.addClaim(claim, summary="Bot: Adding claim describing what item is instance of")


            # ARTIST
            if artwork["artist_wikidata"]:
                claim = pywikibot.Claim(repo, "P170")   #P170, creator
                claim.setTarget(pywikibot.ItemPage(repo, artwork["artist_wikidata"]))
                url = pywikibot.Claim(repo, "P854") # P854, reference URL
                url.setTarget("https://picasso.iro.umontreal.ca/~mona/api/v3/artwork/" + artwork["artwork_id"])
                claim.addSource(url, summary="Bot: Adding source for creator of work of art")
                item.addClaim(claim, summary="Bot: Adding claim detailing creator of work of art")

            # YEAR
            if artwork["year"]:
                claim = pywikibot.Claim(repo, "P571")   #P571, inception
                claim.setTarget(pywikibot.WbTime(year=artwork["year"]))
                url = pywikibot.Claim(repo, "P854") # P854, reference URL
                url.setTarget("https://picasso.iro.umontreal.ca/~mona/api/v3/artwork/" + artwork["artwork_id"])
                claim.addSource(url, summary="Bot: Adding source for creation year")
                item.addClaim(claim, summary="Bot: Adding year of creation of work of art")
