with open('src/App.jsx', 'r') as f:
    content = f.read()

old = '''          <div
            key={s.label}
            style={{
              background: s.accent ? COLORS.clayLight : "#fff",
              border: `1px solid ${s.accent ? COLORS.clay : COLORS.line}`,
              borderRadius: 10,
              padding: "10px 8px",
              textAlign: "center",
            }}
          >
            <div style={{ fontFamily: "Georgia, serif", fontSize: 18, color: s.accent ? COLORS.clay : COLORS.pine, fontWeight: 700 }}>
              {s.value}
            </div>
            <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 0.4, color: COLORS.sage, marginTop: 2 }}>
              {s.label}
            </div>
          </div>'''

new = '''          <div
            key={s.label}
            style={{
              background: s.accent ? COLORS.clayLight : "#fff",
              border: `1px solid ${s.accent ? COLORS.clay : COLORS.line}`,
              borderRadius: 10,
              padding: "10px 8px",
              textAlign: "center",
              minWidth: 0,
            }}
          >
            <div style={{ fontFamily: "Georgia, serif", fontSize: 18, color: s.accent ? COLORS.clay : COLORS.pine, fontWeight: 700 }}>
              {s.value}
            </div>
            <div style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: 0.4, color: COLORS.sage, marginTop: 2, overflowWrap: "break-word" }}>
              {s.label}
            </div>
          </div>'''

if old in content:
    content = content.replace(old, new)
    with open('src/App.jsx', 'w') as f:
        f.write(content)
    print("Stat grid overflow fix applied")
else:
    print("SKIPPED - pattern not found (already applied?)")
