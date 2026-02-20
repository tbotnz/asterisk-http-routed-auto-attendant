# Asterisk HTTP Routed Auto Attendant

## Architecture

```mermaid
graph LR
    subgraph Host
        SIP[SIP Client<br>port 5060] -->|REGISTER / INVITE| AST

        subgraph Docker
            AST[Asterisk<br>PJSIP]
            API[FastAPI<br>port 8000]

            AST -->|ext 444<br>CURL: GET /call/number| API
            API -->|redirect,caller_id| AST
        end
    end

    AST -->|ext 777| C[Chicken Audio]
    AST -->|ext 888| W[Cow Audio]
    AST -->|ext 100| E[Echo Test]
```

```mermaid
sequenceDiagram
    participant C as SIP Client
    participant A as Asterisk
    participant F as FastAPI

    C->>A: INVITE ext 444
    A->>C: Answer + play prompt
    C->>A: DTMF digits (phone number)
    A->>F: GET /call/{phone_number}
    F->>A: redirect,caller_id
    A->>A: Set CALLERID, Goto redirect ext
    A->>C: Play audio (777=chicken, 888=cow)
    A->>C: Hangup

    Note over A,F: On API timeout/error,<br>defaults to ext 888
```

## Setup

```
docker compose up -d --build
```

## Test Account

| Field | Value |
|-------|-------|
| Username | `6001` |
| Password | `test6001pass` |
| Server | Your host IP |
| Transport | UDP |

## Extensions

| Extension | Description |
|-----------|-------------|
| 100 | Echo test |
| 444 | Auto attendant - prompts for phone number, sends to API via HTTP |
| 777 | Plays chicken sound |
| 888 | Plays cow sound |

## API

FastAPI server on port 8000. Source is mounted with auto-reload.

`GET /call/{phone_number}` - called by extension 444 after collecting DTMF input.

## Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 5060 | UDP/TCP | SIP |
| 8000 | TCP | API |
| 10000-10004 | UDP | RTP |

2 RTP ports per call, so 5 ports = 2 concurrent calls.

### Expanding RTP range

1. `asterisk-config/rtp.conf` - change `rtpend`
2. `docker-compose.yml` - update port mapping to match
3. Update port forwarding rules if applicable

### Custom sounds

Drop 8kHz 16-bit mono `.wav` files into `sounds/`.
