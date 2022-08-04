#!/usr/bin/env python3
from typing import Optional, Dict
from pathlib import Path
import pandas as pd
import gffutils

import typer


class Configuration:
    gencode_file = Path("./data/gencode.v41lift37.annotation.gtf.gz")
    gencode_db = Path("./data/gencode.db")
    tad_files = Path("./data/TADs")

    output_csv = Path("./tad_boundaries.csv")

    human_tad_cell_types = {'GM12878', 'HMEC', 'NHEK', 'IMR90', 'KBM7', 'K562', 'HUVEC'}


def main(input_tsv: Path, output_annotated: Path):
    if not Configuration.gencode_db.exists():
        db = gffutils.create_db(str(Configuration.gencode_file), str(Configuration.gencode_db), keep_order=True, disable_infer_genes=True, disable_infer_transcripts=True)
    else:
        db = gffutils.FeatureDB(str(Configuration.gencode_db))

    data: pd.DataFrame = pd.read_csv(input_tsv, sep="\t") # type: ignore

    hgnc_mapping: Dict[str, Optional[gffutils.Feature]] = {k: None for k in data['HGNC']}
    for f in db.features_of_type("gene"):
        if 'hgnc_id' in f.attributes and f['hgnc_id'][0] in hgnc_mapping:
            hgnc_mapping[f['hgnc_id'][0]] = f

    # now we have hgnc mappings
    print("Obtained following hgnc mappings")
    for f in hgnc_mapping.values():
        if f is not None:
            print(f.chrom, f.start, f.end)

    # obtain TAD boundaries
    keys = ('variant', 'cellline', 'caller', 'resolution', 'path')
    hic_paths = [
        {**p, **{'data': pd.read_csv(p['path'], sep=' ', header=None, names=['chrom', 'start', 'end'])}} for p in # type: ignore
        [
            dict(zip(keys, [*p.stem.split("_"), p]))
            for p in Configuration.tad_files.iterdir()
        ]
        # if p['cellline'] in Configuration.human_tad_cell_types
        if p['cellline'] in {'IMR90'} # only use fibrobl
    ]

    result_data = []
    for f in hgnc_mapping.values():
        if f is not None:
            chrom = f.chrom
            start = f.start
            end = f.end

            intersectings = []
            for hic in hic_paths:
                coords = hic['data']
                intersecting = coords.loc[
                    (coords['chrom'] == chrom)
                    & (((coords['start'] < start) & (coords['end'] > start))
                       | ((coords['start'] < end) & (coords['end'] > end)))]
                intersectings.append(intersecting)
            ins_hics = pd.concat(intersectings)
            # TODO: limitation intersection with multiple diff hic will be badly
            # approximated
            hic_median = pd.Series(ins_hics[['start', 'end']].median())
            hic_start = hic_median['start']
            hic_end = hic_median['end']
            print(f['gene_name'], chrom, start, end, 'hic', hic_start, hic_end)
            result_data.append({
                'gene_name': f['gene_name'][0],
                'hgnc': f['hgnc_id'][0],
                'gene_id': f['gene_id'][0],
                'chrom': chrom,
                'start': start,
                'end': end,
                'tad_start': hic_start,
                'tad_end': end,
            })
    result_df = pd.DataFrame.from_records(result_data)
    result_df.to_csv(output_annotated)

if __name__ == "__main__":
    typer.run(main)
