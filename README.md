# DisjorkDados

isso é um teste

## ⚠️ IMPORTANT LEGAL NOTICE

This tool is strictly for educational purposes and assisting users in creating servers. It simulates the cloning or restoration of Discord server structures (categories, text/voice/forum/announcement/stage channels, names, customizations, and roles), but it must **NOT** be used on servers without the explicit authorization of their owners.

**Recommendation:** Only test on servers you own or have explicit permission to manage.
Example: your own servers, or with the consent of the owner. In **Manual Mode**, use it to restore lost servers based on information you collected.

---

### Features:

* Stylish **Graphical Interface (GUI)** with two modes:

  * **Bot:** Directly clones a server where the bot has access (source and destination).
  * **Manual:** Manually create or restore the structure using a visual form or JSON (easy for Discord beginners).
* Supports categories, channels, custom names, and roles via **Discord API** (discord.py).
* Authentication via **bot token** (create a bot in the Discord Developer Portal with admin permissions).
* **Rate limiting** to avoid Discord bans.
* Communication via **Redis** for managing cloning/creation queues.
* Export of **metrics** to Grafana (automatic dashboards) and interactive charts with Chart.js.
* **Deploy on Docker or Kubernetes** for scalable simulations.
* Optional: Integration with **AWS S3** for log storage.


---

## 🚀 How to Use

### Clone the repo:

```bash
git clone https://github.com/hygark/disjorkdados.git
```

### Create a bot in Discord Developer Portal:

👉 [https://discord.com/developers](https://discord.com/developers)

* Enable permissions: `Manage Channels`, `Manage Roles`, `View Channels`.
* Add the bot to:

  * **Bot Mode:** source server (read) and destination server (admin).
  * **Manual Mode:** destination server only (admin).
* Get the **bot token** and the **server IDs** (source and destination, if using Bot Mode).

### Setup servers:

* Create a **test server (Test Server)** with categories, channels, and roles.
* Create an **empty backup server (Backup Server)** and add the bot as admin.


## 💻 Local Test (GUI)

```bash
python gui.py
```

### Choose the mode:

* **Bot Mode:** Enter bot token, server IDs (source and destination), clone order, log level, and Grafana API key (optional).

* **Manual Mode:** Enter bot token, destination server ID, and add categories, channels, and roles through the visual form or JSON upload.

---

## ⚠️ Limitations

* **Bot Mode:** Requires bot with permissions in source server (View Channels) and destination server (Manage Channels, Manage Roles).
* **Manual Mode:** Requires user to provide structure (form or JSON).
* **Discord Limits:**

  * Max 50 categories per server.
  * Max 500 channels (text, voice, forum, announcement, stage) per server.
  * Max 250 roles per server.
  * API rate limits (handled by script with delays).
* **Performance:** Limited by host machine. Kubernetes improves scalability.
