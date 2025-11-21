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

### CoT is Hidden

**Paper 1:** 
[Chain-of-Thought Reasoning Without Prompting](https://arxiv.org/pdf/2402.10200)

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

<img src="{{ '/assets/cot_reasoning/cot_example.png' | relative_url }}" alt="CoT Example" width="100%">

### Experiments & Findings 
Experiments across models like Mistral and PaLM-2 confirm that CoT-decoding consistently outperforms standard greedy methods on math and commonsense tasks. The findings show that this technique effectively "unlocks" latent reasoning in pre-trained models, allowing them to rival instruction-tuned counterparts without needing additional data or prompting.

<img src="{{ '/assets/cot_reasoning/cot_vs_greedy.png' | relative_url }}" alt="CoT Example" width="100%">


### The Fragility of LLM Reasoning


**Paper 2:** 
[Premise Order Matters in Reasoning with
Large Language Models](https://arxiv.org/pdf/2402.08939)

The core point of this paper is LLM's frailty and their dependence in order in which the premises are being presented to them. 

Ideal state for LLMs to perform is when the premise order is presented in **Forward Order**. This aligns well with the intermediate steps required to reach the conclusion. 

In Logical reasoning tasks, each problem has a set of facts, a set of rules, and a conclusion. The authors quantify the "disorder" of these premises using [**Kendall Tau ($$\tau$$) distance**](https://www.wikiwand.com/en/articles/Kendall_tau_distance).

* **$$\tau = 1$$ (Forward Order):** Premises appear exactly in the order needed for the proof (Forward Chaining).
* **$$\tau = -1$$ (Backward Order):** Premises appear in the exact reverse order (Backward Chaining).
* **$$\tau \approx 0$$ (Shuffled):** Random ordering.

The study evaluated GPT-4-turbo, GPT-3.5-turbo, PaLM 2-L, and Gemini 1.0 Pro. The results revealed distinct behaviors across models

Across all models, there's a strong preference for Forward order $$\tau = 1$$ and inclusion of distracting rules drastically amplifies the sensitivity to order.With 10 distracting rules, performance drops significantly when the order is shuffled ($$\tau=0$$). This confirms that LLMs are easily distracted, and "noise" makes them lose track of the logical thread if the order isn't perfect.

**GPT-4-turbo (The U-Shape):** It performs best at $$\tau=1$$, drops performance at $$\tau=0$$ (random), but recovers performance at $$\tau=-1$$. This suggests GPT-4 is capable of Backward Chaining (reasoning from conclusion back to premises) effectively.

<img src="{{ '/assets/cot_reasoning/ucurve.png' | relative_url }}" alt="CoT Example" width="100%">

**PaLM 2-L (The Linear Drop):** 
This model struggles significantly with backward order. Its performance degrades linearly as the order moves away from $$\tau=1$$.

**Fact Hallucination:** This is the most common error type in logical reasoning.The model reads a rule like "If A, then B". If the fact "A" appears later in the prompt, the model (processing left-to-right) hasn't seen it yet. Instead of waiting, it hallucinates that "A" is true to satisfy the rule immediately.This error escalates dramatically as $$\tau$$ decreases (becomes more disordered).

<img src="{{ '/assets/cot_reasoning/hallucination.png' | relative_url }}" alt="CoT Example" width="100%">

Finally These behavior shouldn't be confused with **"Lost-in-the-middle"** effect, which is  models forget information in the middle of long contexts. However, the benchmark problems here are short (<300 tokens). Experiments placing rules at the beginning, middle, or end showed little difference compared to the massive impact of scrambling the order.

These experiments confirm that LLMs possess a "left-to-right" reasoning bias that makes them significantly inferior to humans in handling disordered information. While humans can scan back and forth to assemble a proof, LLMs attempt to greedily resolve reasoning steps sequentially.

**Usage:**
For Retrieval Augmented Generation (RAG) or Agent workflows, simply retrieving context isn't enough; the context must be topologically sorted to match the reasoning chain.We need to preprocess the input to organize it (e.g., generating a dependency graph before feeding it to the LLM).