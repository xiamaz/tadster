# TADSTER

Convert Gene names into Gene coordinates and TAD boundaries.

## Data preparation

Download GENCODE genes to `./data/gencode` with the following commands:

```
$ wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19/gencode.v19.annotation.gff3.gz
$ gunzip gencode.v19.annotation.gff3.gz
$ mv gencode.v19.annotation.gff3 data/
```

## References

TAD coordinates are obtained from [TADKB](http://dna.cs.miami.edu/TADKB/).

  Liu T, Porter J, Zhao C, Zhu H, Wang N, Sun Z, Mo Y-Y, Wang Z. TADKB: Family classification and a knowledge base of topologically associating domains. BMC Genomics 2019, 20(1):217.

Gene List obtained from [Gencode](https://www.gencodegenes.org/human/release_19.html).
