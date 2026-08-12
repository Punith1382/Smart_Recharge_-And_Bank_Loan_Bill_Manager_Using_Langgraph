import datetime
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# ---------------------------------------------------------------------------
# 1. Data Models
# ---------------------------------------------------------------------------
class Bill(BaseModel):
    id: str
    category: str  # "BANK_LOAN", "SCHEME", "RECHARGE"
    provider: str  # "HDFC Loan", "Jio Recharge", "Airtel Fiber", etc.
    amount: float
    due_date: str  # YYYY-MM-DD
    priority: int  # 1 = Highest (Loans/Schemes), 2 = Standard (Recharges)

class WorkflowState(TypedDict):
    user_id: str
    bills: List[Dict[str, Any]]
    priority_alerts: List[str]
    pending_approvals: List[Dict[str, Any]]
    user_decision: Optional[str]  # "APPROVED" or "REJECTED"
    payment_status: List[Dict[str, Any]]

# ---------------------------------------------------------------------------
# 2. Node Functions
# ---------------------------------------------------------------------------
def fetch_due_bills_node(state: WorkflowState) -> Dict[str, Any]:
    """Simulates fetching monthly recharges and bank loans due in the next 7 days."""
    today = datetime.date.today()
    
    mock_bills = [
        {
            "id": "LOAN-101",
            "category": "BANK_LOAN",
            "provider": "HDFC Home Loan EMI",
            "amount": 25000.0,
            "due_date": (today + datetime.timedelta(days=2)).isoformat(),
            "priority": 1
        },
        {
            "id": "RECHARGE-202",
            "category": "RECHARGE",
            "provider": "Jio Fiber Monthly",
            "amount": 999.0,
            "due_date": (today + datetime.timedelta(days=4)).isoformat(),
            "priority": 2
        },
        {
            "id": "SCHEME-303",
            "category": "SCHEME",
            "provider": "SBI PPF / Investment",
            "amount": 5000.0,
            "due_date": (today + datetime.timedelta(days=3)).isoformat(),
            "priority": 1
        }
    ]
    return {"bills": mock_bills}


def analyze_priorities_node(state: WorkflowState) -> Dict[str, Any]:
    """Analyzes upcoming bills and prioritizes bank loans/schemes over utility recharges."""
    bills = state.get("bills", [])
    alerts = []
    pending_approvals = []

    # Sort by priority (1 = Loans/Schemes first) and then by due date
    sorted_bills = sorted(bills, key=lambda x: (x["priority"], x["due_date"]))

    loan_bills = [b for b in sorted_bills if b["category"] in ["BANK_LOAN", "SCHEME"]]

    if loan_bills:
        alerts.append(f"⚠️ HIGH PRIORITY: You have {len(loan_bills)} Bank Loan/Scheme payment(s) due soon!")

    for bill in sorted_bills:
        pending_approvals.append(bill)

    return {
        "priority_alerts": alerts,
        "pending_approvals": pending_approvals
    }


def human_confirmation_node(state: WorkflowState) -> Dict[str, Any]:
    """Acts as a boundary where human approval is requested before debiting funds."""
    return {}


def execute_payments_node(state: WorkflowState) -> Dict[str, Any]:
    """Executes payments if approved, or skips if rejected."""
    decision = state.get("user_decision")
    pending = state.get("pending_approvals", [])
    results = []

    if decision == "APPROVED":
        for bill in pending:
            results.append({
                "bill_id": bill["id"],
                "provider": bill["provider"],
                "amount": bill["amount"],
                "status": "SUCCESS",
                "timestamp": datetime.datetime.now().isoformat()
            })
    else:
        for bill in pending:
            results.append({
                "bill_id": bill["id"],
                "provider": bill["provider"],
                "amount": bill["amount"],
                "status": "CANCELLED_BY_USER",
                "timestamp": datetime.datetime.now().isoformat()
            })

    return {"payment_status": results}


def send_notification_node(state: WorkflowState) -> Dict[str, Any]:
    """Sends final confirmation output to the user."""
    results = state.get("payment_status", [])
    print("\n" + "="*50)
    print("📲 SMART PAYMENT ASSISTANT NOTIFICATION")
    print("="*50)
    
    for item in results:
        status_icon = "✅" if item["status"] == "SUCCESS" else "❌"
        print(f"{status_icon} {item['provider']}: ₹{item['amount']} | Status: {item['status']}")
    
    print("="*50 + "\n")
    return {}

# ---------------------------------------------------------------------------
# 3. LangGraph Construction
# ---------------------------------------------------------------------------
def build_graph():
    builder = StateGraph(WorkflowState)

    builder.add_node("fetch_bills", fetch_due_bills_node)
    builder.add_node("analyze_priorities", analyze_priorities_node)
    builder.add_node("human_confirmation", human_confirmation_node)
    builder.add_node("execute_payments", execute_payments_node)
    builder.add_node("send_notification", send_notification_node)

    builder.add_edge(START, "fetch_bills")
    builder.add_edge("fetch_bills", "analyze_priorities")
    builder.add_edge("analyze_priorities", "human_confirmation")
    builder.add_edge("human_confirmation", "execute_payments")
    builder.add_edge("execute_payments", "send_notification")
    builder.add_edge("send_notification", END)

    memory = MemorySaver()
    
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["human_confirmation"]
    )
    return graph

# ---------------------------------------------------------------------------
# 4. Execution Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = build_graph()
    thread_config = {"configurable": {"thread_id": "user_session_001"}}

    initial_input = {"user_id": "usr_9988"}

    print("🚀 Starting Monthly Smart Bill Check Workflow...\n")
    
    for event in app.stream(initial_input, thread_config, stream_mode="values"):
        if "priority_alerts" in event and event["priority_alerts"]:
            print("ALERT RECEIVED:")
            for alert in event["priority_alerts"]:
                print(f" -> {alert}")

    current_state = app.get_state(thread_config)
    pending_bills = current_state.values.get("pending_approvals", [])

    print("\n--- 📋 PENDING PAYMENT APPROVAL REQUEST ---")
    for b in pending_bills:
        print(f"• [{b['category']}] {b['provider']} - Amount: ₹{b['amount']} | Due Date: {b['due_date']}")

    user_input = input("\nDo you approve these payments? (yes/no): ").strip().lower()
    decision = "APPROVED" if user_input in ["yes", "y"] else "REJECTED"

    app.update_state(thread_config, {"user_decision": decision})
    
    print("\n🔄 Resuming workflow processing...")
    for event in app.stream(None, thread_config, stream_mode="values"):
        pass