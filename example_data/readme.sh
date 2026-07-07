# gut
cd gut
for i in `ls *.genus.txt`;
do
	cat $i | awk -F',' '$4!="" {print $2,$3}' > ${i%txt}.ID
done

for i in `ls *.genus.ID`;
do
	name=$(basename $i _pAMPs.genus.ID);
	for samp in `ls ../../../5_Binary/$name/*_psort_binary.csv`;
	do
		ID=$(basename $samp _psort_binary.csv);
		cat $i | awk -v ID="${ID}" '$1==ID {print $2}' > temp/${ID}.txt
		## HZ: cat HADZA_pAMPs.genus.ID | awk -v ID="H.${ID}" '$1==ID {print $2}' > temp/${ID}.txt
		seqkit grep -f temp/${ID}.txt ../../../5_Binary/$name/${ID}_binary.fasta >> ${name}_binary.genus.fa
	done
done
cat *.fa | seqkit rmdup -s > ../gut_clean.genus.fa
/home/Metagenome/LiuQ/Tools/cd-hit/cd-hit -i gut_clean.genus.fa -c 0.8 -o gut_clean.genus.cdhit.fa

# oral
cd oral
mkdir temp
cat PRJEB36291_pAMPs.genus.txt | sed '1d' | awk -F',' '$4!="" {print $2,$3}' > PRJEB36291_pAMPs.genus.ID
cat PRJEB36291_pAMPs.genus.ID | cut -d' ' -f 1 | sort | uniq | while read id;
do
	cat PRJEB36291_pAMPs.genus.ID | awk -v ID="${id}" '$1==ID {print $2}' > temp/${id}.txt
	seqkit grep -f temp/${id}.txt ../../../5_Binary/PRJEB36291/${id}_binary.fasta >> oral_binary.genus.fa
done
cp oral_binary.genus.fa ../
cat oral_binary.genus.fa | seqkit rmdup -s > oral_clean.genus.fa
/home/Metagenome/LiuQ/Tools/cd-hit/cd-hit -i oral_clean.genus.fa -c 0.8 -o oral_clean.genus.cdhit.fa
cat gut_clean.genus.fa | seqkit replace -p .+ -r "pAMP{nr}" > gut.genus.fa

# vagina
cd vagina
mkdir temp
cat VMRC_pAMPs.genus.txt | sed '1d' | awk -F',' '$4!="" {print $2,$3}' > VMRC_pAMPs.genus.ID
cat VMRC_pAMPs.genus.ID | cut -d' ' -f 1 | sort | uniq | while read id;
do
	cat VMRC_pAMPs.genus.ID | awk -v ID="${id}" '$1==ID {print $2}' > temp/${id}.txt
	seqkit grep -f temp/${id}.txt ../../../5_Binary/VMRC/${id}_binary.fasta >> vagina_binary.genus.fa
done
cat vagina_binary.genus.fa | seqkit rmdup -s > ../vagina_clean.genus.fa
/home/Metagenome/LiuQ/Tools/cd-hit/cd-hit -i vagina_clean.genus.fa -c 0.8 -o vagina_clean.genus.cdhit.fa

# skin
cd skin
mkdir temp
for i in `ls *.genus.txt`;
do
	cat $i | sed '1d' | awk -F',' '$4!="" {print $2,$3}' > ${i%txt}ID;
	name=$(basename $i _pAMPs.genus.txt);
	cat ${i%txt}ID | cut -d' ' -f 1 | sort | uniq | while read id;
	do
		cat ${i%txt}ID | awk -v ID="${id}" '$1==ID {print $2}' > temp/${id}.txt;
		seqkit grep -f temp/${id}.txt ../../../5_Binary/${name}/${id}_binary.fasta >> ${name}_binary.genus.fa
	done
done
cat *.fa | seqkit rmdup -s > ../skin_clean.genus.fa
/home/Metagenome/LiuQ/Tools/cd-hit/cd-hit -i skin_clean.genus.fa -c 0.8 -o skin_clean.genus.cdhit.fa

# healthy_CRC
cd healthy
mkdir temp
cat healthy_pAMPs.genus.txt | grep -v 'E.SRR' | grep -v 'SRR59' | sed '1d' | awk -F',' '$4!="" {print $2,$3}' > healthyCRC_pAMPs.genus.ID
cat healthyCRC_pAMPs.genus.ID | cut -d' ' -f 1 | sort | uniq | while read id;
do
	cat healthyCRC_pAMPs.genus.ID | awk -v ID="${id}" '$1==ID {print $2}' > temp/${id}.txt;
	seqkit grep -f temp/${id}.txt ../../../5_Binary/healthy/${id}_binary.fasta >> healthyCRC_binary.genus.fa;
done

# crc
cd crc
mkdir temp
for i in `ls *.genus.txt`;
do
	cat $i | sed '1d' | awk -F',' '$4!="" {print $2,$3}' > ${i%txt}ID;
	name=$(basename $i _pAMPs.genus.txt);
	cat ${i%txt}ID | cut -d' ' -f 1 | sort | uniq | while read id;
	do
		cat ${i%txt}ID | awk -v ID="${id}" '$1==ID {print $2}' > temp/${id}.txt;
		seqkit grep -f temp/${id}.txt ../../../5_Binary/${name}/${id}_binary.fasta >> ${name}_binary.genus.fa;
	done
done
cat *.fa | seqkit rmdup -s | seqkit stat

# 6_Multi
for i in `ls ../7_Analysis/filterG/healthy/temp/*.txt`;
do
	id=$(basename $i .txt);
	grep -w -f $i ./healthy/${id}_binary_multi.csv | sed "s/^/$id,/g" >> ./healthyCRC_multi.genus.csv;
done
sort -t ',' -k 3,3 -u healthyCRC_multi.genus.csv > healthyCRC_multi.genus.rmdup.csv
sed -i '1i sample,ID,sequence,antibacterial,antifungal,anticancer,antiviral' healthyCRC_multi.genus.rmdup.csv

