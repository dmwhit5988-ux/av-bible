# The garden in Eden: Genesis 2-3

Both chapters on one drawn place under one camera: 49 verses, 375.5 s of narration, 1024x576 and full
bleed, with no panel and no map. The narration carries the text. The pictures carry the place, and
what is done in it.

## Status: built (2026-11-01)

| What | Where |
|---|---|
| The land, the trees, the river and the plan | `garden_art.py` |
| The marks, the shots, the serpent's road, the host card, the engine, the rules for water and dusk, the plates, the build | `garden_stage.py` |
| Each verse: its camera legs, its events on their cues, its names, and what is not in the text | `genesis2_garden.py`, `genesis3_garden.py` |
| The people, the hand, the foot, the rib, the mound | `svg_figures.py` |
| What must be clear before a file is written, and `POSES`, the pose list | `garden_qc.py`, run by `garden_stage.write_story`, which writes both chapters or neither |
| Real frames, by hand: the seams between verses, and names by pixel difference | `tools/garden_seams.py` |
| The generators, either of which writes both chapters (so the two are one family in `svg_generators.json`), and the garden's palette that Genesis 1 and Numbers 1-2 import | `generate_genesis2_svg.py`, `generate_genesis3_svg.py` |

What the QC reports: still time 1.8% of the narration, 2.5% not counting the water; a man's median
height about 110 px at rest, and never under 40 px in frame; the largest file about 314 KB, and the
most animations in a file 129; the fastest camera 1064 px/s and 3.27/s.

## The idea

Both chapters happen on one long stretch of ground that the viewer comes to know like a stage set. Chapter 2 walks the man east into a garden that comes up round him. Chapter 3 takes the two of them east out of it, by stages: to the tree, to the shrubs they hid in, and at the last from under a close-up, on along the worn way through the last two trees at one walking pace, and out of the frame. They don't come back.

The camera has marks on that ground, and it goes back to them. So a reversal is a frame you have seen before with something gone. And a few times it goes right down to the one small thing, a hand and a fruit, two hands, a heel, a mound, so that the wide shots have something to cost.

What is only spoken of stands on the same ground in pale stone. That is the only figure colour of its kind in either chapter, and the one exception is the last thing she is called: "all the living" are warm.

Nothing stands for Yahweh. Nothing begins while his name is said, or just before it. Nothing goes looking for anyone on his behalf. What he does is seen in the world it happens to.

### The reversals, seen

| What turns | What you see | Shots |
|---|---|---|
| "There was not a man" / "from the presence of Yahweh God" | the same empty frame, twice | `pair` 2:5, `pair` 3:8 |
| not ashamed → fig leaves | facing each other, hand in hand; then the same camera, turned away, a gap, leaves | `pair` 2:25, `pair` 3:7 |
| walked with → hid | they run east out of the frame and it stands empty through his name; then two heads among the trees, which sink on "Where" | `pair`, `hid_wide` 3:8, 3:9 |
| eat freely → you ate | his hand takes a fig from the fig; his hand stops short of the fruit; hers stops further off; hers closes; the bare stem | 2:16, `fruit` 2:17, 3:3, 3:6, `stem` 3:11 |
| keep the garden → thorns and sweat | he raises one shoot at his plot; on "cursed" it wilts where it stands, in the same shot; a stone man digs with the same stick outside | `plot` 2:15, `plot` 3:17, `beyond` 3:17 |
| the breath of life → to dust | one camera path both ways: mound, man, colour coming down him; colour going, man sinking, mound | 2:7, 3:19 |
| the tree of life → the sword | a stone hand stops a hair from its fruit as the verse breaks off; the worn way warms from the wheel back to the tree's foot | `spray` 3:22, `last` 3:24 |
| level → ruled | two hands fingers to fingers; the same two, his down on hers | `hands` 2:23, `rule` 3:16 |
| the arm | the arm that names the animals points at her, and she points on, and it names her Eve | 2:19, 3:12, 3:13, 3:20 |
| the garden goes quiet | the water runs in every verse from 2:15, eases to a stop on "he ate", and runs once more, on "the mother of all the living" | 3:6, 3:20 |

