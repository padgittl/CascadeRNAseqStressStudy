import sys, re, os
from Bio import SeqIO
from Bio.Seq import Seq

###############
# SUBROUTINES #
###############

def readAndFilterFasta(fastaFile):
    geneDict = {}
    fullPath = fastaFile.strip() 
    fileName = os.path.basename(fullPath)
    filePrefix,fileExt = os.path.splitext(fileName) 
    # TCONS_00000193 gene=000000F.g1
    # loop through all transcripts and append to dict of lists keyed by geneID
    for record in SeqIO.parse(fastaFile,"fasta"):
        #print record.id,record.name,record.description
        getGeneID = re.search('gene=(.+)',record.description)
        geneID = getGeneID.group(1)
        #print geneID
        if geneID not in geneDict:
            geneDict[geneID] = []
        geneDict[geneID].append((record.id,len(record.seq)))
    
    # sort for longest transcript length per gene
    for geneID in geneDict:
        geneDict[geneID].sort(key=lambda x:x[1], reverse=True)

    # keep longest transcript only 
    longestTranscripts = {}
    for geneID in geneDict:
        recordID,recordLen = geneDict[geneID][0]
        #print geneID,recordID,recordLen
        if recordID not in longestTranscripts:
            longestTranscripts[recordID] = geneID
            
    # loop through fasta again to keep only the longest transcript per gene
    filteredRecordDict = {}
    filteredRecordList = []
    for record in SeqIO.parse(fastaFile,"fasta"):
        if record.id in longestTranscripts:
            #print record.id
            if record.id not in filteredRecordDict:
                filteredRecordDict[record.id] = 1
                filteredRecordList.append(record)
    SeqIO.write(filteredRecordList,"longestTranscriptPerGene.fasta", "fasta")


########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <fasta file>\n"
if len(sys.argv) != 2:
    print usage
    sys.exit()

fastaFile = sys.argv[1]

readAndFilterFasta(fastaFile)

