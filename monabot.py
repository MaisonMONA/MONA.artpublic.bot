import pywikibot
import inspect
import json

with open("journee_wikimedia.json", "r") as file_contents:

    artworks = json.load(file_contents)

    #site = pywikibot.Site("test", "wikidata")
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    for artwork in artworks:

        if artwork["artwork_id"] != 1605:
            artwork_qid = artwork["wikidata_qid"]
            item = pywikibot.ItemPage(repo, artwork_qid)

            if artwork["artist_wikidata"]:
                claim = pywikibot.Claim(repo, "P170")   #P170, creator
                claim.setTarget(pywikibot.ItemPage(repo, artwork["artist_wikidata"]))
                item.addClaim(claim, summary="Bot: Adding claim detailing creator of work of art")

            if artwork["year"]:
                claim = pywikibot.Claim(repo, "P571")   #P571, inception
                claim.setTarget(pywikibot.WbTime(year=artwork["year"]))
                item.addClaim(claim, summary="Bot: Adding year of creation of work of art")


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
