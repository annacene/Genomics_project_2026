import subprocess
import os

# PARTE 1:
# --> crea una cartella per ogni caso e collega:
##   - mamma, papà, figlio, fw e rev
##   - i file che ci sono sulla cartella generica per tutti
##   - samples.txt dalla cartella sopra

def setup_links(trio_id):
    run_command(f"ln -s /home/BCG2026_exam/BCG2026_Cenedese_A/{trio_id}/* . ") #e importo i file fw e rev mamma papà figlio
    run_command(" ln -s /home/BCG2026_exam/chr20* .")
    print(f"Configurazione link per {trio_id}...")
    run_command("ls")

# PARTE 2: Facciamo il multiqc e bowtie
def run_variant_calling(samples, roles):
    # Qui metti la tua pipeline vera e propria
    # Ricorda di usare il file BED per le target regions!
    print("Running variant calling...")
    for i in range (0,len(samples)):
        cmd = f"bowtie2 -x chr20 -1 {samples[i]}.targets_R1.fq.gz -2 {samples[i]}.targets_R2.fq.gz --rg-id {samples[i]} --rg SM:{roles[i]} | samtools view -Sb - | samtools sort -o {roles[i]}.bam"
        run_command(cmd)

def run_qc(roles):
    print("Avvio MultiQC e Quality Control...")
    run_command("fastqc *.bam")
    for role in roles:
        cmd1 = f"qualimap bamqc -bam {role}.bam --feature-file chr20_ILMN_Exome_2.0_Plus_Panel.hg38_padded.bed --outdir {role}_stats"
        run_command(cmd1)
        cmd2 = f"bedtools genomecov -ibam {role}.bam -bg -trackline -trackopts 'name={role}' -max 100 > {role}Cov.bg"
        run_command(cmd2)
    run_command("multiqc .")

# PARTE 3: variant calling -> ottengo il vcf finale
def run_vcf(roles):
    samples_str = ",".join(roles)We
    print("Avvio MultiVCF...")
    run_command("nohup freebayes -f chr20.fa -m 20 -C 5 -Q 10 -q 10 --min-coverage 10 child.bam father.bam mother.bam > output.vcf ")
    run_command("bgzip output.vcf ")
    run_command("bcftools index output.vcf.gz ")
    run_command(f"bcftools view -R chr20_ILMN_Exome_2.0_Plus_Panel.hg38_padded.bed output.vcf.gz | bcftools view -s {samples_str} | bcftools view -i 'GT[0]=\"RA\" && GT[1]=\"RR\" && GT[2]=\"RR\"' | bcftools filter -i 'QUAL>20' -Ov -o output.cand.vcf ")

#questo fa partire il comando che voglio io su bash

def run_command(cmd):
    try:
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {cmd}\nDettaglio: {e}")
        exit(1)


# --- MAIN LOOP ---
if __name__ == "__main__":
    setup_links("trio_3") #qui è da cambiare il numero per ogni trio però poco male
    samples = ["HG00421","HG00422","HG00423"] ##CAMBIARE QUA
    roles = ["child", "father", "mother"]
    run_variant_calling(samples, roles)
    run_qc(roles)
    run_vcf(roles)