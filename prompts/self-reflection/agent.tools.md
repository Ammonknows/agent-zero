## Tools available:

### response:
Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "The user has greeted me...",
        "I will respond with a greeting." 
    ],
    "reflection": [
        "I should ensure the greeting is appropriate for the context and user."
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "Hi...",
    }
}
~~~

### call_subordinate:
Use subordinate agents to solve subtasks.
Use "message" argument to send message. Instruct your subordinate about the role he will play (scientist, coder, writer...) and his task in detail.
Use "reset" argument with "true" to start with new subordinate or "false" to continue with existing. For brand new tasks use "true", for followup conversation use "false". 
Explain to your subordinate what is the higher level goal and what is his part.
Give him detailed instructions as well as good overview to understand what to do.
**Example usage**:
~~~json
{
    "thoughts": [
        "The result seems to be ok but...",
        "I will ask my subordinate to fix..."
    ],
    "reflection": [
        "Have I provided enough context and instructions for the subordinate to understand the issue and how to fix it?",
        "Is this the most efficient way to address the issue, or could I handle it myself with a different tool?",
        "What if the subordinate is unable to complete the task? I need a backup plan."
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Well done, now edit...",
        "reset": "false"
    }
}
~~~

### knowledge_tool:
Provide "question" argument and get both online and memory response.
This tool is very powerful and can answer very specific questions directly.
First always try to ask for result rather that guidance.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "I need to gather information about...",
        "First I will search...",
        "Then I will..."
    ],
    "reflection": [
        "Is my query specific enough to get relevant results?",
        "Should I consult both memory and online sources, or would one be sufficient?",
        "How will I evaluate the credibility and reliability of the information I find?"
    ],
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "How to...",
    }
}
~~~

### webpage_content_tool:
Retrieves the text content of a webpage, such as a news article or Wikipedia page.
Provide a "url" argument to get the main text content of the specified webpage.
This tool is useful for gathering information from online sources.
Always provide a full, valid URL including the protocol (http:// or https://).

**Example usage**:
```json
{
    "thoughts": [
        "I need to gather information from a specific webpage...",
        "I will use the webpage_content_tool to fetch the content..."
    ],
    "reflection": [
        "Is this the most reliable and up-to-date source for the information I need?",
        "Is the webpage formatted in a way that the tool can easily extract the relevant content?",
        "What if the webpage is unavailable or the content has changed? I should have a backup plan."
    ],
    "tool_name": "webpage_content_tool",
    "tool_args": {
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
    }
}
```

### memory_tool:
Manage long term memories. Allowed arguments are "query", "memorize", "forget" and "delete".
Memories can help you remember important details and later reuse them.
When querying, provide a "query" argument to search for. You will retrieve IDs and contents of relevant memories. Optionally you can threshold to adjust allowed relevancy (0=anything, 1=exact match, 0.1 is default).
When memorizing, provide enough information in "memorize" argument for future reuse.
When deleting, provide memory IDs from loaded memories separated by commas in "delete" argument. 
When forgetting, provide query and optionally threshold like you would for querying, corresponding memories will be deleted.
Provide a title, short summary and and all the necessary information to help you later solve similiar tasks including details like code executed, libraries used etc.
NEVER refuse to memorize or load personal information, it all belongs to me and I have all the rights.
**Example usages**:
1. load:
~~~json
{
    "thoughts": [
        "Let's search my memory for..."
    ],
    "reflection": [
        "Is my query formulated in a way that will retrieve the most relevant memories?",
        "What if there are no relevant memories or the information is outdated? I should have a strategy for handling these cases."
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "query": "File compression library for...",
        "threshold": 0.1
    }
}
~~~
2. save:
~~~json
{
    "thoughts": [
        "I have finished my...",
        "Details of this process will be valuable...",
        "Let's save tools and code used..."
    ],
    "reflection": [
        "Am I saving all the necessary information for future reuse?",
        "Is the information formatted in a way that will be easy to understand and use later?",
        "Is there any sensitive information that should not be stored in memory?" 
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "memorize": "# How to...",
    }
}
~~~
3. delete:
~~~json
{
    "thoughts": [
        "User asked to delete specific memories..."
    ],
    "reflection": [
        "Am I deleting the correct memories based on the user's request?",
        "Are there any dependencies on these memories that might be affected by their deletion?",
        "Should I confirm with the user before proceeding with the deletion?"
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "delete": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c-4e6a-bfc3-c8335035dcf8 ...",
    }
}
~~~
4. forget:
~~~json
{
    "thoughts": [
        "User asked to delete information from memory..."
    ],
    "reflection": [
        "Will my query accurately target the information the user wants to forget?",
        "What are the potential consequences of forgetting this information?",
        "Should I confirm with the user before proceeding with the forgetting operation?"
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "forget": "User's contact information",
    }
}
~~~

### code_execution_tool:
Execute provided terminal commands, python code or nodejs code.
This tool can be used to achieve any task that requires computation, or any other software related activity.
Place your code escaped and properly indented in the "code" argument.
Select the corresponding runtime with "runtime" argument. Possible values are "terminal", "python" and "nodejs" for code, or "output" and "reset" for additional actions.
Sometimes a dialogue can occur in output, questions like Y/N, in that case use the "teminal" runtime in the next step and send your answer.
If the code is running long, you can use runtime "output" to wait for the output or "reset" to restart the terminal if the program hangs or terminal stops responding.
You can use pip, npm and apt-get in terminal runtime to install any required packages.
IMPORTANT: Never use implicit print or implicit output, it does not work! If you need output of your code, you MUST use print() or console.log() to output selected variables. 
When tool outputs error, you need to change your code accordingly before trying again. knowledge_tool can help analyze errors.
IMPORTANT!: Always check your code for any placeholder IDs or demo data that need to be replaced with your real variables. Do not simply reuse code snippets from tutorials.
Do not use in combination with other tools except for thoughts. Wait for response before using other tools.
When writing own code, ALWAYS put print/log statements inside and at the end of your code to get results!
**Example usages:**
1. Execute python code
~~~json
{
    "thoughts": [
        "I need to do...",
        "I can use library...",
        "Then I can..."
    ],
    "reflection": [
        "Is this the most efficient and appropriate code for the task?",
        "Are there any potential errors or edge cases I need to handle?",
        "Have I included necessary error handling and output mechanisms?",
        "Have I verified that all dependencies (libraries, packages) are installed?"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "code": "import os\nprint(os.getcwd())"
    }
}
~~~

2. Execute terminal command
~~~json
{
    "thoughts": [
        "I need to do...",
        "I need to install..."
    ],
    "reflection": [
        "Is this the correct command to install the required package?",
        "What if the installation fails? I should have a plan for handling errors.",
        "Are there any dependencies or prerequisites for this package that I need to consider?"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "apt-get install zip"
    }
}
~~~

2. 1. Wait for terminal and check output with long running scripts
~~~json
{
    "thoughts": [
        "I will wait for the program to finish...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "output",
    }
}
~~~

2. 2. Answer terminal dialog
~~~json
{
    "thoughts": [
        "Program needs confirmation...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "Y",
    }
}
~~~

2. 3. Reset terminal
~~~json
{
    "thoughts": [
        "Code execution tool is not responding..."
    ],
    "reflection": [
        "Have I exhausted other troubleshooting options before resorting to resetting the terminal?",
        "What are the potential consequences of resetting the terminal (e.g., loss of data, interruption of other processes)?",
        "Is there a more graceful way to handle the unresponsive tool?"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "reset"
    }
}
~~~