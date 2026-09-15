"""
Granite.Fit door-command listener
==================================

Run this on your home PC. It watches the `doorCommands` collection in
Firestore for new "pending" commands (written by the web app when the
slider is pulled), performs whatever real-world action you wire up in
`perform_action()`, then writes the result back — which is what the
phone is waiting on to show "Door unlocked" or a failure.

Setup
-----
1.  pip install firebase-admin

2.  In the Firebase console: Project settings (gear icon) → Service
    accounts → "Generate new private key". This downloads a JSON file.
    Save it next to this script as  serviceAccountKey.json

    ⚠️  DO NOT commit that file to a public GitHub repo — it's a full
    admin credential for your Firebase project. Add it to .gitignore
    (already done in this repo's .gitignore) or keep this script
    outside the repo entirely.

3.  Make sure Firestore is enabled for the project (Firebase console →
    Build → Firestore Database → Create database) and that you've
    published the security rules in firestore.rules from this folder.

4.  python door_listener.py

It'll sit there printing "Listening for door commands..." — leave the
window open (or run it as a service / scheduled task) and it'll react
within a second or two of the slider being pulled on the phone.
"""

import time
import traceback

import firebase_admin
from firebase_admin import credentials, firestore

SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
COMMANDS_COLLECTION = "doorCommands"


def perform_action(device: str, action: str) -> tuple[bool, str]:
    """
    This is the bit you actually customise.

    Do whatever the real action is here — trip a relay, hit a local
    API, fire a GPIO pin, whatever your door hardware needs — and
    return (True, "") on success or (False, "some reason") on failure.

    `device` and `action` come straight from what the web app sent,
    e.g. device="main_door", action="unlock", so you can branch on
    them if you end up with more than one door/action.
    """
    print(f"  -> performing action: {action} on {device}")

    # ------------------------------------------------------------
    # EXAMPLE ONLY — replace this with your real hardware/API call.
    # ------------------------------------------------------------
    time.sleep(1)  # pretend it takes a second to actuate
    success = True
    # ------------------------------------------------------------

    if success:
        return True, ""
    return False, "Relay did not confirm"


def handle_new_command(doc_snapshot, db):
    data = doc_snapshot.to_dict()
    if not data or data.get("status") != "pending":
        return

    device = data.get("device", "unknown")
    action = data.get("action", "unknown")
    print(f"New command {doc_snapshot.id}: {action} on {device}")

    try:
        ok, message = perform_action(device, action)
    except Exception as exc:  # noqa: BLE001 - we want to report *any* failure back
        ok, message = False, str(exc)
        traceback.print_exc()

    doc_snapshot.reference.update({
        "status": "success" if ok else "fail",
        "message": message,
        "updatedAt": firestore.SERVER_TIMESTAMP,
    })
    print(f"  -> reported {'success' if ok else 'fail'} for {doc_snapshot.id}")


def main():
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    query = db.collection(COMMANDS_COLLECTION).where("status", "==", "pending")

    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            # ADDED covers new pending docs; MODIFIED can happen if a
            # doc briefly re-matches the query — handle_new_command
            # already checks status=='pending' so this stays safe.
            if change.type.name in ("ADDED", "MODIFIED"):
                handle_new_command(change.document, db)

    query.on_snapshot(on_snapshot)

    print("Listening for door commands... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()