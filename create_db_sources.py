import os
import gzip
import glob
import json
import random

random.seed(42)

# extracted from 
# https://www.nature.com/articles/s41587-018-0008-8#MOESM4
#
# https://static-content.springer.com/esm/art%3A10caevow9Voomu.1038%2Fs41587-018-0008-8/MediaObjects/41587_2018_8_MOESM7_ESM.xlsx
valid_species = [
    'eggerthella_lenta',
    'clostridium_symbiosum',
    'bacteroides_eggerthii',
    'lactobacillus_plantarum',
    'ruminococcus_lactaris',
    'enterococcus_avium',
    'parabacteroides_distasonis',
    'clostridium_leptum',
    'prevotella_sp',
    'coprococcus_sp',
    'anaerostipes_sp',
    'bacillus_coagulans',
    'lactobacillus_gasseri',
    'enterobacter_sp',
    'bacteroides_clarus',
    'parabacteroides_merdae',
    'enterococcus_durans',
    'lactococcus_lactis',
    'propionibacterium_sp',
    'anaerofustis_stercorihominis',
    'roseburia_inulinivorans',
    'clostridium_innocuum',
    'eubacterium_biforme',
    'enterococcus_faecalis',
    'holdemania_filiformis',
    'enterococcus_saccharolyticus',
    'roseburia_hominis',
    'clostridium_nexile',
    'ruminococcus_gnavus',
    'bacteroides_faecis',
    'clostridium_sp',
    'ruminococcus_bromii',
    'collinsella_intestinalis',
    'dorea_sp',
    'bacteroides_plebeius',
    'bacteroides_oleiciplenus',
    'bacteroides_sp',
    'parabacteroides_gordonii',
    'bifidobacterium_pseudolongum',
    'burkholderiales_bacterium',
    'clostridium_bolteae',
    'coprococcus_catus',
    'clostridium_asparagiforme',
    'streptococcus_lutetiensis',
    'bifidobacterium_stercoris',
    'acidaminococcus_sp',
    'parabacteroides_sp',
    'erysipelatoclostridium_ramosum',
    'clostridium_butyricum',
    'bifidobacterium_adolescentis',
    'odoribacter_sp',
    'tannerella_sp',
    'clostridium_clostridioforme',
    'clostridiales_bacterium',
    'bacteroides_stercoris',
    'solobacterium_moorei',
    'enterococcus_casseliflavus',
    'bacteroides_salyersiae',
    'ruminococcus_sp',
    'klebsiella_pneumoniae',
    'erysipelotrichaceae_bacterium',
    'coprobacillus_sp',
    'bacteroides_uniformis',
    'clostridium_perfringens',
    'lactobacillus_casei',
    'catenibacterium_sp',
    'dorea_formicigenerans',
    'clostridium_spiroforme',
    'lactobacillus_ruminis',
    'bacteroides_caccae',
    'roseburia_sp',
    'mitsuokella_multacida',
    'bacteroides_intestinalis',
    'prevotella_stercorea',
    'blautia_sp',
    'bacillus_licheniformis',
    'odoribacter_splanchnicus',
    'bifidobacterium_animalis',
    'bacteroides_fragilis',
    'bacteroides_cellulosilyticus',
    'fusobacterium_ulcerans',
    'citrobacter_sp',
    'bacillus_sonorensis',
    'faecalibacterium_prausnitzii',
    'bifidobacterium_pseudocatenulatum',
    'bacteroides_coprocola',
    'bacteroides_ovatus',
    'streptococcus_sp',
    'eubacterium_dolichum',
    'eubacterium_ventriosum',
    'staphylococcus_warneri',
    'bacteroides_coprophilus',
    'bacteroides_stercorirosoris',
    'eubacterium_hallii',
    'ruminococcus_torques',
    'ruminococcus_obeum',
    'clostridium_hathewayi',
    'enterobacter_cloacae',
    'alistipes_indistinctus',
    'bifidobacterium_bifidum',
    'dorea_longicatena',
    'coprococcus_eutactus',
    'fusobacterium_mortiferum',
    'enterococcus_asini',
    'firmicutes_bacterium',
    'bacteroides_xylanisolvens',
    'bacteroides_vulgatus',
    'clostridium_sordellii',
    'lachnospiraceae_bacterium',
    'lactobacillus_salivarius',
    'bifidobacterium_longum',
    'veillonella_atypica',
    'streptococcus_gordonii',
    'escherichia_coli',
    'veillonella_sp',
    'prevotella_copri',
    'paraprevotella_clara',
    'dielma_fastidiosa',
    'butyrateproducing_bacterium',
    'faecalibacterium_sp',
    'collinsella_tanakaei',
    'eubacterium_eligens',
    'faecalibacterium_cf',
    'butyricimonas_virosa',
    'streptococcus_parasanguinis',
    'veillonella_parvula',
    'bacillus_cereus',
    'megamonas_funiformis',
    'roseburia_intestinalis',
    'megamonas_rupellensis',
    'weissella_cibaria',
    'alistipes_sp',
    'bacteroides_thetaiotaomicron',
    'coprococcus_comes',
    'eubacterium_rectale',
    'clostridium_citroniae',
    'weissella_confusa',
    'fusobacterium_varium',
    'streptococcus_anginosus',
    'lactobacillus_fermentum',
    'bacteroides_nordii',
    'streptococcus_salivarius',
    'eubacterium_sp',
    'lactococcus_garvieae',
    'streptococcus_mutans',
    'streptococcus_equinus',
    'streptococcus_pasteurianus',
    'prevotella_disiens',
    'streptococcus_vestibularis',
    'lactobacillus_amylovorus',
    'paenibacillus_polymyxa',
    'bacteroides_dorei',
    'subdoligranulum_sp'
]

