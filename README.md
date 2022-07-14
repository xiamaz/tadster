# TADSTER

Convert Gene names into Gene coordinates and TAD boundaries.

## Data preparation

Download GENCODE genes to `./data/gencode` with the following commands:

```
$ cd data
$ wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_41/GRCh37_mapping/gencode.v41lift37.annotation.gtf.gz
```

## References

TAD coordinates are obtained from [TADKB](http://dna.cs.miami.edu/TADKB/).

  Liu T, Porter J, Zhao C, Zhu H, Wang N, Sun Z, Mo Y-Y, Wang Z. TADKB: Family classification and a knowledge base of topologically associating domains. BMC Genomics 2019, 20(1):217.

Gene List obtained from [Gencode](https://www.gencodegenes.org/human/release_41lift37.html).
