#!/usr/bin/env python3
"""Golden-fixture generator for dev.cajeta.docs.

Oracles: scikit-learn 1.9.0 for TF-IDF (spec §9.4/§13.10 — EVERY
variant switch exercised, because matching only on defaults hides the
formula differences) and HuggingFace `tokenizers` WordPiece over the
committed bert-base-uncased vocabulary for §10.8/§13.9's
token-for-token subword pin.

Run:  /home/julian/code/ml/venv-sklearn-ref/bin/python gen_docs.py
"""

import numpy as np
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

assert sklearn.__version__ == "1.9.0", sklearn.__version__

OUT = __file__.rsplit("/", 1)[0]

CORPUS = [
    "the reactor held steady under load",
    "the backup reactor tripped under peak load",
    "steady state was recovered after the trip",
    "peak load forecasting uses the reactor telemetry",
    "telemetry archives grow under steady collection",
    "forecasting the peak requires telemetry archives",
]


def save(name, arr):
    a = np.ascontiguousarray(np.asarray(arr, dtype=np.float64))
    np.save(f"{OUT}/{name}.npy", a)
    print(f"  {name}.npy {a.shape}")


def gen_tfidf():
    with open(f"{OUT}/docs_corpus.txt", "w") as f:
        f.write("\n".join(CORPUS) + "\n")

    cv = CountVectorizer()
    counts = cv.fit_transform(CORPUS)
    vocab = sorted(cv.vocabulary_, key=cv.vocabulary_.get)
    with open(f"{OUT}/docs_vocab.txt", "w") as f:
        f.write("\n".join(vocab) + "\n")
    save("docs_counts", counts.toarray())

    configs = {
        "default": dict(),                            # l2 + smooth idf
        "nosmooth": dict(smooth_idf=False),
        "sublinear": dict(sublinear_tf=True),
        "nonorm": dict(norm=None),
        "noidf": dict(use_idf=False),
        "l1": dict(norm="l1"),
    }
    for name, kw in configs.items():
        tv = TfidfVectorizer(**kw)
        m = tv.fit_transform(CORPUS)
        save(f"docs_tfidf_{name}", m.toarray())
    # Unseen transform: vocabulary must NOT grow (§9.2).
    tv = TfidfVectorizer()
    tv.fit(CORPUS)
    unseen = ["the reactor telemetry surprised nobody quantumly"]
    save("docs_tfidf_unseen", tv.transform(unseen).toarray())


def gen_wordpiece():
    from tokenizers import BertWordPieceTokenizer
    tok = BertWordPieceTokenizer(f"{OUT}/bert-base-uncased-vocab.txt",
                                 lowercase=True)
    text = ("The measurement uncannily outperformed expectations, "
            "tokenizing embeddings efficiently in 2026! "
            "Hyperparameters stabilized; overfitting vanished.")
    enc = tok.encode(text)
    # Drop [CLS]/[SEP] specials: the library-level contract is the
    # wordpiece split itself.
    toks = [t for t in enc.tokens if t not in ("[CLS]", "[SEP]")]
    with open(f"{OUT}/docs_wordpiece_input.txt", "w") as f:
        f.write(text + "\n")
    with open(f"{OUT}/docs_wordpiece_tokens.txt", "w") as f:
        f.write("\n".join(toks) + "\n")
    print(f"  wordpiece: {len(toks)} tokens")


def main():
    print(f"sklearn {sklearn.__version__} fixtures -> {OUT}")
    gen_tfidf()
    gen_wordpiece()


if __name__ == "__main__":
    main()
