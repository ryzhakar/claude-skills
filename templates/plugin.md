# {{ plugin.meta.name }}

{{ plugin.meta.description }}

{% if plugin.meta.keywords is defined %}
{% for kw in plugin.meta.keywords %}`{{ kw }}` {% endfor %}
{% endif %}

{% if plugin.skills %}
## Skills

{% for skill in plugin.skills %}
### [{{ skill.name }}]({{ skill.plugin_path }})

{{ skill.description }}

{% if skill.references %}
**References:** {% for ref in skill.references %}[`{{ ref.name }}`]({{ ref.path }}){% if not loop.last %} · {% endif %}{% endfor %}

{% endif %}
{% if skill.scripts %}
**Scripts:** {% for s in skill.scripts %}[`{{ s.name }}`]({{ s.path }}){% if not loop.last %} · {% endif %}{% endfor %}

{% endif %}
{% if skill.examples %}
**Examples:** {% for e in skill.examples %}[`{{ e.name }}`]({{ e.path }}){% if not loop.last %} · {% endif %}{% endfor %}

{% endif %}
---

{% endfor %}
{% endif %}
{% if plugin.agents %}
## Agents

{% for agent in plugin.agents %}
### [{{ agent.name }}]({{ agent.plugin_path }})

{{ agent.description }}

**Model:** `{{ agent.model }}` · **Tools:** {{ agent.tools | join(", ") }}

---

{% endfor %}
{% endif %}
{% if plugin.hooks %}
## Hooks

{% for hook in plugin.hooks %}
### [{{ hook.name }}]({{ hook.plugin_path }})

{{ hook.description }}

---

{% endfor %}
{% endif %}
