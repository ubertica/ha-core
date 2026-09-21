# BUILD-SPEC — ha-payments

PURPOSE: Cash-in/out rails, sandbox PSP, signed webhooks for CORE-SURFACE writes (W2–W4).
PREFIX: pay
MODE: domain-runtime (not forge)
LANES: rails, psp, webhooks, qa, test, dev, sync, lead
OUT: $PUMAPAY_OUT/payments
IMPLEMENTER: ha-ppdev
PROFILE: FINTECH-BUILD
FLAGS: PUMAPAY_LIVE_PSP, PUMAPAY_MONEY_WRITES, PUMAPAY_DESTRUCTIVE_MIGRATE
