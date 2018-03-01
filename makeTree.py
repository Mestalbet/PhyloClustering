from ete3 import Tree, ImgFace, PhyloTree, TextFace
import re
from bioservices import EUtils
import json
from xml.etree import ElementTree
from xml.dom.minidom import parseString

def findName(accession):
    s=EUtils()
    theID = None
    geneOrProtein = "gene"
    # Check gene database
    res = s.ESearch("gene", accession)
    if len(res["idlist"]) > 0:
        # Get the ID in the "gene" database
        theID = res["idlist"][0]
    # If that fails, check the protein database
    if theID == None:
        res = s.ESearch("protein", accession)
        if len(res["idlist"]) > 0:
            theID = res["idlist"][0]
            geneOrProtein = "protein"
    # Couldn't find in either database
    if not theID:
        print("ERROR: couldn't find link for %s"%accession)

    # Get link to the corresponding ID in the Taxonomy database
    link = s.ELink(db="taxonomy", dbfrom=geneOrProtein, id=theID, retmode="json")
    taxID = json.loads(link)["linksets"][0]["linksetdbs"][0]["links"][0]

    # Download taxonomy record
    tax = s.EFetch(db="taxonomy", id=taxID)
    #print(tax)
    tree = ElementTree.fromstring(tax)
    xmlP = parseString(tax)
    #print(xmlP.toprettyxml())
    taxonTag = tree.find("Taxon")
    sciName = taxonTag.find("ScientificName")
    return sciName.text
    
    
f="phylotree.nw"
nw=open(f,"r").read();
print nw

t = PhyloTree(nw)
r = t.write(format=9)
leaves = re.split('\(|\)|,|;',r)
for leaf in leaves:
    try:
        if leaf != "":
            imgName = re.split('\.',leaf)
            imgName = imgName[0] + ".png"
            idName = findName(leaf)
            f = ImgFace(imgName, height=50)
            species = TextFace(idName, ftype='Verdana', fsize=10, fgcolor='black', penwidth=0, fstyle='italic', tight_text=False, bold=False)
            (t&leaf).add_face(f, 1, 'aligned')
            (t&leaf).add_face(species, 1, 'branch-right')
    except Exception as e:
        print("Some unknown error occured: %s"%(str(e)))
        
t.show()
