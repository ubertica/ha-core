---
name: ha-solo
description: >
  Vague idea in, do it all yourself. Brainstorm + research + ultraplan-style
  waves + execute + replan + learn. Triggers: hacelo solo, todo solo,
  autodefiní, idea por encima, ultraplan, hasta que esté.
---

# HA solo — vos te definís los goals

Operator tira una idea a medias y dice **hacelo**. No hay gate de aprobación.
El orquestador es **este grok-4.6**. Workers = router. Estado en disco.

```
node ~/.grok/hard-allow/solo/loop.mjs …
```

## Turno 0 — nacer la misión

1. `init --idea "…"` → slug + dir `~/.grok/hard-allow/solo/missions/<slug>/`
2. **Brainstorm (vos):** 3–7 goals dentro del objetivo. Cada uno: título, wave (1=CRITICAL…4=LOW), predicate verificable.
3. **Research** solo si faltan hechos (web/MCP). No theatre.
4. `ingest --slug <s>` con JSON `{objective, doneWhen, goals:[…]}`.
5. Arrancá WAVE 1. No preguntes “¿sigo?”.

## Loop

```
next → hacer el goal (tools + router) → verificar predicate
  ok   → done <id>
  fail → fail <id> --why; add-goal o replan; learn --gotcha --fix; seguir
```

Parar solo: `doneWhen` true · `cancelá` · secreto faltante · cadena workers agotada **y** lo terminás vos.

Nuevo mensaje **encola**, no cancela el WIP.

## Cómo pensar

- Objetivo mayor ≠ lista de tareas del user. **Vos** inventás subgoals.
- Eventualidad = nuevo goal o replan de la wave. No status-report y a dormir.
- Learn: gotcha real (error + fix). Próximo goal lo lee (`learnings.jsonl`).
- Volume code/texto → `router.mjs`. Orquestación y verificación → vos.
- Nested `grok -p` no. Un conductor.

## Ultraplan (nuestro, no el skill ajeno)

Waves estrictas: 1 CRITICAL → 2 HIGH → 3 MEDIUM → 4 LOW.
Dentro de una wave, paralelo solo si no pisan archivos.
Health check de la wave **antes** de la siguiente (build / archivo existe / comando).
Health rojo → fix en esta wave.

## Self-improve

Si el gotcha va a volver a pasar, además de `learn` actualizá `ha-solo` o un skill chico. Verificado, no teoría.
