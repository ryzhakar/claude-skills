# {{ marketplace.name | default("Claude Skills") }}

{{ total_skills }} skills · {{ total_agents }} agents across {{ plugins | length }} plugins

## Plugins

| Plugin | Description | Version | Components |
|--------|-------------|---------|------------|
{% for p in plugins %}
| [{{ p.meta.name }}]({{ p.dir_name }}/) | {{ p.meta.description | oneline | truncate(80) }} | `{{ p.meta.version | default("-") }}` | {{ p.skills | length }}S{% if p.agents %} {{ p.agents | length }}A{% endif %}{% if p.hooks %} {{ p.hooks | length }}H{% endif %} |
{% endfor %}

---

{% for p in plugins %}
## [{{ p.meta.name }}]({{ p.dir_name }}/) `{{ p.meta.version | default("-") }}`

{{ p.meta.description }}

{% if p.skills %}
### Skills

{% for s in p.skills %}
- **[{{ s.name }}]({{ s.root_path }})** — {{ s.description | oneline | truncate(140) }}
{% if s.root_references %}  References: {% for ref in s.root_references %}[`{{ ref.name }}`]({{ ref.path }}){% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}
{% if s.root_scripts %}  Scripts: {% for sc in s.root_scripts %}[`{{ sc.name }}`]({{ sc.path }}){% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}
{% if s.root_examples %}  Examples: {% for e in s.root_examples %}[`{{ e.name }}`]({{ e.path }}){% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}
{% endfor %}
{% endif %}
{% if p.agents %}
### Agents

{% for a in p.agents %}
- **[{{ a.name }}]({{ a.root_path }})** (`{{ a.model }}`) — {{ a.description | oneline | truncate(120) }}
{% endfor %}

{% endif %}
{% if p.hooks %}
### Hooks

{% for h in p.hooks %}
- **[{{ h.name }}]({{ h.root_path }})** — {{ h.description | oneline | truncate(120) }}
{% endfor %}

{% endif %}
{% endfor %}

---

*Generated README — run `just readme` to regenerate.*
