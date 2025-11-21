---
layout: post
comments: true
title:  "Beyond the Prompt: CoT Paths and Premise Ordering"
excerpt: "#paper-summary"
date:   2025-11-21 11:00:00
mathjax: true
---
<style>
.post-header h1 {
    font-size: 35px;
}
.post pre,
.post code {
    
    font-size: 13px; /* make code smaller for this post... */
}
</style>

### Introduction

We will answer two questions:
1. Can LLMs reason effectively without prompting?
2. Does the order in which the model is being queried matter?

### CoT is Hidden in the Decodes

**Paper:** [Chain-of-Thought Reasoning Without Prompting](https://arxiv.org/pdf/2402.10200)

We usually use methods like "think step-by-step" in the prompt to elicit reasoning from LLMs, and greedily decode the output.

This paper argues that greedy decoding is not the way forward. In cases where the model's first prediction is wrong, there is a chance the right answer is in the top-k predictions.

The presence of CoT in the trajectory is a strong indicator that the answer is correct. The authors provide a way to choose them with a method called CoT-decoding. Trajectories with CoT have higher confidence than the others. This confidence is calculated using $$\Delta$$ (Delta), which measures the difference between the top two probability paths:

$$
\Delta_{k, \text{answer}} = \frac{1}{|\text{answer}|} \sum_{x_t \in \text{answer}} (p(x_t^1 | x_{<t}) - p(x_t^2 | x_{<t}))
$$

Using this method, the more confident trajectories are chosen.

### Example: Calculating $$\Delta$$

To visualize this, imagine we ask a model a question. We compare two different paths it could take to generate the answer **"42"**.

**Path A (Greedy Guessing)**
The model jumps straight to the answer without "thinking."
* **Prediction:** "42"
* **Top 1 Probability ($$p_1$$):** 0.45
* **Top 2 Probability ($$p_2$$):** 0.40 (e.g., for "43")
* **$$\Delta$$ Score:** $$0.45 - 0.40 = \mathbf{0.05}$$

**Path B (CoT Path)**
The model generates a reasoning chain first: *"20 plus 22 equals 42."*
* **Prediction:** "42" (after the reasoning steps)
* **Top 1 Probability ($$p_1$$):** 0.95
* **Top 2 Probability ($$p_2$$):** 0.01
* **$$\Delta$$ Score:** $$0.95 - 0.01 = \mathbf{0.94}$$

**Verdict:** Since Path B has a significantly higher $$\Delta$$ ($$0.94 > 0.05$$), the algorithm selects the CoT path, correctly identifying that the reasoning made the answer more robust.

<img src="{{ '/assets/cot_example.png' | relative_url }}" alt="CoT Example" width="100%">

### Experiments & Findings 
Experiments across models like Mistral and PaLM-2 confirm that CoT-decoding consistently outperforms standard greedy methods on math and commonsense tasks. The findings show that this technique effectively "unlocks" latent reasoning in pre-trained models, allowing them to rival instruction-tuned counterparts without needing additional data or prompting.

<img src="{{ '/assets/cot_vs_greedy.png' | relative_url }}" alt="CoT Example" width="100%">

**Paper:** [Premise Order Matters in Reasoning with
Large Language Models](https://arxiv.org/pdf/2402.08939)