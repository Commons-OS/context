'''
# CLM Training Data Preparation Pipeline

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Objective

To transform the corpus of 1,282+ pattern markdown files into a high-quality, structured dataset suitable for instruction fine-tuning the Commons Language Model (CLM). The goal is to teach the model not just the content of the patterns, but how to reason about them, their relationships, and their application.

---

## 2. Guiding Principles

1.  **Diversity of Tasks**: The dataset must train the model on a variety of tasks, from simple retrieval to complex reasoning.
2.  **Structured Format**: All data will be in the JSONL format, with each line representing a single training example.
3.  **Automated & Repeatable**: The entire pipeline will be encapsulated in a Python script that can be run to regenerate the dataset from the source markdown files.
4.  **Quality over Quantity**: We will prioritize well-structured, accurate examples over a massive, noisy dataset.

---

## 3. The Training Data Format

We will use a unified instruction-tuning format based on the Alpaca dataset structure. Each line in the `dataset.jsonl` file will be a JSON object with the following keys:

```json
{
  "instruction": "A clear instruction for the task.",
  "input": "Optional context or input for the instruction.",
  "output": "The desired response from the model.",
  "task_type": "The category of the task (e.g., qa, summarize, reason)."
}
```

---

## 4. Task Generation Strategies

We will generate training examples for several distinct task types to build a versatile model.

### Task 1: Question Answering (QA)

**Objective**: Teach the model to answer specific questions about a pattern.

**Process**:
1.  For each pattern, parse the markdown content.
2.  Use a template to generate questions based on the YAML frontmatter and key sections (e.g., "Problem", "Solution", "Context").
3.  The `input` will be the pattern title, and the `output` will be the answer extracted from the text.

**Example**:
```json
{
  "instruction": "What problem does the 'Steward Ownership' pattern solve?",
  "input": "",
  "output": "The 'Steward Ownership' pattern solves the problem of mission drift in purpose-driven companies, where the pressure to maximize shareholder profit can compromise the original mission, especially during leadership succession or acquisition.",
  "task_type": "qa"
}
```

### Task 2: Summarization

**Objective**: Teach the model to provide a concise summary of a pattern.

**Process**:
1.  The `summary` field from the pattern's YAML frontmatter will be used as the ground-truth output.

**Example**:
```json
{
  "instruction": "Provide a brief summary of the 'Steward Ownership' pattern.",
  "input": "",
  "output": "A legal structure where a company is controlled by a foundation or trust dedicated to its mission, ensuring that profits serve the purpose, not just the shareholders.",
  "task_type": "summarize"
}
```

### Task 3: Pattern Identification

**Objective**: Teach the model to recommend a pattern given a user's problem description.

**Process**:
1.  The "Problem" section of each pattern will be used as the user's input.
2.  We will use an external LLM (e.g., GPT-4.1-mini) to generate 3-5 paraphrased versions of the problem statement to increase dataset diversity.

**Example**:
```json
{
  "instruction": "I'm worried that as my company grows, we'll be forced to sell out or compromise our values to satisfy investors. What pattern can help?",
  "input": "",
  "output": "The 'Steward Ownership' pattern is designed to address this exact problem by legally protecting a company's mission from purely financial pressures.",
  "task_type": "identify"
}
```

### Task 4: Relationship Reasoning

**Objective**: Teach the model to understand the explicit relationships between patterns.

**Process**:
1.  Parse the `relationships` field from the YAML frontmatter of all patterns.
2.  For each `ENABLES`, `REQUIRES`, and `TENSIONS_WITH` relationship, generate a reasoning example.

**Example (`ENABLES`)**:
```json
{
  "instruction": "How does the 'Self-Managing Teams' pattern relate to 'Holistic Care'?",
  "input": "",
  "output": "The 'Self-Managing Teams' pattern ENABLES 'Holistic Care'. By giving teams the autonomy to make decisions, they can coordinate all aspects of a client's care without needing to go through layers of management, leading to a more integrated and holistic service.",
  "task_type": "reason_relationship"
}
```

**Example (`TENSIONS_WITH`)**:
```json
{
  "instruction": "What is the conflict between 'Rapid Growth' and 'Sustainable Pace'?",
  "input": "",
  "output": "The 'Rapid Growth' pattern is in TENSION WITH 'Sustainable Pace'. The pressure to scale quickly often leads to burnout, technical debt, and cultural erosion, which directly conflicts with the goal of maintaining a healthy, long-term pace for the team and organization.",
  "task_type": "reason_relationship"
}
```

### Task 5: Keyword Extraction

**Objective**: Teach the model to identify the key concepts within a pattern.

**Process**:
1.  Use the `keywords` from the YAML frontmatter as the ground truth.

**Example**:
```json
{
  "instruction": "Extract the main keywords for the 'Steward Ownership' pattern.",
  "input": "",
  "output": "stewardship, ownership, governance, mission-driven, purpose, succession",
  "task_type": "extract_keywords"
}
```

---

## 5. The Data Generation Pipeline (Script)

A Python script (`prepare_data.py`) will perform the following steps:

1.  **Load Patterns**: Walk the `_patterns` directory and load all markdown files into memory, parsing the YAML frontmatter and content.
2.  **Generate Base Dataset**: Iterate through each pattern and generate examples for all task types (QA, Summarization, Identification, Relationships, Keywords).
3.  **(Optional) Augment Data**: Use an LLM API to generate paraphrased questions and problem statements for the QA and Identification tasks.
4.  **Consolidate and Shuffle**: Combine all generated examples into a single list.
5.  **Split Dataset**: Split the consolidated list into `train.jsonl` (90%) and `validation.jsonl` (10%) files.
6.  **Save to Disk**: Write the final JSONL files to the `data/` directory.

---

## 6. Initial Dataset Size Estimate

-   **Patterns**: ~1,300
-   **Tasks per Pattern**: ~10-15 (including multiple relationship examples and augmented questions)
-   **Estimated Total Examples**: 13,000 - 20,000

This is a solid starting point for fine-tuning a 7-14B parameter model.

---

## 7. Next Steps

With this specification in place, the next step is to write the `prepare_data.py` script and generate the first version of the CLM training dataset.
'''
