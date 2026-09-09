from scripts.audit_observation_text_overlap import audit


def test_observation_abstract_has_no_exact_long_sentence_reuse():
    report = audit()
    for source in report["sources"].values():
        assert source["exact_long_sentence_count"] == 0


def test_observation_abstract_has_minimal_12_word_shingle_overlap():
    report = audit()
    counts = {
        name: source["shared_12_word_shingle_count"]
        for name, source in report["sources"].items()
    }
    assert counts["v3_layer1"] <= 2
    assert counts["rec_h1_h5"] == 0
    assert counts["tnoa_mee"] == 0
