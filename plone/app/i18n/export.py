from StringIO import StringIO

def po_export(domain, language, messages):
    charset = 'utf-8'

    out = StringIO()

    print >> out, """# Gettext Message File
msgid \"\"
msgstr \"\"
\"MIME-Version: 1.0\\n\"
\"Content-Type: text/plain; charset=%s\\n\"
\"Content-Transfer-Encoding: 8bit\\n\"
\"Language-code: %s\\n\"
\"Preferred-encodings: %s\\n\"
\"Domain: %s\\n\"

""" % (charset, language, charset, domain)

    for message in messages:
        out.write(u"""
msgid \"%s\"
msgstr \"%s\"""" % (message['msgid'], message['msgstr']))

    return out.getvalue().encode(charset)    
