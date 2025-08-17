---
title: langchain-ai.github.io-langgraph-how-tos-streaming
slug: langchain-ai.github.io-langgraph-how-tos-streaming
tags:
- source
why_for_designers: TODO
bot_application: TODO
collaboration_prompts:
- What retrieval strategy applies here?
sources:
- url: https://langchain-ai.github.io/langgraph/how-tos/streaming/
  title: langchain-ai.github.io-langgraph-how-tos-streaming
  author: ''
  license: internal-copy
  retrieved_at: '2025-08-17'
  policy: copy
figures: []
updated_at: '2025-08-17'
completed: false
---

# langchain-ai.github.io-langgraph-how-tos-streaming

> Synthesis: TODO

# Stream outputs¶
You can stream outputs from a LangGraph agent or workflow.
## Supported stream modes¶
Pass one or more of the following stream modes as a list to the
stream() or
astream() methods:
|Mode
|Description
|
values
|Streams the full value of the state after each step of the graph.
|
updates
|Streams the updates to the state after each step of the graph. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately.
|
custom
|Streams custom data from inside your graph nodes.
|
messages
|Streams 2-tuples (LLM token, metadata) from any graph nodes where an LLM is invoked.
|
debug
|Streams as much information as possible throughout the execution of the graph.
## Stream from an agent¶
### Agent progress¶
To stream agent progress, use the
stream() or
astream() methods with
stream_mode="updates". This emits an event after every agent step.
For example, if you have an agent that calls a tool once, you should see the following updates:
**LLM node**: AI message with tool call requests **Tool node**: Tool message with execution result **LLM node**: Final AI response
### LLM tokens¶
To stream tokens as they are produced by the LLM, use
stream_mode="messages":
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
)
async for token, metadata in agent.astream(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]},
stream_mode="messages"
):
print("Token", token)
print("Metadata", metadata)
print("\n")
### Tool updates¶
To stream updates from tools as they are executed, you can use get_stream_writer.
from langgraph.config import get_stream_writer
def get_weather(city: str) -> str:
"""Get weather for a given city."""
writer = get_stream_writer()
# stream any arbitrary data
writer(f"Looking up data for city: {city}")
return f"It's always sunny in {city}!"
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
)
for chunk in agent.stream(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]},
stream_mode="custom"
):
print(chunk)
print("\n")
from langgraph.config import get_stream_writer
def get_weather(city: str) -> str:
"""Get weather for a given city."""
writer = get_stream_writer()
# stream any arbitrary data
writer(f"Looking up data for city: {city}")
return f"It's always sunny in {city}!"
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
)
async for chunk in agent.astream(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]},
stream_mode="custom"
):
print(chunk)
print("\n")
Note
If you add
get_stream_writer inside your tool, you won't be able to invoke the tool outside of a LangGraph execution context.
### Stream multiple modes¶
You can specify multiple streaming modes by passing stream mode as a list:
stream_mode=["updates", "messages", "custom"]:
### Disable streaming¶
In some applications you might need to disable streaming of individual tokens for a given model. This is useful in multi-agent systems to control which agents stream their output.
See the Models guide to learn how to disable streaming.
## Stream from a workflow¶
### Basic usage example¶
LangGraph graphs expose the
.stream() (sync) and
.astream() (async) methods to yield streamed outputs as iterators.
## Extended example: streaming updates
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class State(TypedDict):
topic: str
joke: str
def refine_topic(state: State):
return {"topic": state["topic"] + " and cats"}
def generate_joke(state: State):
return {"joke": f"This is a joke about {state['topic']}"}
graph = (
StateGraph(State)
.add_node(refine_topic)
.add_node(generate_joke)
.add_edge(START, "refine_topic")
.add_edge("refine_topic", "generate_joke")
.add_edge("generate_joke", END)
.compile()
)
for chunk in graph.stream( # (1)!
{"topic": "ice cream"},
stream_mode="updates", # (2)!
):
print(chunk)
- The
stream()method returns an iterator that yields streamed outputs.
- Set
stream_mode="updates"to stream only the updates to the graph state after each node. Other stream modes are also available. See supported stream modes for details.
output
{'refineTopic': {'topic': 'ice cream and cats'}}
{'generateJoke': {'joke': 'This is a joke about ice cream and cats'}} |
### Stream multiple modes¶
You can pass a list as the
stream_mode parameter to stream multiple modes at once.
The streamed outputs will be tuples of
(mode, chunk) where
mode is the name of the stream mode and
chunk is the data streamed by that mode.
### Stream graph state¶
Use the stream modes
updates and
values to stream the state of the graph as it executes.
updatesstreams the
**updates**to the state after each step of the graph.
valuesstreams the
**full value**of the state after each step of the graph. *API Reference: StateGraph | START | END*
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
class State(TypedDict):
topic: str
joke: str
def refine_topic(state: State):
return {"topic": state["topic"] + " and cats"}
def generate_joke(state: State):
return {"joke": f"This is a joke about {state['topic']}"}
graph = (
StateGraph(State)
.add_node(refine_topic)
.add_node(generate_joke)
.add_edge(START, "refine_topic")
.add_edge("refine_topic", "generate_joke")
.add_edge("generate_joke", END)
.compile()
)
Use this to stream only the
**state updates** returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.
### Stream subgraph outputs¶
To include outputs from subgraphs in the streamed outputs, you can set
subgraphs=True in the
.stream() method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.
The outputs will be streamed as tuples
(namespace, data), where
namespace is a tuple with the path to the node where a subgraph is invoked, e.g.
("parent_node:<task_id>", "child_node:<task_id>").
for chunk in graph.stream(
{"foo": "foo"},
subgraphs=True, # (1)!
stream_mode="updates",
):
print(chunk)
- Set
subgraphs=Trueto stream outputs from subgraphs.
## Extended example: streaming from subgraphs
from langgraph.graph import START, StateGraph
from typing import TypedDict
# Define subgraph
class SubgraphState(TypedDict):
foo: str # note that this key is shared with the parent graph state
bar: str
def subgraph_node_1(state: SubgraphState):
return {"bar": "bar"}
def subgraph_node_2(state: SubgraphState):
return {"foo": state["foo"] + state["bar"]}
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()
# Define parent graph
class ParentState(TypedDict):
foo: str
def node_1(state: ParentState):
return {"foo": "hi! " + state["foo"]}
builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", subgraph)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
graph = builder.compile()
for chunk in graph.stream(
{"foo": "foo"},
stream_mode="updates",
subgraphs=True, # (1)!
):
print(chunk)
- Set
subgraphs=Trueto stream outputs from subgraphs.
((), {'node_1': {'foo': 'hi! foo'}})
(('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_1': {'bar': 'bar'}})
(('node_2:dfddc4ba-c3c5-6887-5012-a243b5b377c2',), {'subgraph_node_2': {'foo': 'hi! foobar'}})
((), {'node_2': {'foo': 'hi! foobar'}})
**Note** that we are receiving not just the node updates, but we also the namespaces which tell us what graph (or subgraph) we are streaming from.
### Debugging¶
Use the
debug streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.
### LLM tokens¶
Use the
messages streaming mode to stream Large Language Model (LLM) outputs
**token by token** from any part of your graph, including nodes, tools, subgraphs, or tasks.
The streamed output from
messages mode is a tuple
(message_chunk, metadata) where:
message_chunk: the token or message segment from the LLM.
metadata: a dictionary containing details about the graph node and LLM invocation.
If your LLM is not available as a LangChain integration, you can stream its outputs using
custommode instead. See use with any LLM for details.
Manual config required for async in Python < 3.11
When using Python < 3.11 with async code, you must explicitly pass
RunnableConfig to
ainvoke() to enable proper streaming. See Async with Python < 3.11 for details or upgrade to Python 3.11+.
*API Reference: init_chat_model | StateGraph | START*
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START
@dataclass
class MyState:
topic: str
joke: str = ""
llm = init_chat_model(model="openai:gpt-4o-mini")
def call_model(state: MyState):
"""Call the LLM to generate a joke about a topic"""
llm_response = llm.invoke( # (1)!
[
{"role": "user", "content": f"Generate a joke about {state.topic}"}
]
)
return {"joke": llm_response.content}
graph = (
StateGraph(MyState)
.add_node(call_model)
.add_edge(START, "call_model")
.compile()
)
for message_chunk, metadata in graph.stream( # (2)!
{"topic": "ice cream"},
stream_mode="messages",
):
if message_chunk.content:
print(message_chunk.content, end="|", flush=True)
- Note that the message events are emitted even when the LLM is run using
.invokerather than
.stream.
- The "messages" stream mode returns an iterator of tuples
(message_chunk, metadata)where
message_chunkis the token streamed by the LLM and
metadatais a dictionary with information about the graph node where the LLM was called and other information.
#### Filter by LLM invocation¶
You can associate
tags with LLM invocations to filter the streamed tokens by LLM invocation.
*API Reference: init_chat_model*
from langchain.chat_models import init_chat_model
llm_1 = init_chat_model(model="openai:gpt-4o-mini", tags=['joke']) # (1)!
llm_2 = init_chat_model(model="openai:gpt-4o-mini", tags=['poem']) # (2)!
graph = ... # define a graph that uses these LLMs
async for msg, metadata in graph.astream( # (3)!
{"topic": "cats"},
stream_mode="messages",
):
if metadata["tags"] == ["joke"]: # (4)!
print(msg.content, end="|", flush=True)
- llm_1 is tagged with "joke".
- llm_2 is tagged with "poem".
- The
stream_modeis set to "messages" to stream LLM tokens. The
metadatacontains information about the LLM invocation, including the tags.
- Filter the streamed tokens by the
tagsfield in the metadata to only include the tokens from the LLM invocation with the "joke" tag.
## Extended example: filtering by tags
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph
joke_model = init_chat_model(model="openai:gpt-4o-mini", tags=["joke"]) # (1)!
poem_model = init_chat_model(model="openai:gpt-4o-mini", tags=["poem"]) # (2)!
class State(TypedDict):
topic: str
joke: str
poem: str
async def call_model(state, config):
topic = state["topic"]
print("Writing joke...")
# Note: Passing the config through explicitly is required for python < 3.11
# Since context var support wasn't added before then: https://docs.python.org/3/library/asyncio-task.html#creating-tasks
joke_response = await joke_model.ainvoke(
[{"role": "user", "content": f"Write a joke about {topic}"}],
config, # (3)!
)
print("\n\nWriting poem...")
poem_response = await poem_model.ainvoke(
[{"role": "user", "content": f"Write a short poem about {topic}"}],
config, # (3)!
)
return {"joke": joke_response.content, "poem": poem_response.content}
graph = (
StateGraph(State)
.add_node(call_model)
.add_edge(START, "call_model")
.compile()
)
async for msg, metadata in graph.astream(
{"topic": "cats"},
stream_mode="messages", # (4)!
):
if metadata["tags"] == ["joke"]: # (4)!
print(msg.content, end="|", flush=True)
- The
joke_modelis tagged with "joke".
- The
poem_modelis tagged with "poem".
- The
configis passed through explicitly to ensure the context vars are propagated correctly. This is required for Python < 3.11 when using async code. Please see the async section for more details.
- The
stream_modeis set to "messages" to stream LLM tokens. The
metadatacontains information about the LLM invocation, including the tags.
#### Filter by node¶
To stream tokens only from specific nodes, use
stream_mode="messages" and filter the outputs by the
langgraph_node field in the streamed metadata:
for msg, metadata in graph.stream( # (1)!
inputs,
stream_mode="messages",
):
if msg.content and metadata["langgraph_node"] == "some_node_name": # (2)!
...
- The "messages" stream mode returns a tuple of
(message_chunk, metadata)where
message_chunkis the token streamed by the LLM and
metadatais a dictionary with information about the graph node where the LLM was called and other information.
- Filter the streamed tokens by the
langgraph_nodefield in the metadata to only include the tokens from the
write_poemnode.
## Extended example: streaming LLM tokens from specific nodes
from typing import TypedDict
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")
class State(TypedDict):
topic: str
joke: str
poem: str
def write_joke(state: State):
topic = state["topic"]
joke_response = model.invoke(
[{"role": "user", "content": f"Write a joke about {topic}"}]
)
return {"joke": joke_response.content}
def write_poem(state: State):
topic = state["topic"]
poem_response = model.invoke(
[{"role": "user", "content": f"Write a short poem about {topic}"}]
)
return {"poem": poem_response.content}
graph = (
StateGraph(State)
.add_node(write_joke)
.add_node(write_poem)
# write both the joke and the poem concurrently
.add_edge(START, "write_joke")
.add_edge(START, "write_poem")
.compile()
)
for msg, metadata in graph.stream( # (1)!
{"topic": "cats"},
stream_mode="messages",
):
if msg.content and metadata["langgraph_node"] == "write_poem": # (2)!
print(msg.content, end="|", flush=True)
- The "messages" stream mode returns a tuple of
(message_chunk, metadata)where
message_chunkis the token streamed by the LLM and
metadatais a dictionary with information about the graph node where the LLM was called and other information.
- Filter the streamed tokens by the
langgraph_nodefield in the metadata to only include the tokens from the
write_poemnode.
### Stream custom data¶
To send
**custom user-defined data** from inside a LangGraph node or tool, follow these steps:
- Use
get_stream_writer()to access the stream writer and emit custom data.
- Set
stream_mode="custom"when calling
.stream()or
.astream()to get the custom data in the stream. You can combine multiple modes (e.g.,
["updates", "custom"]), but at least one must be
"custom".
No
get_stream_writer() in async for Python < 3.11
In async code running on Python < 3.11,
get_stream_writer() will not work.
Instead, add a
writer parameter to your node or tool and pass it manually.
See Async with Python < 3.11 for usage examples.
from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START
class State(TypedDict):
query: str
answer: str
def node(state: State):
writer = get_stream_writer() # (1)!
writer({"custom_key": "Generating custom data inside node"}) # (2)!
return {"answer": "some data"}
graph = (
StateGraph(State)
.add_node(node)
.add_edge(START, "node")
.compile()
)
inputs = {"query": "example"}
# Usage
for chunk in graph.stream(inputs, stream_mode="custom"): # (3)!
print(chunk)
- Get the stream writer to send custom data.
- Emit a custom key-value pair (e.g., progress update).
- Set
stream_mode="custom"to receive the custom data in the stream.
from langchain_core.tools import tool
from langgraph.config import get_stream_writer
@tool
def query_database(query: str) -> str:
"""Query the database."""
writer = get_stream_writer() # (1)!
writer({"data": "Retrieved 0/100 records", "type": "progress"}) # (2)!
# perform query
writer({"data": "Retrieved 100/100 records", "type": "progress"}) # (3)!
return "some-answer"
graph = ... # define a graph that uses this tool
for chunk in graph.stream(inputs, stream_mode="custom"): # (4)!
print(chunk)
- Access the stream writer to send custom data.
- Emit a custom key-value pair (e.g., progress update).
- Emit another custom key-value pair.
- Set
stream_mode="custom"to receive the custom data in the stream.
### Use with any LLM¶
You can use
stream_mode="custom" to stream data from
**any LLM API** — even if that API does **not** implement the LangChain chat model interface.
This lets you integrate raw LLM clients or external services that provide their own streaming interfaces, making LangGraph highly flexible for custom setups.
*API Reference: get_stream_writer*
from langgraph.config import get_stream_writer
def call_arbitrary_model(state):
"""Example node that calls an arbitrary model and streams the output"""
writer = get_stream_writer() # (1)!
# Assume you have a streaming client that yields chunks
for chunk in your_custom_streaming_client(state["topic"]): # (2)!
writer({"custom_llm_chunk": chunk}) # (3)!
return {"result": "completed"}
graph = (
StateGraph(State)
.add_node(call_arbitrary_model)
# Add other nodes and edges as needed
.compile()
)
for chunk in graph.stream(
{"topic": "cats"},
stream_mode="custom", # (4)!
):
# The chunk will contain the custom data streamed from the llm
print(chunk)
- Get the stream writer to send custom data.
- Generate LLM tokens using your custom streaming client.
- Use the writer to send custom data to the stream.
- Set
stream_mode="custom"to receive the custom data in the stream.
## Extended example: streaming arbitrary chat model
import operator
import json
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START
from openai import AsyncOpenAI
openai_client = AsyncOpenAI()
model_name = "gpt-4o-mini"
async def stream_tokens(model_name: str, messages: list[dict]):
response = await openai_client.chat.completions.create(
messages=messages, model=model_name, stream=True
)
role = None
async for chunk in response:
delta = chunk.choices[0].delta
if delta.role is not None:
role = delta.role
if delta.content:
yield {"role": role, "content": delta.content}
# this is our tool
async def get_items(place: str) -> str:
"""Use this tool to list items one might find in a place you're asked about."""
writer = get_stream_writer()
response = ""
async for msg_chunk in stream_tokens(
model_name,
[
{
"role": "user",
"content": (
"Can you tell me what kind of items "
f"i might find in the following place: '{place}'. "
"List at least 3 such items separating them by a comma. "
"And include a brief description of each item."
),
}
],
):
response += msg_chunk["content"]
writer(msg_chunk)
return response
class State(TypedDict):
messages: Annotated[list[dict], operator.add]
# this is the tool-calling graph node
async def call_tool(state: State):
ai_message = state["messages"][-1]
tool_call = ai_message["tool_calls"][-1]
function_name = tool_call["function"]["name"]
if function_name != "get_items":
raise ValueError(f"Tool {function_name} not supported")
function_arguments = tool_call["function"]["arguments"]
arguments = json.loads(function_arguments)
function_response = await get_items(**arguments)
tool_message = {
"tool_call_id": tool_call["id"],
"role": "tool",
"name": function_name,
"content": function_response,
}
return {"messages": [tool_message]}
graph = (
StateGraph(State)
.add_node(call_tool)
.add_edge(START, "call_tool")
.compile()
)
Let's invoke the graph with an AI message that includes a tool call:
inputs = {
"messages": [
{
"content": None,
"role": "assistant",
"tool_calls": [
{
"id": "1",
"function": {
"arguments": '{"place":"bedroom"}',
"name": "get_items",
},
"type": "function",
}
],
}
]
}
async for chunk in graph.astream(
inputs,
stream_mode="custom",
):
print(chunk["content"], end="|", flush=True)
### Disable streaming for specific chat models¶
If your application mixes models that support streaming with those that do not, you may need to explicitly disable streaming for models that do not support it.
Set
disable_streaming=True when initializing the model.
from langchain.chat_models import init_chat_model
model = init_chat_model(
"anthropic:claude-3-7-sonnet-latest",
disable_streaming=True # (1)!
)
- Set
disable_streaming=Trueto disable streaming for the chat model.
### Async with Python < 3.11¶
In Python versions < 3.11, asyncio tasks do not support the
context parameter.
This limits LangGraph ability to automatically propagate context, and affects LangGraph's streaming mechanisms in two key ways:
- You
**must**explicitly pass
RunnableConfiginto async LLM calls (e.g.,
ainvoke()), as callbacks are not automatically propagated.
- You
**cannot**use
get_stream_writer()in async nodes or tools — you must pass a
writerargument directly.
## Extended example: async LLM call with manual config
from typing import TypedDict
from langgraph.graph import START, StateGraph
from langchain.chat_models import init_chat_model
llm = init_chat_model(model="openai:gpt-4o-mini")
class State(TypedDict):
topic: str
joke: str
async def call_model(state, config): # (1)!
topic = state["topic"]
print("Generating joke...")
joke_response = await llm.ainvoke(
[{"role": "user", "content": f"Write a joke about {topic}"}],
config, # (2)!
)
return {"joke": joke_response.content}
graph = (
StateGraph(State)
.add_node(call_model)
.add_edge(START, "call_model")
.compile()
)
async for chunk, metadata in graph.astream(
{"topic": "ice cream"},
stream_mode="messages", # (3)!
):
if chunk.content:
print(chunk.content, end="|", flush=True)
- Accept
configas an argument in the async node function.
- Pass
configto
llm.ainvoke()to ensure proper context propagation.
- Set
stream_mode="messages"to stream LLM tokens.
## Extended example: async custom streaming with stream writer
from typing import TypedDict
from langgraph.types import StreamWriter
class State(TypedDict):
topic: str
joke: str
async def generate_joke(state: State, writer: StreamWriter): # (1)!
writer({"custom_key": "Streaming custom data while generating a joke"})
return {"joke": f"This is a joke about {state['topic']}"}
graph = (
StateGraph(State)
.add_node(generate_joke)
.add_edge(START, "generate_joke")
.compile()
)
async for chunk in graph.astream(
{"topic": "ice cream"},
stream_mode="custom", # (2)!
):
print(chunk)
- Add
writeras an argument in the function signature of the async node or tool. LangGraph will automatically pass the stream writer to the function.
- Set
stream_mode="custom"to receive the custom data in the stream.


