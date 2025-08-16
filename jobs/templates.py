from jinja2 import Template

HTML_EMAIL = Template("""
<h2>🚀 Daily Startup Job Digest — {{ date_str }} {% if mode == 'preview' %}(Preview){% endif %}</h2>
<p>Found {{ jobs|length }} matching roles.</p>
{% for j in jobs %}
  <div style="margin:16px 0;padding:12px;border:1px solid #eee;border-radius:10px;">
    <div style="font-size:16px;font-weight:600;">{{ loop.index }}. {{ j['title'] }} — {{ j['company'] }}</div>
    <div><a href="{{ j['url'] }}" target="_blank">{{ j['url'] }}</a></div>
    {% if j['location'] %}<div>📍 {{ j['location'] }}</div>{% endif %}
    {% if j['description'] %}<div style="margin-top:6px;">{{ j['description'][:280] }}{% if j['description']|length > 280 %}…{% endif %}</div>{% endif %}
    <details style="margin-top:8px;">
      <summary>💬 LinkedIn outreach draft</summary>
      <pre style="white-space:pre-wrap;font-family:ui-monospace, Menlo, monospace;background:#fafafa;padding:8px;border-radius:8px;">{{ j['outreach'] }}</pre>
    </details>
  </div>
{% endfor %}
<p style="margin-top:16px;">— Bot</p>
""")

PLAIN_TEXT = Template("""Daily Startup Job Digest — {{ date_str }} {% if mode == 'preview' %}(Preview){% endif %}

Found {{ jobs|length }} matching roles.

{% for j in jobs -%}
{{ loop.index }}. {{ j['title'] }} — {{ j['company'] }}
Link: {{ j['url'] }}
{% if j['location'] %}Location: {{ j['location'] }}
{% endif -%}
{% if j['description'] %}About: {{ j['description'][:280] }}{% if j['description']|length > 280 %}…{% endif %}
{% endif -%}
Outreach:
{{ j['outreach'] }}

{% endfor -%}
— Bot
""")
