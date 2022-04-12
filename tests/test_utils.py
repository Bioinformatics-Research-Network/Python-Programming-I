from utils import *
import pandas as pd
import numpy as np
import pytest

#### ID CONVERTER


def test_id_converter_1():
    assert id_converter(ids=["ENSG00000147889", 8243]) == {
        "ENSG00000147889": ["CDKN2A"],
        8243: ["SMC1A"],
    }


def test_id_converter_2():
    """Error on invalid gene ids"""
    with pytest.raises(Exception):
        id_converter(ids=["ABCD", 0])


#### FIND SNVS


def test_find_snvs_1():
    """Positive case: works as expected"""
    res = find_snvs(cancer="ATGCGCTA", normal="ATGCTCTT")
    assert res.reset_index(drop=True).equals(
        pd.DataFrame({"position": [4, 7], "cancer": ["G", "A"], "normal": ["T", "T"]})
    )


def test_find_snvs_2():
    """Error on mismatched length"""
    with pytest.raises(Exception):
        find_snvs(cancer="ATGCGCTAAA", normal="ATGCTCTT")


def test_find_snvs_3():
    """Error on non-DNA bases"""
    with pytest.raises(Exception):
        find_snvs(cancer="ATGCUUUG", normal="ATGCTCTT")


def test_find_snvs_4():
    """Error on empty"""
    with pytest.raises(Exception):
        find_snvs(cancer="", normal="")


def test_find_snvs_5():
    """Error on non-character"""
    with pytest.raises(Exception):
        find_snvs(cancer=1, normal=0)


#### TRANSCRIBE


def test_transcribe_1():
    """Positive case: works as expected"""
    tx = transcribe(sequence="AAAGTCGAGGTGTAGATCAAACCC")
    assert tx == "UUUCAGCUCCACAUCUAGUUUGGG"


def test_transcribe_2():
    """Error on non-DNA bases"""
    with pytest.raises(Exception):
        transcribe(sequence="ATGCUU")


def test_transcribe_3():
    """Error on empty"""
    with pytest.raises(Exception):
        transcribe(sequence="")


def test_transcribe_4():
    """Error on non-character"""
    with pytest.raises(Exception):
        transcribe(sequence=1)


#### TRANSLATE


def test_translate_1():
    """Positive case: works as expected"""
    prot = translate(sequence="UUUCAGCUCCACAUCUAGUUUGGG")
    assert prot == "FQLHI*FG"


def test_translate_2():
    """Error on non-RNA bases"""
    with pytest.raises(Exception):
        translate(sequence="ATGCUU")


def test_translate_3():
    """Error on seq len not divisible by 3"""
    with pytest.raises(Exception):
        translate(sequence="AUGCC")


def test_translate_4():
    """Error on empty"""
    with pytest.raises(Exception):
        translate(sequence="")


def test_translate_5():
    """Error on non-character"""
    with pytest.raises(Exception):
        translate(sequence=1)


#### PROTEIN VARIANT


def test_protein_variant_1():
    """Positive case: works as expected"""
    prot_var = protein_variant(
        cancer="AAAGTGGAGGTGTAGATCAAACCC", normal="AAAGTCGAGGTGTAGATGAAACCC"
    )
    assert prot_var.reset_index(drop=True).equals(
        pd.DataFrame(
            {"codon_number": [1, 5], "cancer": ["H", "*"], "normal": ["Q", "Y"]}
        )
    )


def test_protein_variant_2():
    """Error on mismatch length"""
    with pytest.raises(Exception):
        protein_variant(cancer="ATGCGCTAA", normal="ATGCTCTTACCC")


def test_protein_variant_3():
    """Error on non-RNA bases"""
    with pytest.raises(Exception):
        protein_variant(cancer="ATGCUUUGG", normal="ATGCTCTTG")


def test_protein_variant_4():
    """Error on seq len not divisible by 3"""
    with pytest.raises(Exception):
        protein_variant(cancer="ATGCCCCGGG", normal="ATGCTCTTGG")


def test_protein_variant_5():
    """Error on empty"""
    with pytest.raises(Exception):
        protein_variant(cancer="", normal="")


def test_protein_variant_6():
    """Error on non-character"""
    with pytest.raises(Exception):
        protein_variant(cancer=1, normal=0)


#### FIND NONSENSE


def test_find_nonsense_1():
    sequences = pd.DataFrame(
        {
            "gene_id": ["ENSG00000147889", 8243, 675],
            "cancer": [
                "AAAGTGGAGGTGTAGATCAAACCC",
                "CATATCCTGATCGGCCTGATCGGGAGG",
                "AGGGCTTTTACCCAGCATTGA",
            ],
            "normal": [
                "AAAGTCGAGGTGTAGATGAAACCC",
                "CATAGCCTGATCGGCCTGAGCGGGAGG",
                "AGGGCTTTTACCCAGGATTGA",
            ],
        }
    )
    res = find_nonsense(sequences)
    resreal = pd.DataFrame(
        {
            "gene_id": ["ENSG00000147889", 8243, 8243],
            "symbol": ["CDKN2A", "SMC1A", "SMC1A"],
            "codon_number": [5, 1, 6],
            "cancer": ["*", "*", "*"],
            "normal": ["Y", "S", "S"],
        }
    )
    assert res.reset_index(drop=True).equals(resreal)


def test_find_nonsense_2():
    """Error on mismatch length"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {
                "gene_id": ["ENSG00000147889"],
                "cancer": ["AAAGTGGAGGTGTAGATCAAA"],
                "normal": ["AAAGTCGAGGTGTAGATGAAACCC"],
            }
        )

        find_nonsense(sequences)


def test_find_nonsense_3():
    """Error on non-RNA bases"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {
                "gene_id": ["ENSG00000147889"],
                "cancer": ["AAAGTGGAGGTGTAUATCAAACCC"],
                "normal": ["AAAGTCGAGGTGTAGATGAAACCC"],
            }
        )

        find_nonsense(sequences)


def test_find_nonsense_4():
    """Error on seq len not divisible by 3"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {
                "gene_id": ["ENSG00000147889"],
                "cancer": ["AAAGTGGAGGTGTAGATCAAACCCT"],
                "normal": ["AAAGTCGAGGTGTAGATGAAACCCT"],
            }
        )

        find_nonsense(sequences)


def test_find_nonsense_5():
    """Error on empty"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {"gene_id": ["ENSG00000147889"], "cancer": [""], "normal": [""]}
        )

        find_nonsense(sequences)


def test_find_nonsense_6():
    """Error on non-character"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {"gene_id": ["ENSG00000147889"], "cancer": [1], "normal": [0]}
        )

        find_nonsense(sequences)


def test_find_nonsense_7():
    """Error on non-ID"""
    with pytest.raises(Exception):
        sequences = pd.DataFrame(
            {"gene_id": ["ABCD"], "cancer": [1], "normal": [0]}
        )

        find_nonsense(sequences)
