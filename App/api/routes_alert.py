from fastapi import APIRouter, HTTPException, Form
from App.utils import log_alert

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "Voice Auth API is healthy"}

@router.post("/alerts")
def trigger_alert(
    user_id: str = Form(...),
    alert_type: str = Form(...),
    message: str = Form(None)
):
    try:
        log_alert(user_id, alert_type, message)
        return {"message": f"Alert logged for user '{user_id}'", "alert_type": alert_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log alert: {str(e)}")