### Surfaces by verse range

There is no other surface. No panel, chip, strip, list, inset or counter. The only thing not in the world is the title plate.

| Verses | Surface | How it is built |
|---|---|---|
| 2:1-2:4 | The heavens over bare land | `G.panorama("barren")` with the star wheel inserted after `G.sky_svg()`. 620 pips in three paths, turning about POLE (1200, -700) |
| 2:4-2:7 | The bare place | `G.panorama("barren")`. From 2:6's "watered", the wet palette (dust colours mixed 20% toward (10, 18, 14)) |
| 2:8-2:9 | The garden rising | `panorama("planted", lean=True, heroes=False, plant_in=...)`, wet palette, the river's bed dry (`river_svg` replaced by `dry_course_svg`). 2:8 opens on the bare land's own dry patches (`bare_scrub`), which go as the green comes; Eden's dry shoulder, where he was formed (`SHOULDER`), keeps its dust, its patches and the mound until he walks off it |
| 2:10 | The river comes, then the rise | The same ground with water opened by one clip rect, hung over the plan by `G.hang_in_plan` |
| 2:11-2:14 | The plan | `G.plan_svg`, no even green verge, banks wandering in width, one head's water running per verse from its name, its slivers fading in and out with the verse. Assyria is the Hiddekel's north bank, the tower's: the river "flows in front of" it. Each name hangs by what it names, a world point and a few screen px from it (`PLAN_NAMES`), so that it keeps by its bank or its heap at the close shots and at the plan's widest |
| 2:15 | The coming down | The planted side view hung over the plan |
| 2:15-3:7 | The planted side view | `panorama("planted", lean=True, heroes=False, flow=(0, dur), flow_reaches=("near",))`, trimmed to the flight, `heroes_svg(taken=...)`, the low bough on the tree of life, the near fig and its figs, the shrubs in `front`. The river's slivers come in with the camera over z .42-.54 (`bind_slivers`) |
| 3:8 | Dusk coming on | A rect under the cast from "cool", so they stay bright; and all that stands in front of them, the shrubs, the rocks and the near ground, coming in at its dusk colours over itself (a dimmed copy of `Scene.front`, the old going when it is whole), so that the verse's last frame is 3:9's first |
| 3:9-3:24 | The side view at dusk | The same, every scenery colour mixed 30% toward (14, 18, 38) (`dimmed`). No rect, no overdraw. People at full brightness |
| 3:17-3:24 | What stays | A dry patch at his plot, over the stick's mark, cracks east from it to x 2800, the dead shoot; from 3:22 the fig leaves on the ground at their feet, in the dusk's colours, wherever that spot is in frame |
| 3:18-3:24 | The thorn land | `Scene.outside` from `panorama(thorns_too=True)` and eight near thorns round x 2620. A clump of thorns is plants at depths of their own, so every clump stands wholly north of the river's bands, the near ones behind the line he stands on, where the river runs close along it, and a thicket of the land that would stand in the water is left out (`garden_art.water_top`). Thistle brush muted |
| 3:24 end | The worn way warmed, and stars | `way_ribbon` under the trunks; `far_stars`, 96 pips over the far ranges, as in 2:1's sky |

Plates are the close-ups: a drawing in world px with its own opaque ground. **A plate comes and goes by an edit:** the camera holds, or creeps, on the world, and on a word it is on the plate's rest at once; it goes out the same way, to a shot of the world (`Verse.cut`). Nothing is seen between: no dive past a body at the height of the hand, and no zoom that swaps the picture under it half way, in which people would vanish from the middle of a moving frame. A cut falls between two of the camera's baked keys; the camera holds the first until the time of the second and is on the second at once, and everything baked on the keys, a name's size, a sliver's opacity, a person's line weight, jumps with it (`VerseFlight`). The plate is in, whole, from the cut in to the cut out (`garden_stage.plate`, its opacity and visibility switched together at the camera's keys), and nothing is ever faded between the world and a plate, since a person under a dissolve is a person seen through. While one is in, the scene under it is switched off too (`VerseFlight.scene_visibility`), so that a close-up costs only its own drawing; the plate's ground covers the whole frame while it is in, and `test_garden.SceneOff` holds that for every verse. There are ten moments:

