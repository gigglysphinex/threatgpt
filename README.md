# ThreatGPT: Hierarchical Multi-Agent CTI Architecture

This repository accompanies the paper *"ThreatGPT: A Hierarchical Multi-Agent
Architecture for LLM-Based Cyber Threat Intelligence Analysis --- Design,
Preliminary Evaluation, and Open Challenges."*

The paper proposes a three-agent (Extractor / Mapper / Risk Assessor)
architecture for LLM-based CTI analysis, grounded in a real, reproducible
preliminary experiment for the Mapper Agent's core retrieval sub-task.

**Status:** architecture/design paper with one implemented and evaluated
baseline (TF-IDF retrieval over MITRE ATT&CK). The full LLM-based pipeline
(Extractor Agent, LLM-based Mapper Agent, Risk Assessor Agent, adversarial
defenses) is proposed but not yet implemented — see the paper's Limitations
and Future Work sections.

## Repository structure

```
paper/
  threatgpt_paper.tex     LaTeX source (Springer LNCS format)
  threatgpt_paper.pdf     Compiled PDF
experiment/
  eval_set.py             49 hand-labelled CTI sentences with ATT&CK labels
  run_experiment.py        TF-IDF baseline experiment script
data/
  attack_techniques.json  Extracted MITRE ATT&CK Enterprise v18 technique catalogue
results/
  tfidf_results.json      Output of run_experiment.py (real, measured results)
```

## Reproducing the baseline experiment

```bash
pip install scikit-learn numpy
cd experiment
python run_experiment.py
```

This re-derives the results reported in the paper (Section: Preliminary
Experiment): Top-1 accuracy 0.531, Top-3 accuracy 0.714, MRR 0.655 over the
49-sentence evaluation set against the 222 top-level MITRE ATT&CK Enterprise
techniques.

The `data/attack_techniques.json` file was extracted from the official MITRE
ATT&CK STIX bundle (`https://github.com/mitre/cti`, Enterprise v18). To
regenerate it from scratch, download
`enterprise-attack/enterprise-attack.json` from that repository and re-run
the extraction snippet described in the paper's experiment section.

## Compiling the paper

```bash
cd paper
pdflatex threatgpt_paper.tex
pdflatex threatgpt_paper.tex   # second pass for references
```

Requires the `llncs` LaTeX class (available via `texlive-publishers` on
Debian/Ubuntu, or from Springer's LNCS author kit).

## License

TODO: choose a license (e.g., MIT for code, CC-BY for paper) before making
the repository public.
