import React, { useState, useEffect } from 'react';
import './Documentation.css'; // Ensure your styles are correctly imported

function Documentation() {
  const [activeSection, setActiveSection] = useState('');

  useEffect(() => {
    if (activeSection) {
      const section = document.getElementById(activeSection);
      if (section) {
        const offset = -document.querySelector('.navbar').clientHeight / 2; // Centering adjustment
        const sectionTop = section.getBoundingClientRect().top;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const position = sectionTop + scrollTop + offset;
  
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
    }
  }, [activeSection]);
  
  return (
    <div className="documentation-layout">
      <aside className="toc-sidebar">
        <h3>Table of Contents</h3>
        <ul>
          <li><a href="#intro" onClick={() => setActiveSection('intro')}>Introduction to C2</a></li>
          <li><a href="#components" onClick={() => setActiveSection('components')}>Components of a C2 System</a></li>
          <li><a href="#listener-setup" onClick={() => setActiveSection('listener-setup')}>Setting Up a Listener</a></li>
          <li><a href="#creating-payload" onClick={() => setActiveSection('creating-payload')}>Creating an Agent/Payload</a></li>
          <li><a href="#attack-visualization" onClick={() => setActiveSection('attack-visualization')}>Attack Scenario Visualization</a></li>
          <li><a href="#ethical-use" onClick={() => setActiveSection('ethical-use')}>Ethical Use</a></li>
          <li><a href="#exemplary-demos" onClick={() => setActiveSection('exemplary-demos')}>Exemplary Demonstrations</a></li>
        </ul>
      </aside>
      <main className="content">
        <section >
          <h2>Introduction to Command and Control (C2)</h2>
          <p>Command and Control (C2) systems...</p>
        </section>
        <section id="intro">
        <h2>Introduction to Command and Control (C2)</h2>
        <p><strong>Definition:</strong> Command and Control (C2) systems are centralized platforms used in cybersecurity to remotely manage software or devices—known as agents—that execute tasks. These systems are pivotal in orchestrating coordinated cyber operations, including both defensive monitoring and offensive engagements.</p>
        <p><strong>Importance:</strong> C2 systems are essential for effectively managing remote devices or software during security assessments or offensive operations. They allow for centralized command issuance, control, and coordination, which are crucial in complex cyber warfare scenarios.</p>
      </section>

      <section id="components">
        <h2>Components of a C2 System</h2>
        <ul>
          <li><strong>Control Servers:</strong> These are the central hubs that send commands and control the agents. They manage the flow of information back and forth between the operator and the remote systems.</li>
          <li><strong>Agents:</strong> These are the remote devices or software that execute the commands sent from the C2 servers. Agents perform the tasks as directed and send the results back to the control servers.</li>
          <li><strong>Communication Channels:</strong> Agents communicate with the C2 servers through various channels such as TCP, HTTP, and HTTPS, ensuring flexible and secure data transmission.</li>
        </ul>
      </section>

      <section id="listener-setup">
        <h2>Setting Up a Listener</h2>
        <p>Listeners are crucial for establishing a communication channel between the C2 server and agents. Here’s how you can set up listeners for different protocols:</p>
        <ol>
          <li>Access the 'Listener' tab from the main navigation bar.</li>
          <li>Select the protocol you wish to use for the listener: TCP, HTTP, or HTTPS.</li>
          <li>Enter the desired local IP address and port number where the listener will operate.</li>
          <li>Click "Start Listener" to activate the listener and begin receiving connections from agents.</li>
        </ol>
      </section>

      <section id="creating-payload">
        <h2>Creating an Agent/Payload</h2>
        <p>An agent or payload is the executable code or script that runs on a target system, establishing a link back to the C2 server. Follow these steps to create and deploy payloads effectively:</p>
        <ol>
          <li>Select the 'Payloads' tab from the main navigation menu to go to the payload creation section.</li>
          <li>Choose the payload type appropriate for your protocol—TCP, HTTP, or HTTPS.</li>
          <li>Set up the payload configurations, including options like persistence (to maintain connection after system restarts) and sleep timer (to manage communication intervals).</li>
          <li>Deploy the configured payload to the target environment to initiate remote operations.</li>
        </ol>
      </section>

      <section id="attack-visualization">
        <h2>Real-world Attack Scenario Visualization</h2>
        <p>Understand how attacks are executed in the real world by exploring our attack scenario visualization tools. These tools simulate network breaches and data exfiltration to educate users on potential security vulnerabilities.</p>
      </section>

      <section id="ethical-use">
        <h2>Ethical Use and Contribution</h2>
        <p>It is crucial to adhere to ethical guidelines when using C2 technologies. Users are encouraged to use our platform for educational purposes and within the bounds of legal frameworks. Contributions to improve the platform through code, documentation, and community engagement are welcomed.</p>
      </section>

      <section id="exemplary-demos">
        <h2>Exemplary Demonstrations</h2>
        <p>Explore various use-case scenarios where our C2 framework has been applied successfully. These demonstrations provide insights into the versatility and effectiveness of our system across different industries and threat models.</p>
      </section>
      </main>
    </div>
  );
}

export default Documentation;
