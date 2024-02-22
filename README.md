# Table of Contents

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
  - [2.5 Best Practices/Guard Rails](#25-best-practicesguard-rails)
  - [2.6 Closing Thoughts](#26-closing-thoughts)
- [3. Creating Quick App Prototypes (Target audience: Everyone)](#3-creating-quick-app-prototypes-target-audience-everyone)
  - [3.1 Lang Flow Overview](#31-lang-flow-overview)
  - [3.2 Lang Flow Examples and Templates](#32-lang-flow-examples-and-templates)
- [4. Creating and Deploying AI App (Target audience: Developers)](#4-creating-and-deploying-ai-app-target-audience-developers)
  - [4.1 LangChain Overview](#41-langchain-overview)
  - [4.2 LangChain Examples and Templates](#42-langchain-examples-and-templates)
  - [4.3 Evaluation](#43-evaluation)
  - [4.4 Deployment](#44-deployment)
  - [4.5 Best Practices](#45-best-practices)
- [5. Fine Tuning LM to create custom AI App (Target audience: ML Engineers)](#5-fine-tuning-lm-to-create-custom-ai-app-target-audience-ml-engineers)
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

### 2.2 Typical Uses of Generative LLMs

### 2.3 Modifying Model Behavior

- Few Shot Learnings
- Chain of Thought

### 2.4 Prompt Pattern

### 2.5 Best Practices/Guard Rails

Here is a list of Guard Rails for everyone within SMD:

- Augment and amplify tasks, avoid full automation
- Employ generative models for personal tasks with awareness of limitations
- Apply prompt engineering and RAG patterns for internal app development only
- Utilize curated SDE resources for RAG patterns, ensuring use of authoritative NASA SMD sources
- Reserve fine-tuned models for specialized external apps due to high risk in reputation with prompt-based apps

### 2.6 Closing Thoughts

Full Use requires using combination of these approaches

## 3. Creating Quick App Prototypes (Target audience: Everyone)

### 3.1 Lang Flow Overview

### 3.2 Lang Flow Examples and Templates

- Example 1
- Example 2

## 4. Creating and Deploying AI App (Target audience: Developers)

### 4.1 LangChain Overview

  LangFlow is a tool designed for rapid experimentation and prototyping with LangChain, providing a graphical user interface (GUI) that utilizes react-flow technology. It offers a drag-and-drop feature for easy prototyping and a built-in chat interface for real-time interaction. LangFlow allows users to edit prompt parameters, create chains and agents, track thought processes, and export flows. This modular and interactive design aims to foster creativity and streamline the creation process for dynamic graphs where each node is an executable unit​.




### 4.2 LangChain Examples and Templates

- Example 1
- Example 2

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

### 5.1 Training Data

### 5.2 Fine Tuning the Model

- Example 1
- Example 2

### 5.3 Optimization

- Example 1
- Example 2

### 5.4 Deployment

- Example 1
- Example 2

### 5.5 Best Practices

- Example 1
- Example 2
