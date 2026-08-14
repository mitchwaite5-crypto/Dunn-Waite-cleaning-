with open('index.html', 'r') as f:
    content = f.read()

old = '''    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="Dunn & Waite" />
    <title>Dunn &amp; Waite Cleaning Co.</title>
  </head>'''
new = '''    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="Dunn & Waite" />
    <title>Dunn &amp; Waite Cleaning Co.</title>
    <style>
      /* Global reset: without this, buttons/inputs set to width:100% overflow
         past the screen edge because padding/border get added on top of that
         100% instead of fitting inside it (browser default is content-box). */
      *, *::before, *::after {
        box-sizing: border-box;
      }
      html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        overflow-x: hidden;
      }
      #root {
        width: 100%;
      }
    </style>
  </head>'''

if old in content:
    content = content.replace(old, new)
    with open('index.html', 'w') as f:
        f.write(content)
    print("index.html patched successfully")
else:
    print("SKIPPED - pattern not found (already applied?)")
