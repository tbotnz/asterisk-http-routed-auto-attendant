## Test Account

  ┌──────────────┬──────────────────────────────────────────────┐
  │    Field     │                    Value                     │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Account Name │ Test (or anything)                           │
  ├──────────────┼──────────────────────────────────────────────┤
  │ SIP Server   │ Your machine's IP address (e.g. 192.168.1.x) │
  ├──────────────┼──────────────────────────────────────────────┤
  │ SIP Proxy    │ Leave blank                                  │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Username     │ 6001                                         │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Domain       │ Same as SIP Server (192.168.1.x)             │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Login        │ 6001                                         │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Password     │ test6001pass                                 │
  ├──────────────┼──────────────────────────────────────────────┤
  │ Transport    │ UDP                                          │
  └──────────────┴──────────────────────────────────────────────┘

## Calling the Auto Attendant

Once registered, dial **444** to reach the auto attendant. It picks a random `.wav` file from the `sounds/` directory and plays it back.

| Extension | Purpose |
|-----------|---------|
| 444 | Auto attendant — plays a random WAV file |
| 100 | Echo test — plays back your own audio |

### Adding custom audio

Drop `.wav` files into the `sounds/` directory. Files should be 8kHz, 16-bit, mono for best compatibility. The auto attendant will randomly select one each time extension 444 is called.

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 5060 | UDP/TCP | SIP signaling |
| 10000-10004 | UDP | RTP media (audio) |

Each concurrent call uses 2 RTP ports (audio + RTCP), so 5 ports supports 2 simultaneous calls.

### Expanding the RTP range

To support more concurrent calls, increase the RTP port range in two places:

1. `asterisk-config/rtp.conf` — change `rtpend`:
   ```
   [general]
   rtpstart = 10000
   rtpend = 10019
   ```

2. `docker-compose.yml` — update the port mapping to match:
   ```yaml
   ports:
     - "10000-10019:10000-10019/udp"
   ```

3. If using port forwarding (e.g. VirtualBox), update the forwarding rules to include the new UDP range.

Then restart: `docker compose down && docker compose up -d`