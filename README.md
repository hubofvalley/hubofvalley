<p align="center">
  <img src="https://github.com/user-attachments/assets/9086aae1-2365-4a74-9c19-00a10a7e618d" alt="Grand Valley banner" width="600" height="300">
</p>

<div align="center">
  <h1>Grand Valley</h1>
  <p><strong>Fervent Proof of Stake Validator</strong></p>
  <p>An independent validator and open-source infrastructure team.<br>We secure networks, write the guides we wish we had, and ship tools that take the pain out of running a node.</p>

  <p>
    <a href="https://grandvalleys.com"><strong>Website</strong></a> ·
    <a href="https://x.com/bacvalley"><strong>X</strong></a> ·
    <a href="https://medium.com/@grandvalley"><strong>Medium</strong></a> ·
    <a href="https://github.com/hubofvalley/Testnet-Guides"><strong>Guides</strong></a> ·
    <a href="mailto:letsbuidltogether@grandvalleys.com"><strong>Contact</strong></a>
  </p>
</div>

---

## 🧭 Find Your Way

| You are | Start with |
|---|---|
| **Choosing a validator** to delegate to | [0G validator profile](https://explorer.0g.ai/app/validators/0x108e619da0cdba8a301a53948a4acc23a3d79377/delegators) · [grandvalleys.com](https://grandvalleys.com) · [Email us](mailto:letsbuidltogether@grandvalleys.com) |
| **Setting up your own node** | [Valley toolkits](#-valley-toolkits) · [Testnet Guides](https://github.com/hubofvalley/Testnet-Guides) · [Mainnet Guides](https://github.com/hubofvalley/Mainnet-Guides) |
| **Bringing a network to life** and need an operator | [Email us](mailto:letsbuidltogether@grandvalleys.com) |

## 🛠️ Our Work

| Focus | How we deliver it |
|---|---|
| **Securing networks** | We operate validators on supported chains. Our mainnet validator profile lives on [0G](https://explorer.0g.ai/app/validators/0x108e619da0cdba8a301a53948a4acc23a3d79377/delegators). |
| **Building tools** | Each *Valley of ...* toolkit is a menu-driven terminal app that installs, upgrades and inspects a node, with snapshots, peers, status and logs a keypress away. |
| **Writing guides** | Hands-on walkthroughs for mainnet and testnet, plus an archive of earlier networks we have supported. |
| **Watching the stack** | Prometheus, Grafana, Loki, Alertmanager, Grafana Alloy, Node Exporter and Blackbox Exporter. |
| **Sharing knowledge** | Explainers and calculators on [grandvalleys.com](https://grandvalleys.com) and [Medium](https://medium.com/@grandvalley). |

## 🔭 Under the Hood

```mermaid
flowchart TB
    subgraph Sources
        direction LR
        H[Host and node metrics]
        E[Public endpoint probes]
        G[Service logs]
    end

    subgraph Collect
        direction LR
        P[(Prometheus)]
        L[(Loki)]
    end

    subgraph Act
        direction LR
        D[Grafana dashboards]
        M[Alertmanager]
    end

    H --> P
    E --> P
    G --> L
    P --> D
    L --> D
    P --> M

    classDef amber fill:#ffc355,stroke:#ff6b00,stroke-width:1px,color:#0a0a0a
    class H,E,G,P,L,D,M amber
```

Metrics, probes and logs land in one place. Dashboards show what is happening, and alert rules decide who hears about it.

## 🌐 Valley Toolkits

Every network gets its own toolkit, with a menu-driven launcher and its own documentation.

| Network | Mainnet | Testnet |
|---|---|---|
| **0G** | [Valley-of-0G-Mainnet](https://github.com/hubofvalley/Valley-of-0G-Mainnet) | [Valley-of-0G-Testnet](https://github.com/hubofvalley/Valley-of-0G-Testnet) |
| **Gno.land** | [Valley-of-Gnoland-Mainnet](https://github.com/hubofvalley/Valley-of-Gnoland-Mainnet) | [Valley-of-Gnoland-Testnet](https://github.com/hubofvalley/Valley-of-Gnoland-Testnet) |
| **Story Protocol** | [Valley-of-Story-Mainnet](https://github.com/hubofvalley/Valley-of-Story-Mainnet) | [Valley-of-Story-Testnet](https://github.com/hubofvalley/Valley-of-Story-Testnet) |
| **Namada** | [Valley-of-Namada-Mainnet](https://github.com/hubofvalley/Valley-of-Namada-Mainnet) | n/a |
| **Limonata** | n/a | [Valley-of-Limonata-Testnet](https://github.com/hubofvalley/Valley-of-Limonata-Testnet) |
| **Worrell** | n/a | [Valley-of-Worrel-Testnet](https://github.com/hubofvalley/Valley-of-Worrel-Testnet) |
| **Tempo** (legacy) | n/a | [Valley-of-Tempo-Testnet](https://github.com/hubofvalley/Valley-of-Tempo-Testnet) |

> A toolkit tells you we maintain tooling and documentation for a network. It does **not** mean Grand Valley sits in that network's active validator set. Check the network's own explorer for that.

**Good habits:** read any script before running it, run it as the regular user that owns the node (never root), keep keys and mnemonics to yourself, and rehearse changes on a non-validator node first.

## 📈 Contribution Pulse

<div align="center">

<img height="215" src="assets/stats.svg" alt="Grand Valley GitHub stats: stars earned, public repositories, pull requests, issues and followers">
<img height="215" src="assets/langs.svg" alt="Most used languages across Grand Valley public repositories">

<img src="assets/streak.svg" alt="Grand Valley contribution streak: total contributions, current streak and longest streak">

</div>

<sub>Generated from public GitHub data by a scheduled workflow in this repository, refreshed daily.</sub>

## 💌 Say Hello

<p align="center">
  <img src="https://github.com/user-attachments/assets/1d786a69-6d92-49b7-99a0-417b3e85f292" alt="Let's Buidl Together" width="800" height="400">
</p>

Thinking of delegating, stuck on a node, or about to launch a testnet and need an operator who has done it before? Drop us a line.

<div align="center">

[**Website**](https://grandvalleys.com) · [**Email**](mailto:letsbuidltogether@grandvalleys.com) · [**X**](https://x.com/bacvalley) · [**Medium**](https://medium.com/@grandvalley) · [**Guides**](https://github.com/hubofvalley/Testnet-Guides)

**Let's Buidl Together**

<img src="assets/wave-footer.svg" alt="" width="100%" height="100">

</div>