| Plate | Verses | Ground | Cut in, cut out |
|---|---|---|---|
| The fruit | 2:17 (and out in 2:18) | gradient `mbg` | "for", once his arm is up; 2:18 at 1.0 s, after his name, back to 2:17's `to_fruit` |
| The hands | 2:23 | flat #3e5a3c | once both arms are out on "This"; "She" |
| The fruit | 3:3 (and out in 3:4) | gradient `mbg` | "You", once her arm is up on "has"; 3:4 "serpent" |
| The fruit | 3:6 | gradient `mbg` | "wise"; "ate", the fruit at her mouth where the plate left it on the screen |
| The stitch | 3:7, hung at `stitch` (-125, 1090), in the air over the gap between their heads | flat #3a5638 | "sewed"; "made", a little wide of `pair`, creeping in to it |
| The bare stem | 3:11 (and out in 3:12), hung at `stem` (930, 1300) | `mbg`, dimmed | "Have"; 3:12 "man" |
| The heel | 3:15 (and out in 3:16) | flat #47533a, dimmed | "He"; 3:16 "he", once the foot has lifted out |
| The rule | 3:16 (and out in 3:17) | flat #39543a, dimmed | once her arm is out on "husband"; 3:17 "Adam" |
| The mound | 3:19, and out in 3:20 hung under its camera at `MOUND_HUNG` (810, 1397) | flat #544730, dimmed (`MOUND_REACH`) | once he has all but sunk on the second "dust", from above the thorns; 3:20 "man" |
| The spray | 3:22, and out in 3:23 hung under its camera at `SPRAY_HUNG` (1990, 900), in clear sky above the treetops | flat #465048, dimmed | "hand", once his arm is up on "reach"; 3:23 "sent", after his name |

A plate's forearms run on past the frame's edges, and anything on it that comes in later waits out of the frame, held there from the verse's start, since before its begin a move is no move at all: his hand at 3:16, the leaves at 3:7. At 3:6 the hand pulls the fruit off to where the cut back puts it at her mouth, so that the one bright thing keeps its place on the screen and only its size changes.

A verse that opens on a plate draws that plate's rest, so the seam is clean. **A plate is opaque, so the world under it can be anywhere:** it is hung by the shots the verse cuts between, because the scenery a verse draws reaches as far as its camera's keys (`garden_stage.seen`): the stem by him at 3:11 and 3:12, the stitch over their heads at 3:7, the mound under `eve` at 3:20 and the spray over the worn way at 3:23. 2:21's chest at z 6.5 and 2:7's handful at z 7 are the real scenery, not plates: they stand on bare ground and hold up.

What a frame costs is what is in it, since anything that moves repaints the whole picture inside its `<img>`. So each verse's scenery is trimmed to what its camera can see (`Scene.trimmed`, by real boxes); the haze over the far land is mixed into the far bands' and ranges' own colours by how much air lies in front of them, and the dusk from 3:9 into the scenery's (`garden_art.tinted`, `garden_stage.dimmed`), with no translucent rect over the picture; no ground goes further down than what covers it. The side view dissolves over the plan, at 2:10 and 2:15, through a group opacity over z .09-.16 (`garden_art.SIDE_IN`), short because both pictures are painted while it runs, and the plan is switched off whenever the side view covers it. The plan's garden and its crowns come in only as the side view goes, under z .12 (`garden_art.plan_garden`): seen from above they are dark rosettes, and would stand in the side view's sky.