with open('mapping.json', 'r') as file:
     mapping = json.load(file)

def generate_dbfiles(accessionid, taxid, outname):
    write_next = False

    for k,v in taxid.items():
        print(k)
        # only do anything if there are any taxids to work with and if we've got both prot and nucl data for this species
        if len(v) > 0 and os.path.exists("prot/prot_"+k) and os.path.exists("nucl/nucl_"+k):
            with open("prot/prot_"+k, "r") as f:
                with open(outname+"_prot.fa", "a") as wf:
                    r = f.readline()
                    while r:
                        if ">" in r:
                            if r.split("_")[1].strip() in taxid[k]:
                                write_next = True
                                wf.write(r)
                            else:
                                write_next = False
                        elif write_next:
                            wf.write(r)

                        r = f.readline()

            with open("nucl/nucl_"+k, "r") as f:
                with open(outname+"_nucl.fa", "a") as wf:
                    r = f.readline()
                    while r:
                        if ">" in r:  
                            if r.split(" ")[0].split(".")[0][1:] in accessionid[k]:
                                write_next = True
                                wf.write(r)
                            else:
                                write_next = False
                        elif write_next:
                            wf.write(r)

                        r = f.readline()

#
# FULL REFSEQ
#
# get all taxids so that we can filter out everything from the protein data
taxid = {species:list(taxids.keys()) for species,taxids in mapping.items()}
# get all accession numbers so that we can filter out everything nucleotide data
accessionid = {species:sum(list(taxids.values()), []) for species,taxids in mapping.items()}
 
generate_dbfiles(accessionid, taxid, "db_files/full_refseq")
    
#
# EACH SPECIES ONLY USES THE FIRST TAXID THAT REPRESENTS IT
#
taxid = {species:[list(taxids.keys())[0]] for species,taxids in mapping.items()}
{species:taxids[list(taxids.keys())[0]] for species,taxids in mapping.items()} 

generate_dbfiles(accessionid, taxid, "db_files/only_first")

#
# EACH SPECIES USES A RANDOM TAXID TO REPRESENT IT #1
#
taxid = {species:[list(taxids.keys())[random.randrange(len(taxids.keys()))]] for species,taxids in mapping.items()}
accessionid = {species:taxids[list(taxids.keys())[list(taxids.keys()).index(taxid[species][0])]] for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/each_random_1")
   
#
# EACH SPECIES USES A RANDOM TAXID TO REPRESENT IT #2
#
taxid = {species:[list(taxids.keys())[random.randrange(len(taxids.keys()))]] for species,taxids in mapping.items()}
accessionid = {species:taxids[list(taxids.keys())[list(taxids.keys()).index(taxid[species][0])]] for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/each_random_2")
   
#
# EACH SPECIES USES A RANDOM TAXID TO REPRESENT IT #3
#
taxid = {species:[list(taxids.keys())[random.randrange(len(taxids.keys()))]] for species,taxids in mapping.items()}
accessionid = {species:taxids[list(taxids.keys())[list(taxids.keys()).index(taxid[species][0])]] for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/each_random_3")
   
#
# WE USE ONLY SPECIES THAT HAVE BEEN EXTRACTED FROM THE GUT MICROBIOTA ARTICLE
#
taxid = {species:list(taxids.keys()) for species,taxids in mapping.items() if species.lower() in valid_species}
accessionid = {species:sum(list(taxids.values()), []) for species,taxids in mapping.items() if species.lower() in valid_species}
 
generate_dbfiles(accessionid, taxid, "db_files/only_gut_nature")
   
#
# USE A RANDOM SET OF 30% OF ALL TAXID #1
#
incl = 0.3

taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_30_1")
   
#
# USE A RANDOM SET OF 30% OF ALL TAXID #2
#import os
taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_30_2")
   
#
# USE A RANDOM SET OF 30% OF ALL TAXID #3
#
taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_30_3")
   
#
# USE A RANDOM SET OF 10% OF ALL TAXID #1
#
incl = 0.1

taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_10_1")
   
#
# USE A RANDOM SET OF 10% OF ALL TAXID #2
#
taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_10_2")
   
#
# USE A RANDOM SET OF 10% OF ALL TAXID #3
#
taxid = {species:[x for x in list(taxids.keys()) if random.random() < incl] for species,taxids in mapping.items()}
accessionid = {species:sum([x for z,x in taxids.items() if z in taxid[species]], []) for species,taxids in mapping.items()} 
 
generate_dbfiles(accessionid, taxid, "db_files/random_10_3")
   