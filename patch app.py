import re

with open('src/App.jsx', 'r') as f:
    content = f.read()

changes = 0

# 1. Button: add boxSizing so width:100% buttons don't overflow the screen
old1 = '''  const base = {
    fontFamily: "inherit",
    fontSize: 14,
    fontWeight: 600,
    padding: "9px 16px",
    borderRadius: 8,
    border: "1px solid transparent",
    cursor: "pointer",
    transition: "transform 0.08s ease, opacity 0.15s ease",
  };'''
new1 = '''  const base = {
    fontFamily: "inherit",
    fontSize: 14,
    fontWeight: 600,
    padding: "9px 16px",
    borderRadius: 8,
    border: "1px solid transparent",
    cursor: "pointer",
    boxSizing: "border-box",
    transition: "transform 0.08s ease, opacity 0.15s ease",
  };'''
if old1 in content:
    content = content.replace(old1, new1)
    changes += 1
    print("[1/4] Button boxSizing fix applied")
else:
    print("[1/4] SKIPPED - pattern not found (already applied?)")

# 2. Color: primary teal to #006D6F
old2 = 'pine: "#3D5A5E",     // dusty deep teal — primary color'
new2 = 'pine: "#006D6F",     // primary teal — brand color'
if old2 in content:
    content = content.replace(old2, new2)
    changes += 1
    print("[2/4] Color updated to #006D6F")
else:
    print("[2/4] SKIPPED - pattern not found (already applied?)")

# 3. Insert AccountSettingsModal before OwnerLoginGate
old3 = 'function OwnerLoginGate({ onLoggedIn }) {'
new3 = '''function AccountSettingsModal({ ownerToken, onClose }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newEmail, setNewEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!newEmail.trim() && !newPassword) {
      setError("Enter a new email and/or a new password to change.");
      return;
    }
    if (newPassword && newPassword !== confirmPassword) {
      setError("New passwords don't match.");
      return;
    }

    setBusy(true);
    try {
      await api.ownerUpdateAccount(ownerToken, {
        currentPassword,
        newEmail: newEmail.trim() || undefined,
        newPassword: newPassword || undefined,
      });
      setSuccess(true);
    } catch (err) {
      setError(err.message || "Something went wrong — try again.");
    } finally {
      setBusy(false);
    }
  }

  if (success) {
    return (
      <Modal title="Account updated" onClose={onClose}>
        <p style={{ fontSize: 14, color: COLORS.pine, lineHeight: 1.6 }}>
          Your account details have been updated. Use your new email and/or password next time you sign in.
        </p>
        <Button onClick={onClose} style={{ marginTop: 8 }}>Done</Button>
      </Modal>
    );
  }

  return (
    <Modal title="Account settings" onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <Field label="Current password (required to confirm)">
          <input
            type="password"
            style={inputStyle}
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
            autoFocus
          />
        </Field>
        <Field label="New email (leave blank to keep current)">
          <input
            type="email"
            style={inputStyle}
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
          />
        </Field>
        <Field label="New password (leave blank to keep current)">
          <input
            type="password"
            style={inputStyle}
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            minLength={8}
          />
        </Field>
        {newPassword && (
          <Field label="Confirm new password">
            <input
              type="password"
              style={inputStyle}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </Field>
        )}
        {error && <div style={{ fontSize: 12, color: COLORS.clay, marginBottom: 10 }}>{error}</div>}
        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <Button type="submit">{busy ? "Saving…" : "Save changes"}</Button>
          <Button variant="ghost" onClick={onClose}>Cancel</Button>
        </div>
      </form>
    </Modal>
  );
}

function OwnerLoginGate({ onLoggedIn }) {'''
if old3 in content:
    content = content.replace(old3, new3)
    changes += 1
    print("[3/4] AccountSettingsModal inserted")
else:
    print("[3/4] SKIPPED - pattern not found (already applied?)")

# 4. Add state variable + wire in Account settings button and modal
old4a = '  const [ownerToken, setOwnerToken] = useState(null); // in-memory only; lost on refresh by design for now'
new4a = '''  const [ownerToken, setOwnerToken] = useState(null); // in-memory only; lost on refresh by design for now
  const [showAccountSettings, setShowAccountSettings] = useState(false);'''
old4b = '''              <div style={{ textAlign: "center", marginTop: 30 }}>
                <button
                  onClick={() => { setOwnerToken(null); setLoaded(false); }}
                  style={{ background: "none", border: "none", color: COLORS.sage, fontSize: 12, cursor: "pointer" }}
                >
                  Sign out
                </button>
              </div>'''
new4b = '''              <div style={{ textAlign: "center", marginTop: 30, display: "flex", justifyContent: "center", gap: 16 }}>
                <button
                  onClick={() => setShowAccountSettings(true)}
                  style={{ background: "none", border: "none", color: COLORS.sage, fontSize: 12, cursor: "pointer" }}
                >
                  Account settings
                </button>
                <button
                  onClick={() => { setOwnerToken(null); setLoaded(false); }}
                  style={{ background: "none", border: "none", color: COLORS.sage, fontSize: 12, cursor: "pointer" }}
                >
                  Sign out
                </button>
              </div>
              {showAccountSettings && (
                <AccountSettingsModal ownerToken={ownerToken} onClose={() => setShowAccountSettings(false)} />
              )}'''
if old4a in content and old4b in content:
    content = content.replace(old4a, new4a)
    content = content.replace(old4b, new4b)
    changes += 1
    print("[4/4] Account settings wired into UI")
else:
    print("[4/4] SKIPPED - pattern not found (already applied?)")

with open('src/App.jsx', 'w') as f:
    f.write(content)

print(f"\nDone — {changes}/4 changes applied.")
