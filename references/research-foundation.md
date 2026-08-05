# Scientific Research Foundation for Antigravity Agentic Triad

The **Antigravity Agentic Triad** workflow is directly grounded in peer-reviewed AI Agent research papers:

## 1. MetaGPT: Standard Operating Procedures & Structured Handoffs
*Hong et al., ICLR 2024 (arXiv:2308.00352)*

- **SOP Decomposition**: Raw natural language dialogue ("Hi, how are you?") introduces cascading hallucinations in multi-agent LLM systems. MetaGPT proves that replacing unstructured chat with **Standardized Operating Procedures (SOPs)** and **structured document handovers** (PRDs, File Lists, Interface Specs) eliminates idle chatter and increases Pass@1 success rates to 85.9%–87.7% on MBPP/HumanEval.
- **Role Boundary Specialization**: Unambiguous role profiles (Architect, Worker, QA/Reviewer) prevent role-bleeding and credit assignment confusion.

## 2. Reflexion: Verbal Reinforcement & Actor-Critic Separation
*Shinn et al., 2023 (arXiv:2303.11366)*

- **Verbal Reinforcement**: Traditional RL scalar rewards fail to provide actionable direction to LLM agents. Reflexion replaces scalar rewards with free-form **verbal reflections** ($sr$), forming a "semantic gradient".
- **Episodic Memory Buffer ($mem$)**: Reflective text is stored in an episodic memory buffer bounded by $\Omega \le 3$ experiences. When retrying a task, the worker conditions its output on prior failure reflections.
- **Clean Context Reviewer**: The Evaluator ($M_e$) and Reflection ($M_{sr}$) models operate independently from the Actor ($M_a$) policy, ensuring unbiased verdict generation (`ship`, `fix-first`, `rethink`).

## 3. Tool-Interactive Critiques (CRITIC & Self-Debugging)
*Gou et al., 2023 (arXiv:2305.00033) & Chen et al., 2023*

- Ground truth verification must rely on **tool-interactive execution** (unit test suites, linters, compilers) rather than internal LLM self-evaluation. 
- Independent Reviewers must verify that test assertions are non-trivial and actually evaluate edge cases before trusting execution status.
