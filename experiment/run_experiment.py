"""
Genuine small-scale baseline experiment for CTI-to-ATT&CK technique mapping.

Data:
  - Real MITRE ATT&CK Enterprise v18 technique catalog (222 top-level techniques),
    downloaded from the official MITRE CTI GitHub repository.
  - A manually authored set of 50 short CTI-style sentences, each hand-labeled
    by the author with the correct top-level ATT&CK technique ID.

Method (non-LLM baseline, representative of "Mapper Agent w/o LLM" ablation):
  TF-IDF vectorization of (technique name + description) as the retrieval corpus,
  cosine similarity ranking against each input sentence.

Metrics: Top-1 accuracy, Top-3 accuracy, Mean Reciprocal Rank (MRR).

This is a real, reproducible experiment run in this environment -- NOT fabricated
numbers. It is intentionally modest in scale (50 examples, TF-IDF baseline, no GPU/
API access available in this sandboxed environment) and should be reported as such:
a small illustrative baseline, not a full evaluation of an LLM-based system.
"""
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from eval_set import EVAL_SET

techniques = json.load(open("attack_techniques.json"))
top_level = [t for t in techniques if "." not in t["id"]]
print(f"Corpus size (top-level techniques): {len(top_level)}")

corpus_ids = [t["id"] for t in top_level]
corpus_docs = [f"{t['name']}. {t['description']}" for t in top_level]

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8, min_df=1, ngram_range=(1, 2))
corpus_matrix = vectorizer.fit_transform(corpus_docs)

queries = [s for s, _ in EVAL_SET]
gold = [g for _, g in EVAL_SET]

# sanity check all gold ids exist in corpus
missing = [g for g in gold if g not in corpus_ids]
assert not missing, f"Missing gold IDs in corpus: {missing}"

query_matrix = vectorizer.transform(queries)
sims = cosine_similarity(query_matrix, corpus_matrix)  # (n_queries, n_techniques)

top1_correct = 0
top3_correct = 0
reciprocal_ranks = []
rows = []

for i, (sentence, gold_id) in enumerate(EVAL_SET):
    order = np.argsort(-sims[i])  # descending similarity
    ranked_ids = [corpus_ids[j] for j in order]
    rank = ranked_ids.index(gold_id) + 1  # 1-indexed
    reciprocal_ranks.append(1.0 / rank)
    if rank == 1:
        top1_correct += 1
    if rank <= 3:
        top3_correct += 1
    rows.append((sentence[:60] + "...", gold_id, ranked_ids[0], rank))

n = len(EVAL_SET)
top1_acc = top1_correct / n
top3_acc = top3_correct / n
mrr = float(np.mean(reciprocal_ranks))

print(f"\nN = {n} hand-labeled CTI sentences, {len(corpus_ids)} candidate techniques")
print(f"Top-1 Accuracy: {top1_acc:.3f} ({top1_correct}/{n})")
print(f"Top-3 Accuracy: {top3_acc:.3f} ({top3_correct}/{n})")
print(f"MRR: {mrr:.3f}")

print("\nSample predictions (sentence | gold | predicted | rank of gold):")
for r in rows[:10]:
    print(r)

# Save results for LaTeX table generation
results = {
    "n": n,
    "n_techniques": len(corpus_ids),
    "top1_accuracy": top1_acc,
    "top3_accuracy": top3_acc,
    "mrr": mrr,
    "rows": rows,
}
with open("tfidf_results.json", "w") as f:
    json.dump(results, f, indent=2)
