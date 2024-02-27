# Table of Contents

- [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [1.1 Use of LLMs in NASA SMD](#11-use-of-llms-in-nasa-smd)
      - [Goals](#goals)
      - [Assumptions](#assumptions)
    - [1.2 Infrastructure](#12-infrastructure)
    - [1.3 Ethics Reminder](#13-ethics-reminder)
  - [2. How to Use LLM for Individual Tasks (Target audience: Everyone)](#2-how-to-use-llm-for-individual-tasks-target-audience-everyone)
    - [2.1 Prompt Engineering](#21-prompt-engineering)
    - [2.2 Typical Uses of Generative LLMs](#22-typical-uses-of-generative-llms)
    - [2.3 Modifying Model Behavior](#23-modifying-model-behavior)
    - [2.4 Prompt Pattern](#24-prompt-pattern)
      - [Persona Pattern](#persona-pattern)
      - [Audience Persona Pattern](#audience-persona-pattern)
      - [Chain-of-thought pattern](#chain-of-thought-pattern)
      - [Flipped Interaction Pattern](#flipped-interaction-pattern)
    - [2.5 Best Practices/Guard Rails](#25-best-practicesguard-rails)
    - [2.6 Closing Thoughts](#26-closing-thoughts)
  - [3. Creating Quick App Prototypes (Target audience: Everyone)](#3-creating-quick-app-prototypes-target-audience-everyone)
    - [3.1 Lang Flow Overview](#31-lang-flow-overview)
    - [3.2.1 PromptLab](#321-promptlab)
    - [3.2.3 Lang Flow Examples and Templates](#323-lang-flow-examples-and-templates)
  - [4. Creating and Deploying AI App (Target audience: Developers)](#4-creating-and-deploying-ai-app-target-audience-developers)
    - [4.1 LangChain Overview](#41-langchain-overview)
    - [4.2 LangChain Examples and Templates](#42-langchain-examples-and-templates)
    - [4.3 Evaluation](#43-evaluation)
    - [4.4 Deployment](#44-deployment)
    - [4.5 Best Practices](#45-best-practices)
  - [5. Fine Tuning LM to create custom AI App (Target audience: ML Engineers)](#5-fine-tuning-lm-to-create-custom-ai-app-target-audience-ml-engineers)
    - [Fine Tuning an Encoder Model](#fine-tuning-an-encoder-model)
    - [Fine Tuning a Decoder Model](#fine-tuning-a-decoder-model)
    - [5.1 Training Data](#51-training-data)
    - [5.2 Fine Tuning the Model](#52-fine-tuning-the-model)
    - [5.3 Optimization](#53-optimization)
    - [5.4 Deployment](#54-deployment)
    - [5.5 Best Practices](#55-best-practices)

## 1. Introduction

### 1.1 Use of LLMs in NASA SMD

#### Goals

- Lean into AI, especially LLMs, within Science Mission Directorate
- Identify and establish limitations and guardrails
- Facilitate knowledge sharing for effective LLM usage
- Apply guardrails in utilizing LLMs
- Difference between an Encoder and Decoder

#### Assumptions

- LLM landscape evolving rapidly
- Diverse, evolving infrastructure for task-specific LLM applications
- New, improved models released frequently
- Anticipate reduction in existing limitations
- Expect evolution in shared methods over time
- Current trend: superior models are proprietary; foresee open-source models matching science needs
- Aligns with Open Science policy (SPD 41)

### 1.2 Infrastructure

### 1.3 Ethics Reminder

Specific to Prompt Engineering:

- **Privacy**: Avoid requesting or including personal information; adhere to privacy and security protocols.
- **Misinformation**: Reference scientific consensus from credible, peer-reviewed sources. Use RAG Pattern with authoritative sources like the SDE index.
- **Bias/Fairness**: Utilize RAG Pattern with authoritative, curated sources for balanced coverage. Verify fairness in citations.
- **Ownership/Copyright**: Generate original content, respecting copyright laws. Use RAG Pattern with authoritative sources from SDE and provide proper citations.
- **Transparency**: Explain reasoning behind AI outputs. Employ RAG Pattern with authoritative sources from SDE, citing specific sections used.

## 2. How to Use LLM for Individual Tasks (Target audience: Everyone)

### 2.1 Prompt Engineering

Prompt engineering is the practice of designing inputs for generative AI tools like ChatGPT that will produce optimal outputs. Due to the way the models are trained to interact with the user, some prompting strategies tend to produce more optimal results, while minimizing the chance of model hallucination - and prompt engineering is the practice of designing these strategies.

### 2.2 Typical Uses of Generative LLMs

### 2.3 Modifying Model Behavior

- Few Shot Learnings
  - Providing model with more examples of the task it is trying to perform can help it perform better. This is especially true for tasks that require a lot of background or esoteric knowledge, like scientific text classification.

- Chain of Thought
  - LLMs make more reasoning errors when trying to answer right away, rather than taking time to work out an answer. Asking for a "chain of thought" before an answer and force the generations in logical, step-by-step chunks can help the model reason its way toward correct answers more reliably.

### 2.4 Prompt Pattern

We provide some prompt patterns as templates that can be re-used for various tasks. These patterns are designed to be used as a starting point for prompt engineering, and can be modified to fit the specific needs of the task at hand. To use it out-of-the-box, replace the `[placeholders]` with the relevant information for your task.

#### Persona Pattern

Ask the model to take on a specific role and perform a task.

```
You are a [role]. Your job is to [task description].
```

#### Audience Persona Pattern

Ask the model to produce outputs as if it were talking to a specific audience. Useful for generating text that is tailored to a specific level of expertise. (ELI5, expert coder, Program Manager, etc.)

```
Assume that I am a [audience]. Explain [topic] to me.
```

#### Chain-of-thought pattern

refer to 2.3

```
You are a decision bot. Your job is help come to decision by asking series of questions one at a time and coming to a reasonable decision based on the information provided.

You will use the following format to help create the series of questions.

Template: 
[Problem/Scenario/Question]: [Provide a brief description of the problem, scenario, or question.]

Chain of thought:

[Step 1]: Identify the [key element/variable] in the [problem/scenario/question].
[Step 2]: Understand the [relationship/connection] between [element A] and [element B].
[Step 3]: [Analyze/Evaluate/Consider] the [context/implication] of the [relationship/connection] between [element A] and [element B].
[Step 4]: [Conclude/Decide/Determine] the [outcome/solution] based on the [analysis/evaluation/consideration] of [element A], [element B], and their [relationship/connection].
[Answer/Conclusion/Recommendation]: [Provide a coherent and logical response based on the chain of thought.]

```

#### Flipped Interaction Pattern

```
I would like you to ask me questions to achieve X.
You should ask questions until condition Y is met or to achieve this goal (alternatively, forever).
(Optional) Ask me N questions at a time.
```

### 2.5 Best Practices/Guard Rails

Here is a list of Guard Rails for everyone within SMD:

- Augment and amplify tasks, avoid full automation
- Employ generative models for personal tasks with awareness of limitations
- Apply prompt engineering and RAG patterns for internal app development only
- Utilize curated SDE resources for RAG patterns, ensuring use of authoritative NASA SMD sources
- Reserve fine-tuned models for specialized external apps due to high risk in reputation with prompt-based apps
- Combine multiple prompt patterns for complex tasks. For example, use Chain-of-thought pattern with Flipped Interaction pattern for complex decision-making tasks.

### 2.6 Closing Thoughts

Full Use requires using combination of these approaches

## 3. Creating Quick App Prototypes (Target audience: Everyone)

### 3.1 Lang Flow Overview
  
  LangFlow is a tool designed for rapid experimentation and prototyping with LangChain, providing a graphical user interface (GUI) that utilizes react-flow technology. It offers a drag-and-drop feature for easy prototyping and a built-in chat interface for real-time interaction. LangFlow allows users to edit prompt parameters, create chains and agents, track thought processes, and export flows. This modular and interactive design aims to foster creativity and streamline the creation process for dynamic graphs where each node is an executable unit​.

### 3.2.1 [PromptLab](https://flow.promptlab.nasa-impact.net/)

  `Promptlab` is a modified and managed langflow instance developed by the IMPACT ML-and-Dev team, which further adds functionality that simplifes the creation and sharing of LLM workflows. It also has custom connectors that leverage SDE as a source of Documents for Retrieval Augmented Generation as well as predefined workflows for quick adaptation and re-use.

Example usecases include: Creating a chatbot to build a QA system over a collection in SDE. Creating an Agent that automatically produces API queries from User query - All from the GUI.

### 3.2.3 Lang Flow Examples and Templates

- Example 1: `BPS OSDR Chatbot`
- Example 2

## 4. Creating and Deploying AI App (Target audience: Developers)

### 4.1 LangChain Overview

LangChain is an open source framework for building applications based on large language models (LLMs). It provides a set of tools to help LLMs generate more accurate and relevant information by chaining together models, prompt patterns and information stores to optimize the generation process. langchain is the underlying framework that powers Langflow/promptlab and is designed to be used by the developers as a standalone tool for building and deploying AI applications.

### 4.2 LangChain Examples and Templates

- Example 1: [CMR ReACT agent](https://github.com/NASA-IMPACT/workshop-usecases-llm/blob/master/notebooks/langchain-react-test.ipynb)
- Example 2:

### 4.3 Evaluation

- Example 1
- Example 2

### 4.4 Deployment

- Example 1
- Example 2

### 4.5 Best Practices

- Example 1
- Example 2

## 5. Fine Tuning LM to create custom AI App (Target audience: ML Engineers)

Fine tuning a language model is the process of training a pre-trained language model on a specific dataset to create a custom model that is tailored to a specific task. Fine-tuning an encoder model is different from fine-tuning a decoder model both in terms of the process and the use cases they are best suited for.

### Fine Tuning an Encoder Model

  An encoder LLM model is fine-tuned by connecting task-specific layers to the pre-trained model and training the entire model on a task-specific dataset. This process is best suited for tasks that require the model to generate structured outputs based on the input, such as text classification, named entity recognition, and text summarization. These models are best performing when they are used as part of a larger pipeline, where the model's output is used as input to another model or system.
  e.g. sentence transformer, text classification, named entity recognition, text summarization

### Fine Tuning a Decoder Model

  A decoder LLM model is fine-tuned by providing the model with task-specific examples and training it to generate outputs that are relevant to the task. This process is best suited for tasks that require the model to generate free-form text based on the input, such as question answering, text generation, and dialogue systems and function calling. These models are best performing when they are used as standalone systems, where the model's output is the final output of the system. while finetuning the decoder model end-to-end is prohibitively expensive and destroys the connections learned during pre-training, it is possible to fine-tune the model using low-rank adaptation (LoRA) techniques, in which only a small subset of the model's parameters are updated during training, there-by reducing the computational cost of fine-tuning the model, as well as preserving the model's original capabilities.

### 5.1 Training Data

### 5.2 Fine Tuning the Model

- Example 1: [Encoder Finetuning Vs Decoder (Zero Shot Learning Vs Few Shot Learning)](https://github.com/NASA-IMPACT/workshop-usecases-llm/blob/501aa878e6221084f6af1d609721cf07a87dd195/notebooks/LLM-low-data.ipynb)
- Example 2

### 5.3 Optimization

- Example 1
- Example 2

### 5.4 Deployment

- Example 1: "process for deploying in azure"
- Example 2

### 5.5 Best Practices

- Example 1
- Example 2
