# ssh_decrypt_automation tool

### What is this?

This tool automates the process of dumping multiple iOS apps at once in jailbroken devices

### Disclaimer

- Check out [LICENSE](LICENSE) before using this software.
- **Do not use `Clutch` or `bfdecrypt` for piracy!**
- Please, do not spam NyaMisty with logs of this software
  - **iOS 15 implemented many jailbreak mitigation techniques, dumping apps became 
    harder than it used to be, so do not ask for fixes**
- I'm not responsible for any damage or data lost that could happen for using this software

**You've been warned**


### Compatibility

Tested with:

| Device            | iOS version | Jailbreak       |
|-------------------|-------------|-----------------|
| iPhone XR   (A12) | 15.1        | XinaA15 1.1.6.2 |
| iPad Mini 5 (A12) | 15.1        | XinaA15 1.1.6.2 |

Unfortunately I don't own a checkm8 compatible device on iOS 15
This tool should work with root and rootless jailbreaks (bfdecrypt)

| Operating system            | Python version  |
|-----------------------------|-----------------|
| macOS Monterey 12.5 (ARM64) | 3.9.6           |
| Debian 11           (ARM64) | 3.10.4          |
| Windows 11          (ARM64) | 3.11.2 (x86-64) |

**Note**: At the moment, paramiko is not installable in 
Python3 for ARM in Windows

### Dependencies 

1. [Python](https://www.python.org/downloads/) >= 3.9
   - If you're on Windows, you'll need to add python to PATH under installer options
2. [paramiko](https://pypi.org/project/paramiko/)
3. [Clutch](https://github.com/NyaMisty/Clutch/)
4. [bfdecrypt](https://github.com/fenfenS/bfdecrypt)
   - bfdecrypt requires [libSparkAppList](https://havoc.app/package/libsparkapplist), repo: https://havoc.app/
5. SSH client for your PC and SSH server for your iOS device
   - If you're using XinaA15, make sure to activate
     `open SSH server` under `Option` tab
   - Most Linux distros have an SSH client
   - Windows (10, 11) and macOS includes by default an SSH client

**Notes:**
- You'll need `Clutch` or `bfdecrypt` (both if you want).
- To get `bfdecrypt` to work with iOS 15 (Tested with XinaA15),
  you'll need `libSparkAppList` and [fenfenS' bfdecrypt](https://github.com/fenfenS/bfdecrypt/releases/tag/test)
- If you already have bfdecrypt working (with AppList), it should just work fine

### Usage

- Open your preferred terminal 

- Clone this repo

<pre>
$ git clone https://github.com/cdelaof26/ssh_decrypt_automation_tool.git

# If you don't have git, click "Code" -> "Download ZIP"
</pre>

- Provide a copy of Clutch or bfdecrypt (or both)

<pre>
#   Clutch:
#  * You can skip this if you don't want to use Clutch
#
# Download the latest version from: 
#     https://github.com/NyaMisty/Clutch/releases
# Copy "Clutch_troll" to /path/to/ssh_decrypt_automation_tool

#   bfdecrypt:
#  * You can skip this if you already have bfdecrypt working
#    in your device or you don't want to use bfdecrypt
#
# Download the latest version from: 
#     https://github.com/fenfenS/bfdecrypt/releases
# Copy "com.level3tjg.bfdecrypt.deb" to /path/to/ssh_decrypt_automation_tool
# Rename "com.level3tjg.bfdecrypt.deb" as "bfdecrypt.deb"
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

**Note: Your PC must be connected to the same network**


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


- **I can't find the option to dump apps, where is it?**

1. Connect your Apple device
2. Select `3. Select decrypt utility (needed to decrypt apps)` 
   in the main menu
3. Select your preferred option
   - `Fallback` means that if first option fails, 
      the second one will be used immediately to retry app 
      decryption
4. Done

- **I don't want to enter the IP address, username or password
  each time I use this software, is there any solution?**

Yes:
1. Run the project
2. Connect your idevice
3. Select `S. Setting` on the main menu
4. Enable / disable features as you wish
   - **username and password are saved as plain text!**
5. Done


- **Shall I use `Clutch` or `bfdecrypt`?**

Depends on which works better for you, for me: `bfdecrypt`

| App name  | Clutch  | bfdecrypt |
|-----------|---------|-----------|
| Terraria  | Success | Success   |
| Apollo    | Failed  | Failed    |
| RedditApp | Failed  | Success   |
| WhatsApp  | Failed  | Success   |
| Telegram  | Failed  | Success   |
| Discord   | Failed  | Success   |
| ...       | ...     | ...       |


- **My app keeps failing when dumping, what can I do?**

Unfortunately, there isn't a workaround for those applications,
so maybe ask anyone else if they can dump that app for you

* Alternatively, you can use `bfdecrypt` if `Clutch` fails
  (this might not work as well)

### Changelog

### v0.0.4
- Added support for bfdecrypt
- Fixed _Windows experience_

### v0.0.3
- Minor bug fixes
- Fixed bug where the script couldn't connect (Time out!)
  and it keeps trying until "too many attempts" error is raised
- Fixed bug where the script would crash when attempting 
  to delete temporary data but there isn't a cache directory

### v0.0.2
- Improved app detection

### v0.0.1
- Initial project
