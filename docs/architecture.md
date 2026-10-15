# Architecture

```text
Log source -> Ingestion API -> Feature extraction -> Isolation Forest score
                                           |                 |
                                           +-------> Policy recommendation
                                                             |
                                      monitor / investigate / propose_block
                                                             |
                                                   Employee review (required)
                                                      /             \\
                                                  reject           approve
                                                    |                 |
                                                audit only     simulated block list
                                                                    |
                                                              audit trail
```

## Learning loop

1. Detector produces a score, not a verdict.
2. Policy maps score and prior review outcomes to a recommendation.
3. Employee records approve/reject plus a reason and ticket.
4. Feedback updates recommendation statistics.
5. Periodically evaluate policy behavior on reviewed examples before any rollout.

The demo uses aggregate feedback by risk band, not a full deep-RL agent. This is intentional: decisions are high-impact and should be explainable and bounded. Never let a learned policy directly execute a real block.
