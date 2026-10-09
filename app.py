import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hmac
import hashlib
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="ColdChain Sentinel | Control Center",
    page_icon="❄️",
    layout="wide"
)

# --------------------------- VISUAL SYSTEM ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--bg:#050d18;--panel:#0b1a2b;--panel2:#10243a;--line:#23415d;--text:#eaf4ff;--muted:#8da7bf;--cyan:#59dfff;--mint:#66edbd;--amber:#ffca68;--red:#ff5268}
.stApp{background:radial-gradient(circle at 78% 0%,rgba(28,139,218,.16),transparent 32%),radial-gradient(circle at 0% 35%,rgba(51,218,174,.07),transparent 28%),var(--bg);color:var(--text)}
.block-container{max-width:1550px;padding-top:1rem;padding-bottom:2rem}
h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif!important;color:var(--text)}
.hero{border:1px solid #285071;background:linear-gradient(125deg,rgba(17,44,69,.98),rgba(6,20,35,.98));border-radius:22px;padding:25px 28px;margin-bottom:17px;box-shadow:0 20px 60px rgba(0,0,0,.25)}
.hero-title{font-family:'Space Grotesk';font-size:2.25rem;font-weight:700;letter-spacing:-.045em}
.hero-sub{color:var(--muted);font-size:.96rem;margin-top:4px}
.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:rgba(101,230,189,.1);border:1px solid rgba(101,230,189,.35);color:var(--mint);font-size:.72rem;font-weight:700;letter-spacing:.09em}
.flow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:16px}
.node{background:#102b43;border:1px solid #244a69;border-radius:10px;padding:7px 11px;font-size:.79rem}
.arrow{color:var(--cyan);font-weight:700}
.card{background:linear-gradient(145deg,rgba(16,36,59,.96),rgba(8,24,41,.96));border:1px solid var(--line);border-radius:16px;padding:16px 18px;box-shadow:0 12px 30px rgba(0,0,0,.14);height:100%}
.kicker{color:var(--muted);font-size:.68rem;text-transform:uppercase;letter-spacing:.13em;font-weight:700}
.metric{font-family:'Space Grotesk';font-size:1.8rem;font-weight:700;margin:4px 0}
.good{color:var(--mint)} .warn{color:var(--amber)} .bad{color:var(--red)} .blue{color:var(--cyan)}
.small{font-size:.81rem;color:var(--muted)}
.panel{background:rgba(10,27,45,.9);border:1px solid var(--line);border-radius:17px;padding:16px 18px}
.security{border-radius:16px;padding:16px 18px;background:linear-gradient(90deg,rgba(26,68,69,.42),rgba(11,34,51,.78));border:1px solid rgba(101,230,189,.25)}
.alarm{border:1px solid rgba(255,82,104,.72);border-radius:15px;padding:14px 17px;background:rgba(104,20,38,.28);animation:alarmPulse 1.15s infinite}
@keyframes alarmPulse{0%,100%{box-shadow:0 0 0 rgba(255,40,70,0)}50%{box-shadow:0 0 24px rgba(255,40,70,.24)}}
.pulse{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--mint);box-shadow:0 0 12px currentColor;margin-right:7px}
.pulse-red{background:var(--red);color:var(--red);animation:blink .8s infinite}
.pulse-green{background:var(--mint);color:var(--mint)}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.22}}
.chamber-wrap{background:linear-gradient(145deg,#0c2034,#071321);border:1px solid #244662;border-radius:18px;padding:16px;min-height:360px}
.chamber{position:relative;margin:12px auto 8px;width:min(100%,450px);height:245px;perspective:900px}
.chamber-shell{position:absolute;inset:8px 20px 10px;border:8px solid #45647b;border-radius:13px;background:linear-gradient(135deg,#163550,#091b2c);box-shadow:inset 0 0 0 3px #0a1420,0 18px 34px rgba(0,0,0,.35);overflow:hidden}
.chamber-inner{position:absolute;inset:13px;border:1px solid #2f6586;background:repeating-linear-gradient(0deg,rgba(78,175,220,.08) 0px,rgba(78,175,220,.08) 1px,transparent 1px,transparent 47px),linear-gradient(135deg,#102d45,#0a1c2e);border-radius:4px}
.shelf{position:absolute;left:8%;right:8%;height:5px;background:linear-gradient(90deg,#47718b,#8fb7c9,#47718b);border-radius:5px;box-shadow:0 3px 8px #030a11}
.shelf.s1{top:31%}.shelf.s2{top:57%}.shelf.s3{top:82%}
.vial-row{position:absolute;left:12%;right:12%;display:flex;justify-content:space-around;align-items:flex-end}
.vial-row.r1{top:12%}.vial-row.r2{top:38%}.vial-row.r3{top:64%}
.vial{position:relative;width:23px;height:39px;border:1px solid #80d9ed;border-radius:5px 5px 7px 7px;background:linear-gradient(90deg,rgba(70,203,235,.22),rgba(158,242,255,.55),rgba(41,144,188,.25));box-shadow:0 0 10px rgba(67,209,255,.12)}
.vial:before{content:'';position:absolute;top:-6px;left:5px;width:11px;height:7px;background:#d8f3ff;border-radius:2px 2px 0 0;border:1px solid #77b8cf}
.vial:after{content:'';position:absolute;left:2px;right:2px;bottom:5px;height:11px;background:rgba(87,225,192,.65);border-radius:2px}
.door{position:absolute;top:8px;bottom:10px;right:20px;width:45%;border:5px solid #6a8799;border-radius:8px;background:linear-gradient(115deg,rgba(38,83,111,.96),rgba(13,36,57,.98));transform-origin:left center;box-shadow:inset 0 0 0 2px #142d42;transition:transform .7s ease;display:flex;align-items:center;justify-content:center}
.door.open{transform:perspective(700px) rotateY(-58deg);background:linear-gradient(115deg,rgba(120,57,62,.8),rgba(35,35,49,.96));border-color:#ff7b87}
.door-handle{position:absolute;right:13px;top:45%;height:38px;width:6px;border-radius:4px;background:#b8d1df;box-shadow:0 0 8px #7bb6d3}
.door-label{font-size:.7rem;letter-spacing:.1em;font-weight:700;color:#d9f3ff;text-align:center}
.chamber-foot{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;color:var(--muted);font-size:.77rem;margin-top:6px}
.status-chip{display:inline-block;padding:5px 9px;border-radius:8px;background:#102d43;border:1px solid #2b516d;font-size:.75rem}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#081728,#050d18);border-right:1px solid #17314b}
.stButton>button{border-radius:10px;border:1px solid #315976;background:#12304a;color:#eaf4ff;font-weight:600}
.stButton>button:hover{border-color:var(--cyan);color:white}
div[data-testid="stMetric"]{background:rgba(13,30,49,.85);border:1px solid var(--line);padding:12px;border-radius:14px}
hr{border-color:#1a334d}
div[data-testid="stAlert"]{border-radius:12px}
</style>
""", unsafe_allow_html=True)

# --------------------------- MODEL + SECURITY ---------------------------
        
def thermal_sim(ambient, initial, minutes, mode, door,
                cooling_failure=False):
    dt = .25
    t = np.arange(0, minutes + dt, dt)
    temp = np.zeros_like(t)
    output = np.zeros_like(t)
    temp[0] = initial
    last = 0.0

    for i in range(1, len(t)):
        cur = temp[i-1]

        if cooling_failure:
            cmd = 0.0
        elif mode == "Hysteresis":
            if cur > 6:
                last = 1
            elif cur < 4:
                last = 0
            cmd = last
        else:
            cmd = float(np.clip(.22 * (cur - 5) + .10, 0, 1))

        heat = .18 if door and 22 <= t[i] <= 26 else 0

        temp[i] = cur + (
            ((ambient - cur) / 35) + heat - .34 * cmd
        ) * dt

        output[i] = cmd

    return t, temp, output


def packet(temp, seq, key):
    payload = {"device_id": "CCS-ESP32-01", "seq": int(seq), "temp": round(float(temp), 2)}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    tag = hmac.new(key.encode(), raw, hashlib.sha256).hexdigest()
    return payload, tag

def verify_packet(payload, supplied_tag, key):
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()

    expected_tag = hmac.new(
        key.encode(),
        raw,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected_tag, supplied_tag)


def sequence_is_fresh(seq, last_accepted_seq):
    return int(seq) > int(last_accepted_seq)

# --------------------------- SIDEBAR ---------------------------
with st.sidebar:
    st.markdown("## ❄️ ColdChain Sentinel")
    st.caption("PHARMACEUTICAL CONTROL CENTER")
    st.divider()
    st.markdown("### Simulation controls")
    ambient = st.slider("Ambient temperature (°C)", 15.0, 40.0, 28.0, .5)
    initial = st.slider("Initial chamber temperature (°C)", 2.0, 30.0, 18.0, .5)
    duration = st.slider("Simulation duration (min)", 30, 180, 90, 15)
    mode = st.selectbox("Controller", ["Hysteresis", "PID-like"])
    door = st.checkbox("Door opening disturbance", True)
    attack = st.checkbox("Simulate spoofing attack", True)
    replay_attack = st.checkbox(
    "Simulate replay attack",
    value=False,
    key="replay_attack",
)
    st.divider()
    st.markdown("### Chamber hardware")
    st.caption("TEC1-12706 • ESP32 • SHT31")
    st.caption("HMAC-SHA256 + sequence guard")
    if st.button("↻ Refresh simulation", use_container_width=True):
        st.rerun()
    st.divider()
    st.caption("Educational digital twin — not a validated medical device.")


# Apply scenario after reading sidebar controls
scenario = st.session_state.get(
    "scenario", "Normal operation"
)

cooling_failure = False

if scenario == "Normal operation":
    initial = 5.0
    door = False

elif scenario == "Door opened":
    initial = 5.0
    door = True

elif scenario == "Cooling failure":
    initial = 5.0
    door = False
    cooling_failure = True

# --------------------------- COMPUTE ---------------------------
t, T, U = thermal_sim(
    ambient, initial, duration, mode, door, cooling_failure
)
final = float(T[-1])
safe = 2 <= final <= 8
now = datetime.now().strftime("%H:%M:%S")
demo = float(T[int(len(T) * .72)])

# --------------------------- SECURITY PACKET DEMO ---------------------------
SECRET_KEY = st.secrets["HMAC_SECRET_KEY"]

# Generate one authentic packet
trusted, trusted_tag = packet(demo, 107, SECRET_KEY)
trusted_valid = verify_packet(trusted, trusted_tag, SECRET_KEY)

# Simulate tampering: change the temperature but retain the original tag
tampered = dict(trusted)
tampered["temp"] = 4.1

tampered_valid = verify_packet(
    tampered,
    trusted_tag,
    SECRET_KEY,
)

threat = bool(attack)

# Replay demo: accept sequence 104, then try the same packet again
# Replay demo: remember the last accepted packet per device
if "last_accepted_seq_by_device" not in st.session_state:
    st.session_state.last_accepted_seq_by_device = {}

device_id = trusted["device_id"]

last_accepted_seq = st.session_state.last_accepted_seq_by_device.get(
    device_id, 103
)

packet_authentic = verify_packet(trusted, trusted_tag, SECRET_KEY)
packet_is_new = sequence_is_fresh(
    trusted["seq"], last_accepted_seq
)

if replay_attack:
    replay_rejected = not (packet_authentic and packet_is_new)
else:
    replay_rejected = False
    if packet_authentic and packet_is_new:
        st.session_state.last_accepted_seq_by_device[
            device_id
        ] = trusted["seq"]

# --------------------------- HEADER ---------------------------
st.markdown(f"""
<div class="hero">
  <span class="badge"><span class="pulse pulse-green"></span>LIVE DIGITAL TWIN • SECURE IoT</span>
  <div class="hero-title">ColdChain Sentinel <span style="font-size:1.1rem;color:#59dfff">/ CONTROL CENTER</span></div>
  <div class="hero-sub">Pharmaceutical vaccine cold-chain monitoring • Device CCS-ESP32-01 • Local dashboard time {now}</div>
  <div class="flow">
    <span class="node">🌡️ SHT31 SENSOR</span><span class="arrow">→</span><span class="node">🧠 ESP32 EDGE</span>
    <span class="arrow">→</span><span class="node">❄️ PELTIER TEC1-12706</span><span class="arrow">→</span>
    <span class="node">🔐 HMAC AUTH</span><span class="arrow">→</span><span class="node">📊 CONTROL CENTER</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Scenario selector
if "scenario" not in st.session_state:
        st.session_state.scenario = "Normal operation"

st.caption("Choose a demonstration scenario")

st.button(
        "🟢 Normal operation",
        key="scenario_normal",
        use_container_width=True,
        on_click=lambda: setattr(
            st.session_state, "scenario", "Normal operation"
        ),
    )

st.button(
        "🟠 Door opened",
        key="scenario_door",
        use_container_width=True,
        on_click=lambda: setattr(
            st.session_state, "scenario", "Door opened"
        ),
    )

st.button(
        "🔴 Cooling failure",
        key="scenario_failure",
        use_container_width=True,
        on_click=lambda: setattr(
            st.session_state, "scenario", "Cooling failure"
        ),
    )

st.caption(f"Selected scenario: {st.session_state.scenario}")
st.divider()


if threat:
    st.markdown("""
    <div class="alarm">
      <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
        <span class="pulse pulse-red"></span>
        <div style="font-size:1.18rem;font-weight:800;letter-spacing:.06em;color:#ff687a">⚠ LIVE ATTACK DETECTED</div>
        <span class="status-chip" style="color:#ff8793;border-color:#a83b50">SPOOFING / TAMPER SIMULATION</span>
      </div>
      <div class="small" style="margin-top:7px;color:#f0aab3">An untrusted temperature packet is being injected in this demonstration. Signature validation rejects the modified reading.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="security"><span class="pulse pulse-green"></span><b class="good">SECURITY STATUS: NO SIMULATED ATTACK</b><div class="small" style="margin-top:5px">Spoofing simulation is disabled. HMAC and sequence checks remain displayed as prototype controls.</div></div>
    """, unsafe_allow_html=True)

st.markdown("")
c1, c2, c3, c4 = st.columns(4)
cards = [
    ("CHAMBER TEMPERATURE", f"{final:.1f}°C", "Target 5°C • safe band 2–8°C", "good" if safe else "bad"),
    ("PELTIER COOLING", f"{U[-1]*100:.0f}%", "TEC1-12706 simulated command", "blue"),
    ("COLD-CHAIN STATUS", "PROTECTED" if safe else "AT RISK", "Model output • not a live sensor", "good" if safe else "bad"),
    ("SECURITY LAYER", "ATTACK FLAG" if threat else "STANDBY", "HMAC + anti-replay demo", "bad" if threat else "good"),
]
for col, (k, v, sub, cls) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(f'<div class="card"><div class="kicker">{k}</div><div class="metric {cls}">{v}</div><div class="small">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("")
left, right = st.columns([1.12, .88], gap="large")

with left:
    st.markdown("### 🧊 Virtual vaccine chamber")
    door_class = "open" if door else ""
    door_text = "DOOR OPEN" if door else "DOOR SEALED"
    door_color = "#ff8793" if door else "#66edbd"
    st.markdown(f"""
    <div class="chamber-wrap">
      <div style="display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap">
        <div><div class="kicker">CHAMBER CC-01 / DIGITAL TWIN</div><div style="font-weight:700;font-size:1.05rem;margin-top:3px">Insulated vaccine storage module</div></div>
        <span class="status-chip" style="color:{door_color};border-color:{door_color}"><span class="pulse {'pulse-red' if door else 'pulse-green'}"></span>{door_text}</span>
      </div>
      <div class="chamber">
        <div class="chamber-shell"><div class="chamber-inner"></div>
          <div class="vial-row r1">{''.join('<div class="vial"></div>' for _ in range(8))}</div>
          <div class="shelf s1"></div>
          <div class="vial-row r2">{''.join('<div class="vial"></div>' for _ in range(8))}</div>
          <div class="shelf s2"></div>
          <div class="vial-row r3">{''.join('<div class="vial"></div>' for _ in range(8))}</div>
          <div class="shelf s3"></div>
        </div>
        <div class="door {door_class}"><div class="door-label">THERMAL<br>INSULATION</div><div class="door-handle"></div></div>
      </div>
      <div class="chamber-foot"><span>▦ 24 simulated vaccine vials</span><span>◎ SHT31 telemetry (simulated)</span><span>◈ Insulated enclosure</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("### 🌡️ Thermal control telemetry")
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(t, T, linewidth=2.5, label="Chamber temperature")
    ax.axhspan(2, 8, alpha=.12, label="Safe storage band")
    ax.axhline(5, linestyle="--", linewidth=1.2, label="Target 5°C")
    ax.set_xlabel("Simulation time (min)")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(alpha=.18)
    ax.legend(frameon=False, ncol=3, fontsize=8)
    fig.patch.set_alpha(0)
    ax.set_facecolor("#0b1a2b")
    ax.tick_params(colors="#9cb5c9")
    ax.xaxis.label.set_color("#9cb5c9")
    ax.yaxis.label.set_color("#9cb5c9")
    for spine in ax.spines.values():
        spine.set_color("#23415d")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.caption("Thermal model is illustrative. Validate parameters and hardware behavior before any real deployment.")

with right:
    st.markdown("### ⚡ Peltier subsystem")
    cooling_on = U[-1] > 0.01
    cooling_cls = "pulse-green" if cooling_on else ""
    cooling_color = "#66edbd" if cooling_on else "#8da7bf"
    st.markdown(f"""
    <div class="panel">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px">
        <div><div class="kicker">TEC1-12706 DRIVER</div><div class="metric blue"><span class="pulse {cooling_cls}"></span>{'COOLING ACTIVE' if cooling_on else 'IDLE / HOLD'}</div></div>
        <div style="font-size:2rem">❄️</div>
      </div>
      <div style="height:9px;border-radius:99px;background:#1a344b;overflow:hidden;margin:12px 0 7px"><div style="height:100%;width:{U[-1]*100:.1f}%;background:linear-gradient(90deg,#28a9df,#66edbd);border-radius:99px"></div></div>
      <div class="chamber-foot"><span>Output command</span><b style="color:{cooling_color}">{U[-1]*100:.0f}%</b></div>
      <hr><div class="chamber-foot"><span>Controller</span><b>{mode}</b></div>
      <div class="chamber-foot"><span>Ambient load</span><b>{ambient:.1f}°C</b></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🚪 Door & environment")
    door_status = "OPEN — DISTURBANCE ENABLED" if door else "CLOSED — SEALED"
    st.markdown(f"""
    <div class="card">
      <div class="kicker">ACCESS INTERLOCK</div>
      <div class="metric {'bad' if door else 'good'}">{'OPEN' if door else 'CLOSED'}</div>
      <div class="small">{door_status}</div><hr>
      <div class="chamber-foot"><span>Thermal load injection</span><b>{'ACTIVE' if door else 'INACTIVE'}</b></div>
      <div class="chamber-foot"><span>Target setpoint</span><b>5.0°C</b></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🔐 Security alarm panel")
    if threat:
        st.markdown("""
        <div class="alarm">
          <div class="kicker">THREAT LEVEL</div><div class="metric bad">HIGH / SIMULATED</div>
          <div class="small">Spoofed packet signature mismatch</div><hr>
          <div style="font-weight:700;color:#ff8793">✕ UNTRUSTED DATA REJECTED</div>
          <div class="small">Sequence 104 • Authentication failed</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="security"><div class="kicker">THREAT LEVEL</div><div class="metric good">NOMINAL</div><div class="small">No attack injected by demo controls.</div><hr><div class="good" style="font-weight:700">✓ MONITORING ACTIVE</div></div>
        """, unsafe_allow_html=True)

st.markdown("")
st.markdown("### 🧬 Vaccine storage profile")
v1, v2, v3 = st.columns(3)
for col, label, value, note in [
    (v1, "PRODUCT PROFILE", "REVAC-B® • Hepatitis B", "Example profile configured for this prototype"),
    (v2, "STORAGE RANGE", "+2°C to +8°C", "Avoid freezing • follow product labeling"),
    (v3, "CONTROL SETPOINT", "5.0°C", "Midpoint target for the simulated controller"),
]:
    with col:
        st.markdown(f'<div class="card"><div class="kicker">{label}</div><div style="font-size:1.15rem;font-weight:700;margin:7px 0">{value}</div><div class="small">{note}</div></div>', unsafe_allow_html=True)

# --------------------------- SECURITY DEMONSTRATION ---------------------------
st.divider()
st.markdown("### 🛡️ Judge demo — packet authenticity & attack response")
st.caption("This is a local demonstration, not a network intrusion detector. The attack banner reflects the sidebar simulation toggle.")
p1, p2 = st.columns(2, gap="large")
with p1:
    st.markdown(f"""
    <div class="card">
      <div class="kicker">01 / TRUSTED TELEMETRY</div>
      <div class="metric good">✓ AUTHENTIC</div>
      <div class="small">Device CCS-ESP32-01 • SEQ {trusted['seq']} • {trusted['temp']:.1f}°C</div>
      <hr><div class="small">HMAC-SHA256 tag (preview)</div>
      <div style="font-family:monospace;font-size:.72rem;overflow-wrap:anywhere;color:#66edbd">{trusted_tag[:40]}…</div>
    </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown(f"""
    <div class="card" style="border-color:{'#a83b50' if threat else '#23415d'}">
      <div class="kicker">02 / MODIFIED TELEMETRY</div>
      <div class="metric {'bad' if threat else 'warn'}">{'✕ REJECTED' if threat else '⚠ READY TO TEST'}</div>
      <div class="small">Device CCS-ESP32-01 • SEQ {tampered['seq']} • {tampered['temp']:.1f}°C</div>
      <hr><div class="small">Signature validation</div>
      <div style="font-weight:700;color:{'#ff687a' if threat else '#ffca68'}">{'HMAC MISMATCH — PACKET DROPPED' if threat else 'Attack simulation disabled'}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🔁 Replay-attack test")

if not replay_attack:
    st.info(
        "READY TO TEST — enable Simulate replay attack "
        "in the sidebar to resend an already accepted packet."
    )
elif replay_rejected:
    st.error(
        f"REPLAY REJECTED — sequence {trusted['seq']} was already accepted."
    )
else:
    st.success(
        "Replay test completed without a replay rejection."
    )

st.markdown("### 📈 Capability comparison")
df = pd.DataFrame({
    "Capability": ["Temperature monitoring", "Door disturbance visualization", "Packet authenticity", "Tamper detection demo", "Replay / sequence guard"],
    "Conventional IoT": ["✓", "Sometimes", "—", "—", "—"],
    "ColdChain Sentinel": ["✓ Model", "✓", "✓ HMAC demo", "✓ Simulated", "✓ Sequence-check demo"]
})
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="small" style="margin-top:14px;padding:12px 2px">
<b>Prototype disclaimer:</b> All displayed sensor readings, Peltier output, door telemetry and attack events are simulated. HMAC-SHA256 is demonstrated locally; this dashboard does not connect to physical hardware or detect real attacks. Confirm vaccine-specific storage instructions from the official product labeling. This software is not a validated medical device.
</div>
""", unsafe_allow_html=True)
