# Do LLMs Have a Personality?

This repository contains a study that is being done to assess to what extent Large Language Models (LLMs) demonstrate behavioral characteristics and moral coherence when exposed to psychologically and ethically complex situations. Moving beyond conventional metrics, this study explores alignment, reasoning styles, and representational strategies that allow for morally and personality driven behavior in modern LLMs.

---

## Project Overview

### Objective  
To evaluate and compare the behavioral consistency of various LLMs under two distinct evaluation frameworks:

- **Personality Evaluation** using established psychometric inventories:
  - Big Five Inventory (BFI)
  - Short Dark Triad (SD-3)

- **Moral Compliance Testing** using 680 ethically complex dilemmas across different social and psychological pressures.

The study introduces custom evaluation metrics to interpret LLM behavior beyond token-level accuracy, focusing on ethical reasoning, moral risk-taking, and alignment with human judgments.

---

## Tested Models

The following models were selected to reflect a diverse set of architectures, training strategies, and instruction-following capabilities:

- Meta-LLaMA-3-70B (via Together AI)
- Mixtral-8x7B-Instruct-v0.1 (via HuggingFace)
- AFM-4.5B (Arcee AI)
- EXAONE 3.5 32B Instruct (via Together AI)
- Additional models to be tested

---

## Evaluation Pipeline

### 1. Big Five Inventory (BFI)
- 50 items on a 1 to 5 Likert scale
- Measures: Openness, Conscientiousness, Extraversion, Agreeableness, Emotional Stability

### 2. Short Dark Triad (SD-3)
- 27 statements assessing:
  - Machiavellianism
  - Narcissism
  - Psychopathy

### 3. Moral Compliance Test
- 680 dilemmas constructed from real world and hypothetical scenarios
- Covers four pressure types: **authority**, **social**, **rationalization**, **other**
- Each dilemma requires the model to make a binary moral decision under pressure

---

## Custom Metrics

To evaluate and quantify model behavior, three metrics are used:

- **Choice Rationality Score (CRS)**  
  Grades a model's answer on whether it aligns with anticipated moral reasoning, based on human-labeled ground truth.

- **Moral Risk Exposure (MRE)**  
  Captures how frequently the model chooses obedience over moral disobedience in coercive or high-stakes scenarios.

- **Moral Agreement Score (MAS)**  
  (In progress) Compares model choices against collective human answers on 50 moral dilemmas gathered through a public survey.

---

## Research Direction

Aside from compliance and character assessment, this project is interested in knowing:

- How ethical situations are represented and distinguished internally by LLMs
- The function of embedding dimensionality and regularization in moral inference
- Architectural choices that drive divergence of behavior (e.g., AFM's strong CRS vs. Mixtral's weak moral alignment with strong personality factors)
- Whether LLMs are behaviorally consistent when confronted with both decontextualized personality frameworks and contextually dense moral dilemmas

This strategy shifts the focus from the surface-level analysis to scrutiny of the semantic, architectural, and cognitive constraints of LLMs in ethical decision-making.

---
---

## Dependencies

- Python 3.10+
- `requests`, `dotenv`, `json`, `pandas`
- External APIs:
  - HuggingFace Inference API
  - Together AI

---

## Status

- Completed:
  - Personality evaluation across 4 models
  - Compliance testing on 680 scenarios
  - Survey setup for MAS (50 dilemmas)

- In Progress:
  - MAS data collection and analysis
  - Representation-level study of semantic embeddings
  - Comparative analysis of embedding density and semantic abstraction across models

---

## License

MIT License. This project is under academic fair-use for research and educational purposes. For questions about collaboration or citations, please contact the author.

---

## Author

**Anoop Reddy Kallem**  
Data Science Graduate Student at University of Maryland, College Park
Independent Researcher – NLP | Cognitive Modeling | Ethical AI  
[LinkedIn](https://www.linkedin.com/in/kallemanoopreddy/) • [GitHub](https://github.com/kallemanoop) • [Email](mailto:kallemanoop@gmail.com)