## The rules

From the owner, standing:

1. **Text.** The verse is narrated. Names, numbers, labelled drawings only, in WEB's wording, revealed when said. Georgia. No caption, verse counter, progress dot, chip, list, ledger, speaker tag, arc, X, or arrow, under any name.
2. **No flashing text.** Opaque once in. Names never touch figures, lines, scenery or other names at rest: 3 px of air, checked from the geometry (`garden_qc.name_air`) and by pixel difference (`tools/garden_seams.py`). The title plate is never covered.
3. **No gold-on-gold.** HL (255, 244, 170) is the one highlight. Pulses have a floor of 0.6 alpha when they hold. Scenery ink stays muted.
4. **Draw once, then hold.** A thing animates on the verse it first appears. Highlight by pulsing an outline, never redrawing it.
5. **The only loop is the wheel of 3:24.** Everything else stops by the end of its verse's narration. Checked from the files.
6. **A figure changes pose only on its verse's narrated event.** `garden_qc.POSES` lists every pose and the word it hangs on, for the owner to read. Nothing re-animates as decoration. The water and the wind are not figures, but each is argued and finite.
7. **1024x576, always.** The displayed size never jumps.
8. **Yahweh is never drawn.** No figure, hand, face, light, glow or emblem. Nothing goes through the world in his place: no leaves on the air after "voice walking", no camera that goes back to look.
9. **No sign answers his name.** Nothing new begins from .3 s before "Yahweh" or "God" until the next word. Camera legs and cuts too, and a plate's coming or going, though the switch under it is never seen: 3:23 holds on the spray through "Yahweh God" and cuts to the walk on "sent". A wave of trees or a walk already under way may carry on through it: there are two, 2:9's trees and 2:21's departing beasts. A thing already moving doesn't turn back or set off again on it either: in 3:1 his head holds through "God", and draws back on "said". Checked (`garden_qc.his_name`). The Chi-Rho is not used (decision 1).
10. **The flaming sword is a wheel of flame.** Never a blade. Seven tongues out, five in, a bright core: `_tongue()`'s idea. 6 s a turn.
11. **The cherubim keep Exodus 25's feathered wing** (`generate_tabernacle.feathered_wing`). Heads bowed and hooded, not a ball on a pawn.
12. **Modesty.** Unclothed silhouettes with no anatomical detail, blank faces, her long hair. 2:25 and 3:7 must be innocent to watch with a child in the room, and so must every close shot: a close shot of an unclothed person stops at the hips or above them (`chest`, `two_heads`, `mouth`, `to_fig`, `head_chest`), he lies with both legs straight, and no camera dives through a body on its way to a plate: it cuts.
13. **Faces are blank.** A profile has a nose and a beard or hair, and no eye. Anywhere a design needed an eye it now needs the head's angle (`up`) or the camera.
14. **East is right.** Both walks go east. The way out is to the right.
15. **WEB only. SMIL only.** No script, CSS animation, raster, external file, web font, still image, reduced motion, speed control or notes toggle.
16. **Geography.** No line from a map. The fan of four rivers is pictorial.
17. **Size.** Under about 350 KB a file (today's largest is 314 KB). Under about 130 concurrent animations (today's most is 129 in a file). `<defs>`/`<use>` for anything that repeats.
18. **No filter or mask inside the camera group.** Clip paths only for the length of a verse, on the rising figures and coats, the plan's heads and the one run of water at 2:10. Never on the camera's group. The card's own clip and border are not drawn (`Stage.verse_svg`).
19. **WebKit.** No tspans. `h.001`, not `h0`. No `dx`/`dy` in em under an animated font size without `em_tick`. **keyTimes strictly non-decreasing, starting at 0, ending at 1 unless discrete:** A list like `.250;.241` is dropped silently by WebKit and Edge, which leaves a hand a hand's breadth short. `garden_qc.key_times` checks it.

Of this design, and just as binding:

