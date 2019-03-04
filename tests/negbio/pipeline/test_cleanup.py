import bioc

from negbio.pipeline.cleanup import clean_sentences
from tests.negbio.utils import text_to_bioc


def test_clean_sentences():
    doc = text_to_bioc(['No pneumothorax.', 'No pneumothorax.'], type='d/p/s')
    p = doc.passages[0]
    for i in range(10, 0, -1):
        ann = bioc.BioCAnnotation()
        ann.add_location(bioc.BioCLocation(i, 1))
        p.add_annotation(ann)

    assert len(doc.passages[0].sentences) == 2
    doc = clean_sentences(doc)
    assert len(doc.passages[0].sentences) == 0
    assert len(doc.passages[0].annotations) == 10
    for i in range(10):
        assert doc.passages[0].annotations[i].total_span.offset == 10 - i

    doc = clean_sentences(doc, sort_anns=True)
    for i in range(10):
        assert doc.passages[0].annotations[i].total_span.offset == i + 1
