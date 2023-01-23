# ssh_decrypt_automation tool

### What is this?

This tool is meant to dump multiple iOS apps at once on jailbroken devices

### Disclaimer

- Check out [LICENSE](LICENSE) before using this software.
- **Do not use `Clutch` for piracy!**
- Please, do not spam NyaMisty with logs of this software
  - **iOS 15 implemented many jailbreak mitigation techniques, dumping apps became 
    harder than it used to be, so do not ask for fixes**
- I'm not responsible for any damage or data lost that could happen if:
  - Clutch executable is compromised
  - Your ssh credentials are stolen

**You've been warned**


### Compatibility

Tested with:

| Device            | iOS version | Jailbreak       |
|-------------------|-------------|-----------------|
| iPhone XR   (A12) | 15.1        | XinaA15 1.1.6.2 |
| iPad Mini 5 (A12) | 15.1        | XinaA15 1.1.6.2 |

Unfortunately I don't own a checkm8 compatible device on iOS 15

| Operating system            | Python version |
|-----------------------------|----------------|
| macOS Monterey 12.5 (ARM64) | 3.9.6          |
| Debian 11           (ARM64) | 3.10.4         |

I can't test Windows, but it should work let me know 
if you run into any issues.

### Dependencies 

1. [Python](https://www.python.org/downloads/) >= 3.9
2. [paramiko](https://pypi.org/project/paramiko/)
3. [Clutch](https://github.com/NyaMisty/Clutch/)
4. SSH client for your PC and SSH server for your iOS device
   - If you're using XinaA15, make sure to activate
     `open SSH server` under `Option` tab
   - Most Linux distros have an SSH client
   - Windows (10, 11) and macOS includes by default an SSH client


### Usage

- Open your preferred terminal 

- Clone this repo

<pre>
$ git clone https://github.com/cdelaof26/ssh_decrypt_automation_tool.git
</pre>

- Provide a copy of Clutch

<pre>
# Download the latest version from: 
#     https://github.com/NyaMisty/Clutch/releases
# Copy Clutch_troll to /path/to/ssh_decrypt_automation_tool
</pre>

- Move into project directory

<pre>
$ cd ssh_decrypt_automation_tool
</pre>

- Install dependencies
<pre>
# You might need elevated privileges!

$ pip install -r requirements.txt
# or
$ pip3 install -r requirements.txt
</pre>

Run using python

<pre>
# If you're on Linux or macOS
$ python3 main.py

# If you're on Windows
$ python main.py
</pre>


### FAQ

- **How do I find my iOS device IP?**
1. Open settings
2. Go to Wi-FI section
3. Click on the `i` icon of your Wi-Fi network
4. Under `IPV4 ADDRESS` section, copy `IP ADDRESS` field
5. Done

- **I keep getting "Please, consider changing ssh default password!" message,
  how do I change root password?**
1. Open your preferred terminal
2. Run: `ssh root@<your_ios_device_ip>`
   - e.g: `ssh root@10.0.1.5`
3. Enter `alpine` as password
4. Run: `passwd`
5. Enter your password
   - You won't see anything, it's normal
   - Write your new password and then press enter
6. Confirm your password
7. Done

- **I don't want to enter the IP address, username or password
  each time I use this software, is there any solution?**

Yes:
1. Run the project
2. Connect your idevice
3. Select `S. Setting` on the main menu
4. Enable / disable features as you wish
   - **username and password are saved as plain text!**
5. Done

- **My app keeps failing when dumping, what can I do?**

Unfortunately, there isn't a workaround for those applications,
so maybe ask anyone else if they can dump that app for you

### Changelog

### v0.0.2
- Improved app detection

### v0.0.1
- Initial project