20. **One foreground thing at a time.** At most one figure acts on a word. The camera may carry that action, and the water is background. Where the text lists things (3:15) they come one after another on their words. If two things want the same word, drop one. "Three things at once are as bad as nothing."
21. **A body is never see-through, and an arm or a head that moves is a limb.** A change of the arms or the head alone is a limb turning from the shoulder: the event carries `_morph`, and the drawing's own paths animate through a mid-pose interpolated by the joints' angles (`_morph_drawing`, `_chain`), with no fade at all, since an arm faded in over the old one would be a second arm, seen through. The stick and the head go with it. A narrated gesture, in 2:7, 2:15, 2:16, 2:19, 2:23, 3:2, 3:6, 3:12, 3:13, 3:17-20 and 3:22, takes .3-.9 s; the arms and heads that only follow the story, 2:16's head, the arms to the fruit and back at 2:17 and 3:3, 3:6's arm out with the fruit, 3:7's sewing and covering, 3:8's arms drawn in and 3:17's arms down, take .25-.35 s (`test_garden.Looks` holds that every such change is a limb). Any other change of look fades its new look in over the old (d about .2-.35 s), as 3:7's leaves come on once their hands are at their hips, and the old goes when the new is whole, or when a later look is, if that is sooner; a change of the whole body, turning round, kneeling, lying down, getting up, setting off on a walk or stopping, is nearly a cut (`TURN_S`, .04 s), because two outlines that barely overlap would show two heads, two pairs of legs, or two of him. Do it in `garden_stage.Stage._actor`, never in the shared card (its bytes must not change for Joshua and Acts). Nobody fades in or out in plain view: he comes out from behind the trunk at 2:15, a stone figure stands up out of the ground and goes back into it (`stand_up` at 2:24, 2:25 and 3:15, the card's `grow` at 3:17 and 3:22), and at 2:10 and 3:24 they leave by the frame's edge, and at 3:24 they are switched off at the first moment the frame has lost all of them, their shadows too, wherever 3:23's narration has left them (`walk_on`; `test_garden.Looks` holds that no one on the card is switched off in sight). So do the serpent at 3:16 and all the living at 3:21, and the small snakes of 3:15 come in by it, as the serpent comes into sight at 3:1, sliding out from under the crown, where his road begins beyond 2:25's frame (`S_IN`); what goes while a close-up covers it, the small snakes at 3:16, is simply gone when the camera comes out. Nor is anything faded between the world and a plate: it cuts.
22. **Stone is what is only spoken of.** Father, mother, son, bride (2:24). Her children, and the foot (3:15). The man who digs and dies (3:17-19). The man at the tree, and the hand (3:22). One solid treatment: the pair's own profile drawing in pale warm stone (`stone` paint), cap, hair and beard lighter than the face so that a head doesn't read as a hood, in a coat, or in leaves when he is the man himself. Never a see-through outline, never the vocabulary's robes. **All the living (3:20) are the exception, on purpose:** the same drawing in the live paint, small (k .40-.58) and far off. They are the living, and she stays the largest figure in the frame.
23. **The light goes once,** on "cool" in 3:8, and it is dusk for every verse after.
24. **The water.** Runs for the length of each verse from 2:15 to 3:5. In 3:6, `flow=(0, 14.10)`, so it eases to a stop on "he ate" with the river in frame. Not again but 3:20, from "mother" to the end. Tapered, wavering slivers at varied offsets and lengths in light blue, on a still ribbon: no centred dashes, no white. Only the "near" reach runs.
25. **The camera never closes past z 1.6 on thorns or thistles.** Their cups are hexagons, and at z 2.6 and up they are the crudest thing in the two chapters. 3:19 holds at z 1.38 while he sinks, then cuts to the mound's plate.
26. **People are never under 40 px in frame** (z .364). They go out of the frame instead. No figure fades in below that either.
27. **Ten plate moments in 49 verses, and no more.** If a plate is added, one comes out.
28. **Line weight rides the camera.** A person's keyline and contour inherit `stroke-width`: `key_w(z) = 4.6` at z ≤ 1, else `4.6 / z^.86`; `body_w(z) = 2.1`, else `2.1 / z^.82`; animated at a fifth of the camera's keys.
29. **Each file can be entered cold.** Its rest must say what the verse is, on its own.
30. **The camera is not seasick.** No verse's camera peaks over 1200 px/s across the screen or 3.3/s in zoom. Checked from the baked keys (`garden_qc.camera_speed`). The published tours have a median peak of 169 px/s and .54/s; two of 233 pass 1200 px/s and three pass 3.3/s. These chapters are busier: median 233 and 1.16, most 1064 and 3.27. A cut to or from a plate is an edit, not a move, and isn't measured.
31. **Nothing stands still for long.** The longest time anywhere in a verse with nothing moving, the water aside, is under 2 s, named stillness aside. A hold that would be longer is a creep of 2-5% zoom. A re-shot arrives a little wide and creeps in to its exact value, so re-shots stay equal (`Verse.settle`).
32. **A walk has a pace.** People walk at about 155 px/s, stride .5, 2:9's pace, whether they are walking in or walking out. Only 3:8 runs. A long walk or a beast leaving is at a steady speed (`STEADY`, no ease), so that it carries over a verse's seam without slowing and its feet don't skate.

## What is not in the text

None of this is named on screen. All of it can be ruled out by the owner.

**The land** (from the art; see `garden_art.py`'s docstring). Every species but the fig. The shapes of the two named trees, and life standing west of knowledge. The flowers, the far ranges, the two old cypresses as the last trees, the worn way, Cush's acacias and red hills, the walled tower, the palms and reeds, the gold heap, the bdellium as a tree, the banded stones, the dark sky.

**Chapter 2.**
- 2:1-3: the stars as a wheel, turning, and their stop on "rested". 2:4: the descent.
- 2:5: the camera looking at the ground where the two trees will stand, before they are named; wind over the dust; thin dry cloud; the stage being empty as the frame for "There was not a man".
- 2:6: the look of the mist; the ground staying dark.
- 2:7: the mound, grains, a man rising in the ground's colour, the colour coming down from the head, his hands opening. That he is formed west of the garden and walks to it (from "eastward... and there he put the man").
- 2:9: that he walks through it as it grows; the order.
- 2:10-14: nobody on the plan; the camera's stops.
- 2:15: his plot, on the ground east of the tree; the digging stick; the one shoot, which stays; his coming out from behind the trunk on "put", from a little further back than the people's line.
- 2:16: that the tree he eats from is the near fig, the same that gives 3:7's leaves; the figs, hanging from 2:9.
- 2:17: the walk to the fruit; his hand; which fruit; its swinging at "die"; him stepping back unseen.
- 2:19-20: which animals (lions, wolves, sheep, oxen, donkeys, four birds), two of each; rising out of the ground with grains; the birds on the crown; the arm; one pulse for each name, and no name written; that they walk away.
- 2:21: the dark for the deep sleep; kneeling first; his chest, and his arm at rest beside him; a line on his side; the rib and its size, bone white, sliding out from under his skin, no hand.
- 2:22: her rising where the rib lies, behind him; in bone white, her colour running down after, as his did; that she walks along him to where she's brought.
- 2:23: the two hands. 2:24: father, mother, son and bride in stone coats on the near bank, standing up out of it, and at 2:25 going back into it; the son's walk.
- 2:25: facing each other, hand in hand.

**Chapter 3.**
- 3:1: where the serpent was, and the way he comes; his colour, bands and the chevron on his nape; no legs; the tongue; his head going on and back as he speaks; that she lets go and lifts her head to him, and the man is with her.
- 3:2: her arm. 3:3: her walk to the fruit; her hand stopping as she quotes "touch".
- 3:4: his head coming down by her face: nothing happens to him, which is his argument.
- 3:5: the camera opening on "opened"; her head lifting; the pulse across the crown.
- 3:6: which fruit, and where; one ring; her head lifting by steps; one fruit for both ("some of its fruit"), crossing the air; the stem left behind; the water stopping.
- 3:7: heads up, then down; turning away; two leaves coming down, one over the edge of the other, one hand closing on the first; four stitches through their overlap, the thread's end in her fingers; her hands being the ones we see. That the coverings go round the hips.
- 3:8: the dusk on "cool of the day"; that they run; east; shrubs; that they kneel; that the camera holds as they go. That the serpent stays on the bough, 3:7-3:13.
- 3:9: their heads sinking. 3:10: his coming out; where; the head, the arms, the step back.
- 3:11: the stem shown at "Have you eaten"; the outline where the fruit was; the stem swinging.
- 3:12: her getting up; the pointing arm, low, under the fruit; his backing away. 3:13: her walking past him; the direction of the arm; the serpent's head lifting; that the man doesn't turn.
- 3:14: that he pours off the tree; where he lands; his crawl east, to her feet; dust at his mouth.
- 3:15: hostility as a gap and a raised head; three small snakes, in a file from beyond the frame; three stone children standing up behind the man; one bare stone foot with no one above it; that it's the heel on the head and the same heel struck; one ring.
- 3:16: the foot lifting out; the serpent drawing back along the ground and going west out of the frame, the last of him; arms round her middle, the bend; her walking to him and reaching; that "rule" is his hand coming down on hers.
- 3:17: his glance; that he stands at his plot; the shoot wilting; the dry patch; cracks east; that the stone man is himself, ahead of time, outside the garden, before he is sent; the same stick. **That the land where he digs, and where the mound lies (x 2620), is between the wheel (2520) and the east cherub (2660), so the place of his toil lies inside what is later guarded.** Moving it east of them makes `beyond` a flight of 2460 px, and 3:17 fails rule 30. The mound is a plate, and isn't left there at 3:24; the thorns are.
- 3:18: thorns rising round that place; the herb; the kneeling.
- 3:19: hand to brow; a hand to the mouth with no bread; kneeling; the colour going; the sinking; the mound.
- 3:20: the arm; ten small warm figures, how far off, and which way they go; the water running once more.
- 3:21: the living walking off east, out of the frame; coats rising from the hem; their shape; the leaves dropping, and lying where they fell from then on. No animal seen.
- 3:22: the crown's second pulse; the stone man at the tree; the low bough; where the hand stops.
- 3:23-24: her going with him ("him", "the man"); that he walks a little ahead; two cherubim, one each side, heads bowed; the wheel (the owner's ruling, `_tongue`'s idea); that the two don't look back; the worn way warming; the stars; that the last frame has no one in it.

## Decisions for the owner

Each has a default, and the default is what is built, unless the owner says otherwise. The owner has ruled on none of them yet: answers go here as they come.

| # | Decision | Default | The alternative |
|---|---|---|---|
| 1 | **The Chi-Rho at 3:15** | None. One bare stone foot, no one above it, the text left to say who he is | The Chi-Rho over the foot at "He" |
| 2 | **Stone for what is only spoken of** | Yes, solid, the pair's own drawing in a coat, in pale warm stone; and "all the living" warm and small. | Nothing drawn at 2:24 and 3:20 (and 3:15-19, 3:22's man), the verse left to the narration. Or warm robed people |
| 3 | **The foot on the head, and the heel** | Yes, quick, at z 7, the one blow in the two chapters | A small stone man stamping at z 1.36, or no contact |
| 4 | **The stone man who goes back to dust, 3:17-19** | Yes: a kneeling stone figure whose colour goes, then a mound. No body. He is alive at 3:20 | The living man takes up a handful and lets it run out; no one dies on screen |
| 5 | **The stillness of 2:2, and the wheel as a sign** | Keep: the wheel stops on "rested", 3.1 s of nothing, then 2:3's name warms on "blessed", with a 3% creep of the frame. **The question this is:** the sky stopping is mapped to his work stopping, and a name warming straight after "God". Is that a sign answering him? It is read here as the verse's own rest, seen in the sky | Stars turning on, slower, through 2:3; no stop, no sign, and it loses "rested". Or a sun crossing |
| 6 | **The dusk at 3:8** | On "cool", dusk only. Nothing crosses the frame: anything moving through the garden straight after "voice walking in the garden" reads as his passing | The five leaves on the air, east to west, a good second and a half after his name |
| 7 | **The camera at 3:8-3:9** | It holds on `pair` as they run out of it, so the frame stands empty through his second name; then at 3:9 it holds on them, and on "Where" their heads sink. It doesn't go looking: a camera that sets off on "called" and lands on "Where" is a searcher's point of view | It goes back and finds the empty frame at 3:9 |
| 8 | **The water stopping on "he ate", and once more at 3:20** | Yes. Not a claim about the river: the garden going quiet, and "all the living". **The cost is real:** from 3:7 to 3:24 nothing but the people moves in the world, and they stand while the voice speaks, so the camera's creep is all that moves for about 48 s of 147 s | Quarter-speed water through 3:7-3:24: nothing ever quite stops. It loses the stop. Or never again. Or it never stops |
| 9 | **The serpent stays on the bough, 3:7-3:13** | Yes | He goes out of sight until 3:13 |
| 10 | **"He will rule over you"** | The hands: his over hers, slow, in the shot of 2:23 | Nothing on "rule", if it reads as holding hands. Or he points and she goes. Or he walks past her |
| 11 | **The digging stick at 2:15** | Yes, because 3:17 needs the same stick to be the same labour | Hands in the ground |
| 12 | **Ten plates** | All. They are the strongest frames. Each runs to the verse's end or comes straight out again, and none but 3:6's is more than one verse's work | Drop 3:7's stitch first: leaves from the near fig at `pair`, hands together, and the frame never leaves 2:25. It is the plate to give up first, though sewing is one of the things the owner asked to see done |
| 13 | **3:4: his head close by her face** | Yes, on `two_heads`, tongue on "You" | His nose on the fruit, on the plate: an old reading, not the text |
| 14 | **2:7: the breath** | Nothing in the air. The colour runs down from the head. Grains drawn in at the nose would be an unseen breath, the nearest thing to his act that's drawn | Grains in the air before his face, drawn in at the nose by "nostrils" |
| 15 | **The title of chapter 3** | "The Garden in Eden — Genesis 3": "The Garden Undone" would tell the ending | "The Garden Undone" |
| 16 | **The last frame, and the walk to it** | No one. They walk at 155 px/s without a stop, past the east cherub by "cherubim", out of `gate`'s right edge by about 5.5 s as the wheel opens, and the stars of 2:1 come out. Only the wheel moves. **The cost:** warped under the plate, they start at x 1620, so the walk past the shrubs isn't seen | The two stay small at the right, at 37 px against the 40 floor. Or one look back of under a second, unnarrated |
| 17 | **His plot beside the trial** | He works the ground east of the tree, so 3:17's shoot wilts where he stands. The garden's west is then only walked through | A plot in the west, and no wilting |
| 18 | **The man ahead of the woman going out** | He leads by 50 px: the verses say "him" and "the man". Warped under the plate, so neither overtakes the other | Together, side by side |
| 19 | **Hand in hand at 2:25, in profile** | In profile, facing each other, as they have stood since 2:23. It turns the reversal of 3:7 into facing, then turned away, and it needs no frontal drawing, which would be a different, bull-necked person, a swap in .25 s and an unnarrated turn at 3:1 | Face on, the only frontal frame: the frontal slimmed to the profile's shoulder and neck first |
| 20 | **The dark at 2:21-22** | Yes, a third, lifting at "The man said" | No dark |
