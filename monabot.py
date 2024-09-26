import pywikibot
import inspect
import json

def create_item(site, label_dict, descr_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary="Setting labels")
    new_item.editDescriptions(descr_dict, summary="Setting descriptions.")
    return new_item.getID()

with open("journee_wikimedia.json", "r") as file_contents:

    artworks = json.load(file_contents)

    #site = pywikibot.Site("test", "wikidata")
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    for artwork in artworks:

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
            if artwork["category"]:
                descr_dict["en"] = artwork["category"] + " by " + artwork["artist_name"]
            else:
                descr_dict["en"] = "Public art by " + artwork["artist_name"]

        artwork_qid = "Q130363504"
        if artwork["artwork_id"] != 1605:
            artwork_qid = create_item(site, label_dict, descr_dict)
            print(label_dict)
            print(descr_dict)
            print("QID: " + artwork_qid)
            print(" ")

            item = pywikibot.ItemPage(repo, artwork_qid)
            coordinateclaim = pywikibot.Claim(repo, u'P625')
            coordinateclaim.setTarget(pywikibot.Coordinate(lat=artwork["latitude"], lon=artwork["longitude"], precision=0.000001, site=site))
            item.addClaim(coordinateclaim, summary=u'Adding coordinate claim')

#        item = pywikibot.ItemPage(repo, artist_id)
#        hasGenre = "P136" in item.claims
#        if hasGenre:
#            print(artist_id + " already has claim for P136")
#            hasPublicArtGenre = pywikibot.ItemPage(repo, "Q557141") in [
#                claim.target for claim in item.claims["P136"]
#            ]
#            if hasPublicArtGenre:
#                print(artist_id + " already has Q557141 as target of P136 claim")
#
#        if hasGenre and hasPublicArtGenre:
#            print("Skipping...\n")
#        else:
#            print("Adding P136 claim to " + artist_id)
#            claim = pywikibot.Claim(
#                repo, "P136"
#            )  # Adding artistic genre of oeuvre (P136)
#            target = pywikibot.ItemPage(
#                repo, "Q557141"
#            )  # Connecting P136 with 'Public art' (Q557141)
#            claim.setTarget(target)
#            item.addClaim(
#                claim,
#                summary="Bot: Adding claim Public Art as artist's genre to "
#                + artist_id
#                + ".",
#            )
#
#            url = pywikibot.Claim(repo, "P854")  # P854, reference URL
#            url.setTarget("https://picasso.iro.umontreal.ca/~mona/api/v3/artworks")
#            claim.addSource(
#                url,
#                summary="Bot: Adding sources to artistic genre of oeuvre (P136).",
#            )
#
#            counter += 1
#            print("")
