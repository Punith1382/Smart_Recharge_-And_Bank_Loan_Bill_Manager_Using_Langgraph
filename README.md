# Smart_Recharge_-And_Bank_Loan_Bill_Manager_Using_Langgraph

# 💳 Smart Recharge & Bank Loan Priority Manager

> **An Intelligent Financial Assistant built with LangGraph** that automatically checks upcoming utility bills (Jio, Airtel) and strictly prioritizes bank loan EMIs/schemes beforehand to avoid credit penalties. Features a **Human-In-The-Loop (HITL)** safeguard before executing payments.

---

## 🏗️ System Architecture & Workflow
                    ┌──────────────────────────────┐
                    │          [ START ]           │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      fetch_due_bills         │
                    │  Queries Jio, Airtel, Bank   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     analyze_priorities       │
                    │  Ranks Debt > Schemes > Utility│
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                   🛑 INTERRUPT BEFORE HUMAN APPROVAL
                                   │
                    ┌──────────────┴───────────────┐
                    │      human_confirmation      │
                    │   User decision: YES / NO    │
                    └──────────────┬───────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
               [ APPROVED ]                [ REJECTED ]
                     │                           │
                    ┌┴───────────────────────────┴┐
                    │      execute_payments       │
                    │ Executes or Cancels Payments │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      send_notification       │
                    │   Prints Receipt & Summary   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │           [ END ]            │
                    └──────────────────────────────┘

---

## ⚡ How It Works (Step-by-Step Flow)

### 1. 🔍 Bill Aggregation (`fetch_due_bills`)
The system connects to simulated biller APIs (Jio Fiber, Airtel Mobile, HDFC Loan EMI, SBI PPF) and retrieves all bills due in the upcoming cycle.

### 2. 🎯 Risk-Aware Prioritization Engine (`analyze_priorities`)
Unlike standard payment apps that treat all bills equally, this system applies a financial risk ranking algorithm:
- **Priority 1 (High Risk / Critical):** Bank Loans, EMIs, Investment Schemes. Missing these leads to late charges and negative CIBIL/FICO credit score impacts[cite: 1].
- **Priority 2 (Standard):** Mobile/Fiber Recharges (Jio, Airtel)[cite: 1]. Missing these only leads to temporary service delays[cite: 1].

### 3. 🛑 Human-In-The-Loop Interrupt (`human_confirmation`)
Using LangGraph's state persistence (`MemorySaver`), execution automatically **freezes** before money is debited[cite: 1]. The system alerts you with high-priority warnings and requests explicit approval (`YES` or `NO`)[cite: 1].

### 4. 💳 Transaction Processing (`execute_payments`)
Depending on your decision:
- **`APPROVED`**: Marks payments as `SUCCESS` with exact transaction timestamps[cite: 1].
- **`REJECTED`**: Safely marks payments as `CANCELLED_BY_USER` without touching your account balance[cite: 1].

### 5. 📲 Notification Dispatch (`send_notification`)
Generates a clean payment audit log summary[cite: 1].

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.10+** installed on your system.

# 🌟 What Makes This Project Special?

This project stands out—especially on a GitHub portfolio or in technical interviews—because it moves beyond simple automation scripts to solve **real-world financial and software architecture challenges** using modern **Agentic AI pattern design**[cite: 1].

---

## 1. 🛡️ Human-in-the-Loop (HITL) Safety Guardrails
* **The Problem:** Fully autonomous financial scripts or AI agents that automatically debit money are risky; a bug, API glitch, or wrong calculation could trigger unauthorized payments.
* **The Solution:** By leveraging **LangGraph execution interrupts** (`interrupt_before`), the workflow runs up to the decision boundary, **freezes state in memory**, and pauses for explicit human authorization (`YES`/`NO`) before touching any funds[cite: 1].
* **Engineering Impact:** Demonstrates a deep understanding of AI safety, state persistence, and risk management in production software[cite: 1].

---

## 2. 🧠 Risk-Aware Financial Prioritization Logic
* **The Problem:** Standard biller apps treat all dues equally—displaying a ₹999 internet recharge right alongside a ₹25,000 Home Loan EMI[cite: 1].
* **The Solution:** The workflow enforces a **financial penalty hierarchy**[cite: 1]:
  1. **Priority 1 (Loans / EMIs / Investments):** High risk[cite: 1]. Defaulting on these incurs heavy financial penalties, late fees, and permanent credit score (CIBIL/FICO) damage[cite: 1].
  2. **Priority 2 (Utility Recharges):** Lower risk[cite: 1]. Missing a Jio or Airtel recharge only results in temporary service suspension[cite: 1].
* The system automatically bubbles critical bank obligations to the top of the processing queue and raises high-priority alerts[cite: 1].

---

## 3. 💾 Stateful Execution Engine (LangGraph State Machine)
* **The Problem:** Traditional Python scripts run top-to-bottom and exit. Pausing a script mid-way for input risks losing context if the process terminates or restarts.
* **The Solution:** Built on LangGraph's `StateGraph` and `MemorySaver` checkpointer[cite: 1]. The centralized state object (`WorkflowState`) acts as a **single source of truth**[cite: 1]. The engine can freeze state, wait indefinitely for an external action (`user_decision`), and resume execution seamlessly from the exact checkpoint[cite: 1].

---

## 4. 📐 Scalable, Enterprise-Grade Architecture
* **Strict Type Safety:** Uses **Pydantic v2** data models and **TypedDict** state schemas to validate inputs prior to graph execution[cite: 1].
* **Decoupled Node Design:** Every phase (`fetch`, `analyze`, `approve`, `execute`, `notify`) operates as an isolated Python node[cite: 1]. This modular structure allows easy integration of real-world services—such as Twilio WhatsApp notifications, UPI payment APIs, or database storage—without altering core workflow logic[cite: 1].

---

### 💡 Summary
Rather than being a basic notification script, this project operates as a **stateful, risk-aware, human-guided financial orchestrator** built with modern backend standards[cite: 1]!
