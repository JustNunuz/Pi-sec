# **Deauthentication Attack**  

A **Deauthentication (Deauth) Attack** is a type of **Denial of Service (DoS) attack** that targets wireless networks. It forces devices to disconnect from a Wi-Fi network by sending **deauthentication frames** (packets).  

### **How Deauth Attacks Work?**  
Essentially, a deauthentication attack works through the following steps:  

1. Some Wi-Fi networks **do not effectively verify MAC addresses**, making them vulnerable.  
2. Attackers **spoof MAC addresses** and send deauthentication frames, **forcing a device to disconnect** from the network.  
3. If attackers **continuously send forged frames**, users won’t be able to reconnect. The attack can be directed at a **single target** or **all connected clients**, effectively jamming the network.  
4. Attackers can set up **rogue networks (Evil Twin attack)** mimicking legitimate Wi-Fi access points. This allows them to **monitor traffic**, intercept sensitive data, and perform **Man-in-the-Middle (MITM) attacks**.  

### **Why Deauth Attacks Are Dangerous?**  
- Can **disconnect** users from the internet, causing disruption.  
- Can be used to force users onto **malicious networks** for credential theft.  
- Often used in **Wi-Fi password cracking** (forcing reconnection to capture the handshake).  

### **How to Protect Against Deauth Attacks?**  
- **Use WPA3 encryption** (protects against certain deauth attacks).  
- **Enable 802.11w (Protected Management Frames - PMF)** to secure management frames.  
- **Use a VPN** to encrypt traffic and prevent MITM attacks.  
- **Monitor network traffic** for unusual disconnection patterns.  
- **Avoid connecting to public Wi-Fi** or use **personal hotspots** instead.