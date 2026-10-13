# Content sheet templates

Field lists come from the content tracker (section in brackets). Every sheet starts with:

```markdown
**Status:** draft
**Type:** <type>   **ID:** <type-prefix>-<slug>   **Tracker:** §<n> <item>
**Canon sources:** <links>
```

and ends with:

```markdown
## Connections
## Writing briefs      # one line per player-facing text field; no prose
## Runtime notes       # Content Language v1 mapping
## Language gaps
## Missing sheets
## Open questions      # [PROPOSED] items with options
```

| Type | ID prefix | Body fields |
|---|---|---|
| Named NPC [§8] | `npc` | Role · Public personality · Desire · Fear · Secret (with layer) · Allies · Rivals · Relationship to settlement · Relationship to player-facing conflicts · Species · Coupling (as canon defines it) · Schedule and haunts |
| Generic NPC template [§8] | `npct` | Role · Where found · Variation knobs (species, gear, attitude) · What they know (rumor layer) · Typical barks (briefs only) |
| Faction [§9] | `fac` | Name · Purpose · Leadership · Membership · Resources · Territory · Goals · Allies · Enemies · Internal disagreement · Relationship with the player · Stance on the world's central traditions |
| Item [§10] | `item` | Category (survival / weapon / armor / technology / salvage / magic) · Era layer · Tech level · Rarity · Who makes, sells, or finds it · Function · Mechanics `[PROPOSED]` · Lore layer it can reveal |
| Creature / enemy [§11] | `cre` | Category (humanoid / wildlife / supernatural / construct / canon's other kinds) · Origin (native, altered, or arrived by canon's means) · Territory and terrain · Behavior · Threat tier `[PROPOSED]` · Drops or salvage · What it teaches the player about the world |
| Conflict [§12] | `con` | Category · Parties (≥2 NPCs, ≥1 faction, ≥1 location) · Stakes · Current state · How it escalates without the player · Player entry points · Possible resolutions |
| Mystery [§13] | `mys` | Public explanation · Common rumors · Evidence (item, location, NPC for each) · NPCs who know part · Specialist interpretation · Hidden truth · Deeper implication · Connection to the larger world |
| Adventure hook [§14] | `hook` | Type (village problem, escort, salvage, …) · Giver · Premise · What it reveals about the world · Locations · Rewards · Leads to |
| Zone [§6–§7] | `zone` | Settlement or surrounding · Focus themes · Terrain · Rooms (list, 30–40 total target across zones) · Exits to other zones · Residents and spawns · Secrets located here |
| Room [§6] | `room` | Zone · Function · Exits · Contents (NPCs, items, fixtures) · Environmental storytelling beats · Layers revealed here · Writing brief for short and long description |

Rules:
- Every Secret or Deep truth field says which layer and how the player can reach it.
- A mystery sheet must place evidence for every layer somewhere findable, or list it as missing.
- A conflict with fewer than two NPCs, one faction, and one location is incomplete by the tracker's rule.
