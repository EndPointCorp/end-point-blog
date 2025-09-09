---
author: "Kürşat Kutlu Aydemir"
title: "Creating Agentic AI Applications"
description: An in-depth guide to understanding AI agents, building agentic applications with orchestration, and implementing them using open-source frameworks.
date: 2025-09-10
tags:
- artificial-intelligence
- agent
- agentic applications
---

![# Man and Woman Back to Back and Holding Guns](/blog/2025/09/creating-agentic-ai-apps/pexels-cottonbro-8717526.jpg)
Photo by [cottonbro studio](https://www.pexels.com/photo/man-and-woman-back-to-back-and-holding-guns-8717526/) on Pexels


# Creating Agentic AI Applications

In rapidly evolving world of AI, agentic AI is emerging as a game-changer. These systems go beyond simple chatbots or predictive models, they're designed to act autonomously, make decisions, and interact with the real world to accomplish goals. In this blog post, we'll dive into what agents are, explore agentic applications and orchestration, and walk through how to build your own agentic applications with open-source examples.

## What Are Agents?

AI agents are autonomous entities that can perceive their environment, reason about it, and take actions to achieve specific objectives. Think of an AI agent as more than just a chatbot, it’s like a digital teammate that can look around, make decisions, and take action on its own. Unlike traditional AI models that respond passively to inputs, agents are proactive: they can break down goals into sub-tasks, use tools (like APIs or databases), maintain memory across interactions, and adapt based on feedback. This makes AI agents ideal for applications requiring independence, such as automation, research, or problem-solving.

At their core, agents typically integrate large language models (LLMs) like GPT-4 or Llama for reasoning, combined with mechanisms for tool invocation and state management. They can operate in loops, iteratively refining their approach until the goal is met.


### Open-Source Examples of AI Agents

If you want to get hands-on with agents, there are already plenty of open-source projects you can experiment with and build on. Here are a few of the most notable:

* **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)**: One of the earliest and well-known autonomous agents. AutoGPT takes a high-level goal, breaks it down into steps, and tries to complete them—whether that means researching a topic, generating code, or managing a workflow. It comes with a simple frontend for building agents, plus a library of ready-made ones (including some quirky ones, like creating viral videos from Reddit trends).
* **[AgentGPT](https://github.com/reworkd/AgentGPT)**: A browser-based platform that lets you spin up and deploy agents without extra setup. Just type in a goal and watch the agent go—browsing the web, running code, or connecting with external services to move toward the objective.

For a longer list of projects, check out this [open-source AI agents directory on Hugging Face](https://huggingface.co/blog/tegridydev/open-source-ai-agents-directory).


## What Are Agentic Applications and Agent Orchestration?

An agentic application is simply an app that uses one or more AI agents to take on complex tasks by itself. Instead of coding every step by hand, you can plug agents together like modules to tackle real-world problems, whether that’s analyzing data, generating content, or even building software. The word `agentic` really just highlights one thing: these systems can act on their own while still working toward your goals.

When you bring more than one agent into the mix, you need a way to coordinate them. This is where orchestration comes in—the art of getting multiple agents to work together smoothly. That might mean giving them specific roles (say, a researcher and a writer), setting up how they communicate, keeping track of what they’ve learned, and making sure they stay on task.

To make this manageable, orchestration frameworks provide ready-made structures, like graphs, crews, or conversation flows, that organize the collaboration. With these in place, it becomes much easier to grow from a single helpful agent to an entire team working together.


### Open-Source Examples of Agentic Applications and Orchestration

If you want to start building agentic applications yourself, there are already a number of open-source frameworks that can help. Here are some of the most popular:

* **[CrewAI](https://github.com/crewaiinc/crewai)**: A lightweight Python framework for orchestrating agents that work together in teams. You can assign roles, define tasks, and let the agents collaborate—without the bulk of larger frameworks like LangChain. It’s simple, fast, and flexible enough for everything from small experiments to enterprise automations.
* **[AutoGen](https://github.com/microsoft/autogen)**: Created by Microsoft, AutoGen is all about multi-agent conversations. Agents can chat with each other, work independently, or take direction from a human. It also supports tool use like code execution and web browsing, making it handy for more specialized domains like math or chemistry.
* **[LangGraph](https://github.com/langchain-ai/langgraph)**: Part of the LangChain ecosystem, LangGraph lets you design agents as graphs, which makes them resilient and stateful. It’s well-suited for long-running workflows, offering built-in memory, human-in-the-loop controls, and debugging support through LangSmith—perfect for production-grade projects.

Other frameworks worth exploring include OpenAI’s Agents SDK (built and evolved upon Swarm) for multi-agent workflows, and MetaGPT, which simulates role-based teams of agents.


## Writing Agentic Applications

To build an agentic application, the first step is choosing the right framework for your needs, for instance, CrewAI if you want simplicity and lightweight orchestration, or AutoGen if you need extensibility and layered APIs.

Once you’ve selected a framework, you’ll need to

- Define agent roles, e.g., researcher, writer, reviewer. Each agent is an actor to complete one or more tasks.
- Equip agents with tools, like search APIs, code interpreters, or custom functions. As you can see, theoretically there is no limit on what you can do with agents.
- Assign tasks and orchestration rules, deciding how agents will interact, share state, and collaborate.
- Add safeguards, error handling, memory management, and human oversight to ensure reliability and trustworthiness.

With those elements in place, you can start assembling workflows. Below, we’ll look at how to get started with one of the most widely used frameworks (CrewAI).

#### Building with CrewAI

First, install CrewAI and ddgs (duckduckgo-search) which is a free search tool that I used for this example.

```bash
pip install crewai 'crewai[tools]'
pip install ddgs
```

CrewAI uses decorators for agents and tasks. Below is a simple example of a crew for researching and reporting on a given topic. It defines two agents: a `researcher` and a `reporting analyst`, and one task for each agent (`research task` and `reporting task`). This code creates a sequential workflow; 

- the researcher gathers data,
- then the analyst compiles a report.

You can extend it with more agents with more tasks or parallel processes.

```python
from typing import Type, Optional
import json

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ddgs import DDGS

class DDGSearchInput(BaseModel):
    query: str = Field(..., description="Search query")

class DDGSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = "Web search via DuckDuckGo. Returns a JSON list of results."
    args_schema: Type[BaseModel] = DDGSearchInput

    # declare this as pydantic field
    max_results: int = Field(8, description="Maximum number of results to return")

    def _run(self, query: Optional[str] = None, **kwargs) -> str:
        if query is None:
            query = kwargs.get("query")

        if not query:
            return json.dumps([], ensure_ascii=False)

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=self.max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body"),
                })
        return json.dumps(results, ensure_ascii=False)

@CrewBase
class ResearchCrew():
    """
    Crew of agents for researching and reporting on given topic.
    """

    def __init__(self, topic):
        self.topic = topic

    @agent
    def researcher(self) -> Agent:
        return Agent(
            role='Senior Data Researcher',
            goal=f'Uncover cutting-edge developments in {self.topic}',
            backstory=f'Seasoned researcher skilled in finding relevant information about {self.topic}.',
            verbose=True,
            tools=[DDGSearchTool(max_results=10)]
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            role='Reporting Analyst',
            goal=f'Create detailed reports from {self.topic} research findings',
            backstory=f'Meticulous analyst who turns {self.topic} data into clear reports.',
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            description=f'Conduct thorough research on {self.topic}.',
            expected_output='A list of 10 bullet points with key findings.',
            agent=self.researcher()
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            description=f'Expand the research on {self.topic} into a full report.',
            expected_output='A markdown-formatted report with detailed sections.',
            agent=self.reporting_analyst(),
            output_file=f'ai_report-{self.topic}.md'
        )

    @crew
    def crew(self) -> Crew:
        """Assembles the crew."""
        return Crew(
            agents=[self.researcher(), self.reporting_analyst()],
            tasks=[self.research_task(), self.reporting_task()],
            process=Process.sequential,
            verbose=True
        )

# run the crew of agents
if __name__ == '__main__':
    topic = input('Topic: ')
    crew = ResearchCrew(topic).crew()
    result = crew.kickoff(inputs={'topic': topic})
    print(result)
```

### Building A Dynamic Agent

We can follow a dynamic approach to create an agentic AI application as well. In this approach, without other 3rd party agent orchestration frameworks we can dynamically create task and agentic processes. Here I present a simple dynamic agent which can work on any given goal until the goal is met. I used OpenAI as LLM in this example. The dynamic approach extracts sub-goals from the given main goal. Then works on tasks and decides if the goals are met.

```python
import os
import json
from openai import OpenAI

class DynamicAgent:
    def __init__(self, goal: str, model: str = "gpt-4o"):
        self.goal = goal
        self.model = model
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.memory = []  # store context and past decisions
        self.max_iterations = 5  # prevent infinite loops

    def get_llm_response(self, prompt: str) -> str:
        resp = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an autonomous agent that creates plans and conditions to achieve goals."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        result = None
        try:
            result = resp.choices[0].message.content
        except Exception:
            # fallback
            result = str(resp)
        print(f"llm result: {result}")
        return result

    def generate_plan(self) -> list:
        prompt = (
            f"Given the goal '{self.goal}', generate a pure JSON list of actionable steps with conditions for success."
            "Don't use any formatting like markdown outside of the JSON content.\n"
            "Each step should include: {'step': 'description', 'condition': 'success criteria'}.\n"
            "Do not rely on predefined rules; infer the steps and conditions from the goal."
        )
        plan = json.loads(self.get_llm_response(prompt))
        self.memory.append({"action": "planning", "output": plan})
        return plan

    def execute_step(self, step: dict) -> str:
        prompt = (
            f"Execute this step: {step['step']}.\n"
            f"Success condition: {step['condition']}.\n"
            "Provide the result and whether the condition was met."
        )
        result = self.get_llm_response(prompt)
        self.memory.append({"step": step['step'], "result": result})
        return result

    def run(self):
        print(f"Starting agent with goal: {self.goal}")
        plan = self.generate_plan()
        results = []
        for i, step in enumerate(plan[:self.max_iterations]):
            print(f"Executing step {i+1}: {step['step']}")
            result = self.execute_step(step)
            results.append(result)
            print(f"Result: {result}")
            # check if goal met
            if "Goal achieved" in result:
                break
        self.save_results_to_markdown(results)

    def save_results_to_markdown(self, results: list):
        filename = f"dynamic_agent_report-{self.goal}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    goal = input("Goal: ")
    agent = DynamicAgent(goal=goal)
    agent.run()
```

## Real-World Examples and Use Cases of Agentic AI Applications

Agentic AI applications are already finding their way into practical, high-value scenarios. By combining autonomy with orchestration, these systems go beyond demos and research projects to deliver measurable impact.

* **Customer Support Automation**: Instead of static chatbots, agentic systems can act as full-service assistants—resolving customer queries, escalating complex cases, and even initiating refunds or ticket creation. They maintain context across long interactions, providing a more human-like experience.
* **Research and Analysis**: Enterprises and individuals use research agents to autonomously scan news sources, academic databases, or financial reports. For example, a financial analyst could deploy agents to track company earnings, summarize investor calls, and produce actionable insights daily.
* **Content Creation Pipelines**: Marketing teams benefit from multi-agent setups where one agent researches a topic, another drafts a blog post, and another optimizes it for SEO. The result is faster, higher-quality content production with less manual effort.
* **Software Development Assistants**: Multi-agent workflows can handle bug triaging, code generation, testing, and documentation. For instance, one agent detects issues, another suggests fixes, while another runs automated tests and updates docs.
* **Healthcare and Biomedicine**: Specialized agents can search the latest medical literature, cross-reference patient data, and generate preliminary diagnostic reports, supporting clinicians in decision-making while reducing information overload.

These examples demonstrate how agentic AI is moving from experimentation to production, delivering tangible value across industries.


## Challenges Ahead

While agentic AI holds promise, several challenges remain before widespread adoption becomes seamless:

* **Reliability and Hallucination**: LLM-based agents can still generate incorrect or fabricated outputs. Ensuring trustworthiness through validation, feedback loops, and human-in-the-loop oversight is crucial. But, personally I am not against hallucination. We humans do hallucination too, and I call it more like authenticity.
* **Security and Safety**: Autonomous agents that can browse the web, execute code, or control external systems pose risks if misconfigured or exploited. Sandboxing, permissions, and guardrails are essential to prevent harmful actions.
* **Evaluation and Benchmarking**: Unlike traditional ML models, measuring the success of agentic systems is difficult. Metrics must capture not only accuracy but also task completion, collaboration quality, and user satisfaction.
* **Ethics and Alignment**: As agents gain autonomy, aligning them with human values, legal frameworks, and ethical principles becomes critical. Misaligned objectives could cause unintended consequences.
* **Integration with Legacy Systems**: Many organizations still rely on older infrastructure. Seamlessly embedding agentic AI into these environments can be a non-trivial engineering challenge.


## Wrapping up

Agentic AI applications represent the future of intelligent software, blending autonomy with collaboration. By leveraging open-source tools like CrewAI and LangGraph or specialized custom agents, you can create powerful solutions tailored to your needs. As AI evolves, we might expect even more sophisticated orchestration capabilities.















