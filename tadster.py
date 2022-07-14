from pathlib import Path
import pandas as pd
import gffutils


class Configuration:
    gencode_file = Path("./data/gencode.v41lift37.annotation.gtf.gz")
    gencode_db = Path("./data/gencode.db")
    tad_files = Path("./data/TADs")


if __name__ == "__main__":
    Configuration.gencode_db.unlink()
    if not Configuration.gencode_db.exists():
        db = gffutils.create_db(str(Configuration.gencode_file), str(Configuration.gencode_db), keep_order=True, disable_infer_genes=True, disable_infer_transcripts=True)
    else:
        db = gffutils.FeatureDB(str(Configuration.gencode_db))

    print(db.schema())

    data = pd.read_csv("./examples/panelapp_osteogenesis_imperfecta.tsv", sep="\t")
    for n in data['EnsemblId(GRch37)']:
        db[n]
