import React, { useState, useEffect } from 'react';
import './Documentation.css'; // Ensure your styles are correctly imported

function Documentation({ activeSection: initialActiveSection }) {
  // State to manage the active section
  const [activeSection, setActiveSection] = useState(initialActiveSection);

  const descriptions = [
    "Description for Step 1: Initial phase - The users have to navigate to the Listener page from navigation menu.",
    "Description for Step 2: Protocol Selection - Users selects the type of protocol that they want to listen for. ",
    "Description for Step 3: Starting Listener - Users inputs the local IP and Port that they want to listen in.",
    "Description for Step 4: Successfully Configuring Listener - TCP Listener successfully configured.",
    "Description for Step 5: Creating Payload - Fill the forms and input the ip and port according to the listener configured.",
    "Description for Step 6: Payload Successful - After successful creation of payload it is sent to the User for downloading.",
    "Description for Step 7: Execution - The malware payload is executed within the network.",
    "Description for Step 8: Callback - The agent calling back to the server appears in the callback page.",
    "Description for Step 9: Interaction - Interact button leads to the Interacting Interface with the appropriate agent.",
    "Description for Step 10: Executing Command - Dir command is being executed by the agent",
    "Description for Step 11: Selecting file for upload to the agent.",
    "Description for Step 12: uploading file to the agent",
    "Description for Step 13: Acknowledgment to successful upload",
    "Description for Step 14: Collection - Data is collected from the target environment.",
    "Description for Step 15: Acknowledgement to data download.",
    "Description for Step 16: Changing Directory."
  ];

  useEffect(() => {
    // Function to handle scrolling to the active section
    const scrollToSection = () => {
      const section = document.getElementById(activeSection);
      if (section) {
        const navbarHeight = document.querySelector('.navbar') ? document.querySelector('.navbar').clientHeight : 0;
        const offset = navbarHeight / 2; // Centering adjustment based on navbar height
        const sectionTop = section.getBoundingClientRect().top;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const position = sectionTop + scrollTop - offset;

        window.scrollTo({
          top: position,
          behavior: "smooth"
        });

        // Clear previous active classes and set the current
        document.querySelectorAll('.content section').forEach(sec => {
          sec.classList.remove('active'); // Remove active class from all sections
        });
        section.classList.add('active'); // Add active class to the current section
      }
    };

    // Call scrollToSection when component mounts and whenever activeSection changes
    scrollToSection();
  }, [activeSection]);
  
  return (
    <div className="documentation-layout">
      <aside className="toc-sidebar">
        <h3>Table of Contents</h3>
        <ul>
          <li><a href="#intro" onClick={() => setActiveSection('intro')}>Introduction to C2</a></li>
          <li><a href="#components" onClick={() => setActiveSection('components')}>Components of a C2 System</a></li>
          <li><a href="#evade" onClick={() => setActiveSection('evade')}>Evade-A-C2 Framework</a></li>
          <li><a href="#ethical-use" onClick={() => setActiveSection('ethical-use')}>Ethical Use</a></li>
          <li><a href="#listener-setup" onClick={() => setActiveSection('listener-setup')}>Setting Up a Listener</a></li>
          <li><a href="#creating-payload" onClick={() => setActiveSection('creating-payload')}>Creating an Agent/Payload</a></li>
          <li><a href="#interact" onClick={() => setActiveSection('interact')}>Interacting with the agents</a></li>
          <li><a href="#attack-visualization" onClick={() => setActiveSection('attack-visualization')}>Attack Scenario Visualization</a></li>
        </ul>
      </aside>
      <main className="content">
        <section >
          <h2>Welcome to Documentations</h2>
          <p>Evade-A-C2 Framework</p>
        </section>
        <section id="intro">
          <h2>Introduction to the Command and Control (C2) Framework</h2>

          <h3>Definition of Command and Control (C2)</h3>
          <p>A <strong>Command and Control (C2) system</strong> is a sophisticated technology framework used in cybersecurity that allows an operator to command, control, and coordinate a network of computers or devices remotely. These systems are essential in the fields of cybersecurity and cyber warfare, enabling the execution of remote operations and the management of a series of automated tasks across multiple endpoints.</p>

          <h3>Importance of C2 Systems in Cybersecurity</h3>
          <p><strong>C2 systems</strong> are integral to modern cybersecurity operations, providing essential tools for organizations to manage and mitigate cyber threats effectively. These systems allow cybersecurity professionals to:</p>
          <ul>
              <li><strong>Coordinate Defensive Measures:</strong> Rapidly deploy security updates, coordinate threat responses, and manage defense mechanisms across all connected assets.</li>
              <li><strong>Conduct Offensive Cyber Operations:</strong> Strategically plan and execute operations against targets, leveraging controlled assets to test or breach other systems as part of ethical hacking or penetration testing exercises.</li>
              <li><strong>Enhance Incident Response:</strong> Quickly gather data from incidents, analyze breach extents, and perform remediation tasks from a central command point, reducing the time to respond to and recover from cyber incidents.</li>
          </ul>

          <p>The capability to perform these tasks remotely not only increases the efficiency of cybersecurity teams but also provides a crucial advantage in rapidly evolving security landscapes. By automating tasks and centralizing control, C2 systems help minimize human errors and align cybersecurity efforts more closely with organizational strategies.</p>

          <p>Moreover, the use of C2 frameworks in controlled environments, such as penetration testing labs or red team exercises, equips security professionals with the knowledge and experience needed to anticipate and counteract real-world cyberattacks. These systems simulate potential attack scenarios, allowing teams to understand attacker tactics and refine their defensive strategies accordingly.</p>

      </section>

      <section id="components">
          <h2>Core Components of a C2 System</h2>
          <p>The effectiveness of a C2 system lies in its components, which work together to provide seamless, covert, and efficient communication between the operator and the compromised systems. Key components include:</p>

          <h3>Listeners</h3>
          <p><strong>Listeners</strong> are server-side components that continuously monitor and wait for incoming connections from agents or payloads. They act as the ears of the C2 framework, picking up signals or commands sent from compromised devices.</p>

          <h3>Agents/Payloads</h3>
          <p><strong>Agents or Payloads</strong> refer to software programs or scripts that execute specific tasks on a target machine. These are typically deployed during the initial compromise and ensure persistent access to the device for ongoing operations.</p>

          <h3>Persistence</h3>
          <p><strong>Persistence</strong> refers to techniques used by agents to maintain their presence on an infected device even through reboots and security measures. This is achieved through various methods such as registry modification, startup folder placement, and scheduled tasks. Persistence ensures that the control channel remains open and the compromised device continues to execute C2 commands without requiring re-infection.</p>

          <h3>Beaconing/Sleep Timers</h3>
          <p><strong>Beaconing</strong> is the process by which compromised devices (or agents) communicate back to the C2 server at regular intervals. This can include status updates, exfiltrated data, or requests for further instructions. Beaconing mechanisms are critical for maintaining control over long distances and through firewalls.</p>

          <h3>Defense Evasion</h3>
          <p><strong>Defense Evasion</strong> involves techniques that agents use to avoid detection by antivirus software, firewalls, and other security measures. This can include encrypting command and control communications, mimicking normal network traffic, and leveraging trusted processes to execute malicious activities. The goal is to maintain the functionality of the C2 framework without being detected by security defenses.</p>

          <h3>Callbacks</h3>
          <p><strong>Callbacks</strong> are crucial for the dynamic aspect of C2 operations, where compromised devices or agents report back to the C2 server. These callbacks are not only critical for the ongoing command and control of the agents but also provide the operator with real-time data and status updates.</p>

          <h3>Role of Callbacks</h3>
          <p>Callbacks serve as a communication method by which agents send asynchronous notifications to the C2 server. They are vital for:</p>
          <ul>
              <li><strong>Continual Monitoring:</strong> Keeping track of the health, status, and output of each agent actively deployed in the field.</li>
              <li><strong>Data Exfiltration:</strong> Transferring captured data from the target environment back to the C2 server for analysis and further action.</li>
              <li><strong>Command Confirmation:</strong> Acknowledging the receipt and execution of commands issued by the C2 operator, ensuring that operations proceed as intended.</li>
          </ul>

          <h3>Communication Protocols</h3>
          <p>Effective communication between the C2 server and its agents is facilitated through various <strong>protocols</strong>, each suited to different operational requirements and security levels:</p>
          <ul>
              <li><strong>TCP (Transmission Control Protocol):</strong> Offers reliable, ordered, and error-checked delivery of a stream of bytes. Used where accuracy is more critical than speed, such as uploading/downloading files.</li>
              <li><strong>HTTP (Hypertext Transfer Protocol):</strong> Useful for blending in with normal web traffic, making detection more difficult. It is commonly used for data exfiltration in environments where web traffic is allowed.</li>
              <li><strong>HTTPS (Secure Hypertext Transfer Protocol):</strong> Similar to HTTP but encrypts the communication for additional security, essential for covert operations where sensitive data is transmitted.</li>
              <li><strong>ICMP (Internet Control Message Protocol):</strong> Less commonly used for data transfer, ICMP can be used for covert communications and signaling due to its low bandwidth. It's typically utilized for diagnostic or control purposes but can be adapted for stealthy exfiltration in constrained environments.</li>
              <li><strong>DNS (Domain Name System):</strong> Employed for command and control communications disguised as regular DNS queries. This method is particularly stealthy, as DNS traffic is often allowed to pass through firewalls without inspection, making it a preferred method for bypassing network defenses.</li>
              <li><strong>SMB (Server Message Block):</strong> Although primarily used for file sharing within local networks, SMB can be adapted for intra-network command and control under certain scenarios, especially within segmented corporate environments.</li>
          </ul>

          <p>Understanding these components and how they interact within a C2 framework provides insights into both the capabilities and vulnerabilities of modern cybersecurity architectures. By mastering C2 systems, cybersecurity professionals can better defend against potential attacks and develop more robust security measures.</p>
      </section>

      <section id="evade">
          <h2>About the Evade-C2 Framework</h2>
          <p>The Evade-C2 Framework is a specialized web-based Command and Control (C2) system designed to manage cybersecurity operations effectively. This section explains the specific functionalities and features of Evade C2 as they pertain to its operational components.</p>
          
          <h3>Listeners</h3>
          <p>In Evade-C2, <strong>listeners</strong> are critical for establishing a communication channel with remote agents. Users can set up listeners using various protocols such as TCP, HTTP, and HTTPS, which are configured by specifying the protocol, IP address, and port. This flexibility allows for tailored security configurations that fit diverse operational needs.</p>

          <h3>Agents/Payloads</h3>
          <p>The framework supports multiple types of <strong>agents or payloads</strong> that can be used under TCP, HTTP, and HTTPS protocols. Each agent can be customized extensively within the C2 including options such as:</p>
          <ul>
              <li>Name, Local Host (Lhost), and Local Port (Lport)</li>
              <li>Output type (either .exe for executables or .py for Python scripts)</li>
              <li>Persistence, ensuring that the agent remains active through techniques like autorun registry keys even after the target machine restarts.</li>
          </ul>

          <h3>Communication and Defense Evasion Techniques</h3>
          <p>In Evade-C2, for HTTP and HTTPS protocols, additional options such as <strong>user agents and sleep timers</strong> are available. These features not only help in mimicking normal user behaviors to blend seamlessly with regular traffic but also manage beaconing intervals to evade network monitoring tools. Such combined techniques are crucial in reducing detection risks and helping agents avoid detection by security software, thus enhancing the overall efficacy of defense evasion strategies within the framework.</p>

          <h3>Persistence Techniques</h3>
          <p>Persistence within the Evade-C2 framework is meticulously designed to ensure that agents maintain their presence on a compromised device through reboots and system checks. This is achieved primarily by copying the executable to a strategic location, typically the user's Documents directory (e.g., <code>C:\Users\user's computer name\Documents</code>), which is a common practice to blend in with legitimate files. To automate reactivation of the agent after a reboot, a new registry key is added within the Windows Autorun structure, pointing to this newly copied executable.
           This registry modification ensures that the agent is discreetly launched each time the system starts, maintaining a consistent presence without manual intervention.</p>

          <h3>Callbacks</h3>
          <p><strong>Callbacks</strong> are an essential feature of Evade-C2, providing a direct line of communication back to the C2 server from the agents. They appear on the callbacks page within the framework and include details like the name and protocol of the agent, allowing the user to command and control the agents actively. Users can interact through these callbacks to exfiltrate data, upload files, or conduct reconnaissance within the compromised environment.</p>

          <p>By integrating these sophisticated elements, Evade-C2 offers a robust platform for cybersecurity professionals to conduct comprehensive remote operations. Its capabilities are designed to simplify the complexities of managing C2 infrastructures while providing powerful tools for real-time response and system manipulation.</p>
      </section>

      <section id="ethical-use">
          <h2>Legal and Ethical Use</h2>
          <p>The Evade-C2 framework is committed to upholding the highest standards of ethical use within the cybersecurity domain. This section outlines the framework's alignment with legal requirements and best practices, ensuring that all users operate within a set of defined ethical guidelines.</p>
          
          <h3>Adherence to Legal Standards</h3>
          <p>While the Evade-C2 framework facilitates complex cybersecurity operations, it is not inherently compliant with all international and local cybersecurity laws. Users are strongly encouraged to obtain explicit permission and ensure compliance with relevant legal frameworks before deploying this tool within any network. Comprehensive resources are provided to help users understand data protection, privacy laws, and regulations governing the use of cybersecurity tools. Users must ensure that their use of Evade-C2 adheres to these legal standards to prevent unlawful practices and mitigate potential legal risks.</p>

          <h3>Ethical Guidelines and Best Practices</h3>
          <p>Understanding the ethical implications of using C2 technologies is crucial. Evade-C2 incorporates guidelines that help users navigate the ethical landscape of offensive cybersecurity:</p>
          <ul>
              <li><strong>Responsible Deployment:</strong> Guidelines on how to deploy C2 operations responsibly, ensuring that activities do not harm unintended targets and are conducted within ethical boundaries.</li>
              <li><strong>Transparency and Accountability:</strong> Encouraging transparency in the use of C2 capabilities and promoting accountability by documenting and justifying operational decisions.</li>
              <li><strong>Preventing Misuse:</strong> Strategies to prevent the misuse of the framework in unauthorized contexts, including robust authentication mechanisms and user training programs.</li>
          </ul>
          <p> It is imperative to consider the legal implications of deploying such tools beyond personal or approved environments. Under Nepal's first cyber law, the Electronic Transactions Act, 2063 (2008)/ETA and the Banking Offences and Punishment Act 2064 (2008), there are significant penalties for unauthorized activities involving computer systems: Three-year imprisonment or a fine up to two hundred thousand rupees, or both, for unauthorized activities such as:
            <li>	Damaging or pirating any computer system purposefully.</li>
            <li>  Gaining unauthorized access to any computer system.</li>
            <li>	Intentionally destroying or deleting data from a computer system.</li>
          </p>
          
          <h3>Building Resilience in Cybersecurity</h3>
          <p>By promoting the ethical use of C2 tools and adhering to best practices, Evade-C2 contributes to the resilience of the cyber domain. Users are equipped with the knowledge and tools to enhance their cybersecurity defenses, making them better prepared to handle and mitigate potential cyber threats. This proactive approach not only protects individual systems but also fortifies the broader cybersecurity infrastructure.</p>

          <p>We invite all users to engage with these guidelines actively and integrate ethical considerations into their cybersecurity strategies. By fostering a culture of responsible use, Evade-C2 aims to advance the field of cybersecurity in a sustainable and ethical manner.</p>
      </section>

      <section id="listener-setup">
        <h2>Setting Up a Listener</h2>
        <p>Listeners are crucial for establishing a communication channel between the C2 server and agents. They monitor specific IP addresses and ports for incoming connections from agents, facilitating command and control operations. Here’s how you can set up listeners for different protocols:</p>
        <ol>
            <li>Access the 'Listener' tab from the main navigation bar.</li>
            <li>Select the protocol you wish to use for the listener: TCP, HTTP, or HTTPS.</li>
            <li>Enter the desired local IP address and port number where the listener will operate. The IP address must be one that is assigned to a network interface on your machine </li>
            <li>Click "Start Listener" to activate the listener and begin receiving connections from agents.</li>
        </ol>
        <h3>Choosing the Correct IP Address for Listeners</h3>
        <p>It is essential to choose an appropriate IP address for your listener setup:</p>
        <ul>
            <li><strong>Local IP Address:</strong> Use an IP address that is assigned to your server to ensure the listener can bind to it successfully. If the IP address does not belong to your machine, the system will likely return an error and fail to start the listener.</li>
            <li><strong>Public vs. Private IPs:</strong> Depending on your operational needs, you may choose a public IP address for receiving connections from the internet or a private IP for managing devices within the same network.</li>
           
        </ul>
        <p>Correct IP configuration ensures that your C2 system can communicate effectively without interruptions.</p>
    </section>

      <section id="creating-payload">
        <h2>Creating an Agent/Payload</h2>
        <p>An agent or payload is the executable code or script that runs on a target system, establishing a link back to the C2 server. Follow these steps to create and deploy payloads effectively:</p>
        <ol>
          <li>Select the 'Payloads' tab from the main navigation menu to go to the payload creation section.</li>
          <li>Choose the payload type appropriate for your protocol—TCP, HTTP, or HTTPS.</li>
          <li>Set up the payload configurations, including options like persistence (to maintain connection after system restarts) and sleep timer (to manage communication intervals).</li>
          <li> How to enable persistance.What does persistance do in this? how to add Beaconing Timer, add user agent for http,https agents</li>
          <li>Deploy the configured payload to the target environment to initiate remote operations.</li>
        </ol>
      </section>

      <section id="interact">
          <h2>Interacting with Agents</h2>
          <p>Interacting with agents is a core functionality of the Evade-C2 framework, allowing users to execute commands and manage files on compromised systems once a callback has been established. This interaction is initiated through a user-friendly interface that provides robust control over deployed agents.</p>

          <h3>Initiating Interaction</h3>
          <p>Interaction with an agent begins when the Evade-C2 server receives a callback from the agent, signaling that the agent is active and ready to receive commands. Each active agent appears on the user's callback page with an 'Interact' button labeled with the agent's name and the protocol it uses. This setup ensures that users can easily identify and connect to the appropriate agent.</p>

          <h3>Capabilities of Interaction</h3>
          <p>Once the interaction is initiated, users can engage with the agent to perform a variety of tasks:</p>
          <ul>
              <li><strong>Command Execution:</strong> Users can execute standard command-line instructions (CMD commands) to explore and manage the system state of the agent. This can include viewing directory listings, modifying files, or any other commands that the command prompt supports.</li>
              <li><strong>File Management:</strong> Evade-C2 provides capabilities for both uploading and downloading files. Users can upload scripts, updates, or other necessary files to the agent's system. Conversely, they can download files from the agent's system to their local machine for analysis, backup, or other purposes.</li>
              <li><strong>Real-time Feedback:</strong> The framework ensures that all commands executed and file transfers initiated provide immediate feedback. This real-time interaction helps users to efficiently manage remote systems and quickly adapt to any operational needs or issues that arise.</li>
          </ul>

          <h3>Security and Control</h3>
          <p>To maintain security and control over these interactions, Evade-C2 employs a robust security strategy that includes authentication and encryption tailored to each communication protocol:</p>

          <ul>
              <li><strong>HTTPS:</strong> Communications via HTTPS are secured using TLS certificates generated with OpenSSL, which encrypts data to protect against unauthorized interception. Additionally, like with TCP and HTTP, HTTPS also requires each agent to verify its unique agent ID upon attempting to connect. This dual-layer security ensures that both data integrity and access control are maintained, providing comprehensive security for HTTPS communications.</li>
              <li><strong>TCP and HTTP:</strong> Although basic TCP and HTTP do not inherently include encryption, Evade-C2 enhances their security through the use of unique agent IDs. Each agent is assigned an ID when created, stored securely in the framework's database. For an agent to establish a connection with the C2 server, its unique ID must be presented and validated against the database records. This authentication process helps secure the connection against unauthorized access and ensures that only recognized agents can communicate with the server.</li>
          </ul>

          <p>This multi-faceted security approach allows Evade-C2 to ensure robust protection across all used protocols. By integrating encryption with comprehensive authentication measures, Evade-C2 provides both secure data transmission and stringent access controls, essential for maintaining operational security and integrity in complex cyber environments.</p>

          <p>By leveraging these interactive capabilities, users of Evade-C2 can effectively manage and utilize their network of agents, enhancing their operational effectiveness and response capabilities in live environments.</p>
      </section>

      <section id="attack-visualization">
      <h2>Real-world Attack Scenario Visualization/Exemplary Demonstrations</h2>
      <p>Understand how attacks are executed in the real world by exploring our attack scenario visualization tools. These tools simulate network breaches and data exfiltration to educate users on potential security vulnerabilities.</p>
      <ol>
        {Array.from({ length: 16 }).map((_, index) => (
          <li key={index}>
            <h4>Step {index + 1}</h4>
            <p>{descriptions[index]}</p>
            <img src={`/images/${index + 1}.png`} alt={`Screenshot ${index + 1}`} style={{ width: '100%', height: 'auto', margin: '20px 0' }} />
          </li>
        ))}
      </ol>
    </section>
      </main>
    </div>
  );
}

export default Documentation;
